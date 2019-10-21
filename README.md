# wiki_page_count
Simple application to compute the top 25 pages on Wikipedia for each of the Wikipedia sub-domains

This project consists of the following compoents
```
      1     config.yml
            
            Contains various porject settings, such as 
            
            log_entry: "./logs/wiki_page_view.log"
            output_directory: "./output"
            black_list_url: "https://s3.amazonaws.com/dd-interview-data/data_engineer/wikipedia/blacklist_domains_and_pages"
            pageviews_url: "https://dumps.wikimedia.org/other/pageviews"
            custom_proxy: {}
            num_of_thread: 6
            
      2     down_loader.py
      
            Responsible to make http request and download data, error handle on 404 data not found
            
      3     manager.py
            
            Main program to call to run the project. 
            Includes multiprocessing when running on multiple data/hour sets
            
      4     run_wiki_page
            Shell script to run manager.py. This shell script can be used with crontab commands for running in interval
      
      5     wiki_page_view.py
      
            The engine for this project. Using Pandas to do data analytics, filtering and aggregation. 
            Output results to local file
```

1. What additional things would you want to operate this application in a production setting?

      This project requires Python 2.7.16 or higher version to run, and it's been tested  with the following python version and enviroment
      
        Python 2.7.16 (default, Oct 10 2019, 01:00:19)
        [GCC 7.3.1 20180303 (Red Hat 7.3.1-5)] on linux2

    config.yml contains setting specific to this program, user can change accordingly
    
    For example, if running behind a firewall, and get request denied when downloading, user can add the following to config.yml
    
        custom_proxy: {"http": [proxy url with port], "https": [proxy url with port]}

2. What might change about your solution if this application needed to run automatically for each hour of the day?
    
    In unix environment, we can create crontab job, and on Windows, we can use window scheduler to run on intervals

    For example, in Unix, to run the program every hour at 50min pass the hour for the day
    
        '50 * * * * /directory/run_wiki_page'

    As I experienced, the data file for the hour doesn't get uploaded to the wiki website until late in the hour, so I set the starting minute to 50
    
3. How would you test this application?

    Simple test case, run in path ./wiki_page_view/
    ```
      python manager.py --help # Display usage info
      
      python manager.py # Run to get data for current date and hour, GMT time
    
      python manager.py 2019-10-17:12 # Run to get data for 2019-10-17 12PM GMT time
    
      python manager.py 2019-10-17:12 2019-10-17:11 2019-10-17:10 # Run on range of day/hours
    ```

4. How you’d improve on this application design?

      I used Pandas to do the data analytics part, to aggregate the page view count. As future improvement, I can make a configuration schema file, to plug in different module (such as python native collection, sorting, etc, or other third party package). 
