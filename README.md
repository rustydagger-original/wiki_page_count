# wiki_page_count
Simple application to compute the top 25 pages on Wikipedia for each of the Wikipedia sub-domains

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
