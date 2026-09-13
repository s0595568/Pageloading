# Pageloading project

## _Page Speed Insights Test_

PSI is a script that is written in Python3 which uses Google service of measuring the loading speed of your webpage. 
Currently, it is configured to run for both mobile and desktop and will create different metrics for each. 
Capturing the real-time page scores (current setup is every four hours - configurable) helps you to analyze the comparison with other pages and the page itself. 
There are variety of measures PageSpeed API returns, but we are currently interested in core web vitals: 

- Overall Performance Score,
- "fcp": FIRST_CONTENTFUL_PAINT_MS,
- "fid": FIRST_INPUT_DELAY_MS,
- "lcp": LARGEST_CONTENTFUL_PAINT_MS,
- "cls": CUMULATIVE_LAYOUT_SHIFT_SCORE,
- “fcp_score”: FIRST_CONTENTFUL_PAINT_MS,
- "fid_score": FIRST_INPUT_DELAY_MS,
- “lcp_score”:LARGEST_CONTENTFUL_PAINT_MS,
- "cls_score": CUMULATIVE_LAYOUT_SHIFT_SCORE,
- "inp": EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT,
- "ttfb": EXPERIMENTAL_TIME_TO_FIRST_BYTE
- "tbt": total-blocking-time
- "si": speed-index

# Input of the script: 

Urllist.json contains list of urls under test.

# Output of the script:

The script saves the core web vitals directly into the database 
 
- Link: BI-02.tcsrv.net:3306
- Database: QA 
- Table: pagespeed 

Every row of the table consists of core web vitals along with time stamps, devices (mobile or desktop) and env, and other few things. The table is connected with the visualization tool as the script run every four hours and saves the result into the database so the visualization tool shows the cumulative result for comparison. 

There is another outfile of this script which is a json file for every web page. This is will created in the same directory with same environment all the webpages will be saved in the environment folder. In this file, you can find detail information from the webpage along with core web vitals. 

# How to run (locally):

A configuration file that includes the below-listed variables.

```
{
    "host": "",
    "database": "",
    "user": "",
    "port" : "",
    "password": "",
    "apikey" : "&key="
}
```

This file will not be found in the repo you may need to ask someone from QA or DevOps team. 

Secondly, on your local machine, you have running connection with MariaDB through DBeaver, for example and you should created a SSH tunnel like this

```
ssh -fN -L 3307:127.0.0.1:3306 username@bi-02.tcsrv.net 
```

Please get your credentials from DevOps team

# Dependencies 

- Python 3 (latest version)
- juypter notebook (for editing) 
- DBviewer (please ask DevOps team for credentials and other things to connect BI-02)
- SSH key (please ask DevOps team or Adrian)

# CI/CD setup:

TODO
