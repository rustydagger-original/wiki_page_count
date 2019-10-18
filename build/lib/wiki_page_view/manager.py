import os
import sys
import time
import argparse
import logging
import multiprocessing
from yaml import load

from wiki_page_view import WikiPageView

def config_logger(log_filename):
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    if not os.path.exists(log_filename):
        os.makedirs(os.path.dirname(log_filename))

    fileHandler = logging.FileHandler(log_filename)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(logging.INFO)
    return rootLogger

def worker_init(*worker_args):
    global WORKER_ARGS
    WORKER_ARGS = worker_args


def worker_fn(date):
    fn = WORKER_ARGS[0]
    fn_args = WORKER_ARGS[1:]

    try:
        fn(date, *fn_args)
    except KeyboardInterrupt:
        # don't print the stack trace for keyboard interrupts, just exit
        pass
    except Exception as e:
        print e
        raise

def apply_to_dates(dates, fn, num_thread, *fn_args):
    if len(dates) == 0:
        return

    worker_args = (fn,) + fn_args

    if len(dates) == 1 or num_thread == 1:
        worker_init(*worker_args)
        for date in dates:
            worker_fn(date)
    else:
        pool = multiprocessing.Pool(
            num_thread, maxtasksperchild=10, initializer=worker_init, initargs=worker_args
        )
        try:
            pool.map_async(worker_fn, dates).get(9999999)
            pool.close()
            pool.join()
        except KeyboardInterrupt:
            pool.terminate()
        except Exception as e:
            print e
            pool.terminate()


def main(dates):

    with open(os.path.join(os.path.dirname(__file__), "config.yml")) as fd:
        config = load(fd.read())

    if not os.path.exists(config["output_directory"]):
        os.makedirs(self.output_directory)

    logger = config_logger(config["log_entry"])
    view = WikiPageView(logger, config["pageviews_url"], config["output_directory"], proxy=config.get("custom_proxy"), black_list=config.get("black_list_url"))
    apply_to_dates(dates, view.process_data, config['num_of_thread'])

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Compute Wiki Page View Count")

    arg_parser.add_argument('dates', help='date format is 2019-10-18:23 year-month-day:hour Date time is in GMT zone', nargs='*')
    args = arg_parser.parse_args()
    if not args.dates:
        args.dates.append(time.strftime("%m/%d/%Y:%H", time.gmtime()))

    main(args.dates)