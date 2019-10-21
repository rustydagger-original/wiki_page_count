import os
import sys
import gzip
import time
import pandas as pd
from io import BytesIO
from collections import defaultdict, deque
from down_loader import DownLoader


class WikiPageView(object):
    def __init__(self, logger, pageviews_url, output_directory, proxy=None, black_list=None):
        self.logger = logger
        self.pageviews_url = pageviews_url
        self.output_directory = output_directory
        self.worker = DownLoader(self.logger, proxy=proxy)
        self.content = defaultdict(lambda: defaultdict(int))
        self.black_list = self.get_black_list(black_list)

    def download_data(self, url):
        response = self.worker.download(url)
        return response

    def get_black_list(self, black_list):
        self.logger.info("start download blacklist {0}".format(black_list))
        data = self.download_data(black_list)
        if data:
            return self.process_black_list(data)

    def process_black_list(self, data):
        with BytesIO(data) as black_list_data:
            frame = pd.read_csv(
                black_list_data,
                sep=" ",
                header=None,
                names=["domain_code", "page_title"],
                error_bad_lines=False,
                encoding="utf-8",
            )

        return frame

    def process_data(self, date_hour):

        try:
            time.strptime(date_hour, "%Y-%m-%d:%H")
        except ValueError as e:
            raise

        date, hour = date_hour.split(":")
        year, month, day = date.split("-")
        url = "{0}/{1}/{1}-{2}/pageviews-{1}{2}{3}-{4}0000.gz".format(self.pageviews_url, year, month, day, hour)

        local_file_name = url.split("/")[-1].replace(".gz", "") + "-page_count"
        local_path = os.path.join(self.output_directory, local_file_name)

        # Check if the work has already been done for the given day and hour.
        if os.path.exists(local_path):
            self.logger.info("{0} has already been processed, the result file is in {1}".format(date_hour, local_path))
        else:
            self.logger.info("start download from {0}".format(url))

            data = self.download_data(url)
            if data:
                self.logger.info("process downloaded data for {0}".format(date_hour))
                self.process_data_by_page_count(data, local_path)

    def process_data_by_page_count(self, data, local_path):

        with gzip.GzipFile(fileobj=BytesIO(data)) as zip_data:
            frame = pd.read_csv(
                zip_data,
                sep=" ",
                header=None,
                names=["domain_code", "page_title", "view_count", "response_size"],
                index_col=[0, 1],
                error_bad_lines=False,
                encoding="utf-8",
            )
        #Eliminate any pages found in blacklist
        merged = frame.merge(self.black_list, how="left", on=["domain_code", "page_title"], indicator=True)
        not_in_black_list = merged[merged["_merge"] == "left_only"]

        #Compute the top 25 articles for the given day and hour by total pageviews for each unique domain in the remaining data.
        agg_page_view = not_in_black_list.groupby(["domain_code", "page_title"]).agg({"view_count": sum})
        agg_page_view_count = agg_page_view["view_count"].groupby(level=0, group_keys=False)
        result = agg_page_view_count.nlargest(25)

        #Save the results to a file, either locally or on S3, sorted by domain and number of pageviews for easy perusal.
        self.logger.info("write page_count data into {0}".format(local_path))
        result.to_csv(local_path, sep=" ", header=False, encoding="utf-8")
