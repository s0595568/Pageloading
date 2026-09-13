#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import os
from binascii import a2b_base64
from pathlib import Path
from urllib.parse import urlparse
from urllib import request
import pandas as pd
import traceback
from datetime import date
import mysql.connector
from mysql.connector import Error

#with open('config.json') as json_file:
#    dbConfig = json.load(json_file)

#strategies = ['desktop', 'mobile']
#apikey = dbConfig['apikey']
import os

dbConfig = {
    'host': os.environ['MARIADB_HOST'],
    'database': os.environ.get('MARIADB_DATABASE', 'QA'),
    'user': os.environ['MARIADB_USER'],
    'port': os.environ.get('MARIADB_PORT', '3307'),
    'password': os.environ['MARIADB_PASSWORD'],
}

strategies = ['desktop', 'mobile']
apikey = '&key=' + os.environ['PAGESPEED_API_KEY']

today = str(date.today())

from datetime import datetime


# In[2]:


def savetoFile(lhtest, summary, url, timestampStr):
    urlelements = urlparse(url)
    domainp = urlelements.netloc
    path = urlelements.path
    if not path.endswith('/'):
        path = path + '/'
    basepath = os.getcwd() + "/testresults/" + domainp + path
    filename = basepath + f'{timestampStr}.json'
    result = Path(basepath +f'{timestampStr}.json')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    timestampfilename = timestampStr.replace(":", "-")
    with open(basepath + f'{timestampfilename}-{strategy}.json', 'w+') as re:
        imptMat = {"loadingExperience":lhtest["loadingExperience"],
                   "originLoadingExperience":lhtest["originLoadingExperience"],
                   "summary" : summary};
        jsonstr = json.dumps(imptMat, ensure_ascii=False, indent=4)
        re.write(jsonstr)
        re.close()
        print(basepath + "results saved")


# In[3]:


def savetoDB(summary):
    connection = None
    try:
        connection = mysql.connector.connect(host=dbConfig['host'],
                                             database=dbConfig['database'],
                                             user=dbConfig['user'],
                                             port=dbConfig['port'],
                                             password=dbConfig['password'])
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("""INSERT into pagespeed (url, env, device, timestamp, overallperformancescore, fcp, fid, lcp, cls, fcp_score, fid_score, lcp_score, cls_score, inp, ttfb, tbt, si) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                               (summary['url'],
                                summary['env'],
                                summary['strategy'],
                                summary['timestamp'],
                                summary['OverallPerformanceScore'],
                                summary['fcp'],
                                summary['fid'],
                                summary['lcp'],
                                summary['cls'],
                                summary['fcp_score'],
                                summary['fid_score'],
                                summary['lcp_score'],
                                summary['cls_score'],
                                summary['inp'],
                                summary['ttfb'],
                                summary['tbt'],
                                summary['si']
                               ))
            connection.commit()
            print("data saved into table")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
            print("sql connection is closed")


# In[5]:


with open('urllist.json') as json_file:
    data = json.load(json_file)
    for strategy in strategies:
        for key, value in data.items():
            for url in value:
                f = '%Y-%m-%d %H:%M:%S'
                dateTimeObj = datetime.now()
                timestampStr = dateTimeObj.strftime(f)
                print("\nStart Lighthouse-Test for " + url)
                lhscores = []
                print("\nFetching results from api", url)
                x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={strategy}{apikey}'
                response = requests.get(x)
                lhtest = response.json()
                print(f"DEBUG - API response for {url}: {lhtest}")

                loadingExperience = lhtest.get("loadingExperience", {}).get("metrics", {})
                audits = lhtest.get("lighthouseResult", {}).get("audits", {})

                if lhtest.get('id', False):
                    summary = {
                        "url": lhtest["id"],
                        "OverallPerformanceScore": lhtest["lighthouseResult"]["categories"]["performance"]["score"] * 100,
                        "fcp": loadingExperience["FIRST_CONTENTFUL_PAINT_MS"]["percentile"] if "FIRST_CONTENTFUL_PAINT_MS" in loadingExperience else None,
                        "fid": loadingExperience["FIRST_INPUT_DELAY_MS"]["percentile"] if "FIRST_INPUT_DELAY_MS" in loadingExperience else None,
                        "lcp": loadingExperience["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"] if "LARGEST_CONTENTFUL_PAINT_MS" in loadingExperience else None,
                        "cls": loadingExperience["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100 if "CUMULATIVE_LAYOUT_SHIFT_SCORE" in loadingExperience else None,
                        "fcp_score": loadingExperience["FIRST_CONTENTFUL_PAINT_MS"]["category"] if "FIRST_CONTENTFUL_PAINT_MS" in loadingExperience else None,
                        "fid_score": loadingExperience["FIRST_INPUT_DELAY_MS"]["category"] if "FIRST_INPUT_DELAY_MS" in loadingExperience else None,
                        "lcp_score": loadingExperience["LARGEST_CONTENTFUL_PAINT_MS"]["category"] if "LARGEST_CONTENTFUL_PAINT_MS" in loadingExperience else None,
                        "cls_score": loadingExperience["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["category"] if "CUMULATIVE_LAYOUT_SHIFT_SCORE" in loadingExperience else None,
                        "inp": loadingExperience["EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT"]["percentile"] if "EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT" in loadingExperience else None,
                        "ttfb": loadingExperience["EXPERIMENTAL_TIME_TO_FIRST_BYTE"]["percentile"]/100 if "EXPERIMENTAL_TIME_TO_FIRST_BYTE" in loadingExperience else None,
                        "tbt": audits["total-blocking-time"]["score"] if "total-blocking-time" in audits else None,
                        "si": audits["speed-index"]["score"] if "speed-index" in audits else None,
                        "timestamp": timestampStr,
                        "strategy": strategy,
                        "env": key
                    }
                    savetoDB(summary)
                    savetoFile(lhtest, summary, url, timestampStr)
                else:
                    print(f"Skipped {url}: no 'id' in response — {lhtest}")


# In[ ]:
