import requests
import argparse
import sys
import os
import json

# Function to get info from API call, this takes the requesting URL as a parameter
def process_api_call(u):
    
    print(f'Requesting {str(u)}...')

    # Appending pagespeed key to end of URL
    r = requests.get(u+"&key="+pagespeed_key)
    final = r.json()

    try:
        # Getting URL
        ID2 = str(line)

        # URL of the page
        urlid = final['id']

        # Check if request is for Mobile or Desktop
        if '?strategy=mobile' in u:
            test_type = "Mobile"
        else: 
            test_type = "Desktop"

        # Overall Score
        overall_score = final["lighthouseResult"]["categories"]["performance"]["score"] * 100
        overall_score_2 = str(overall_score)

        # First Contentful Paint
        fcp = final["lighthouseResult"]["audits"]["first-contentful-paint"]["score"] * 100
        fcp2 = str(fcp)

        # Speed Index
        si = final["lighthouseResult"]["audits"]["speed-index"]["score"] * 100
        si2 = str(si)

        # Largest Contentful Paint
        lcp = final["lighthouseResult"]["audits"]["largest-contentful-paint"]["score"] * 100
        lcp2 = str(lcp)

        # Time To Interactive
        tti = final["lighthouseResult"]["audits"]["interactive"]["score"] * 100
        tti2 = str(tti)        

        # Total Blocking Time
        tbt = final["lighthouseResult"]["audits"]["total-blocking-time"]["score"] * 100
        tbt2 = str(tbt)

        # Cumulative Layout Shift
        ls = final["lighthouseResult"]["audits"]["cumulative-layout-shift"]["score"] * 100
        ls2 = str(ls)

        """ Additional results can be added here. """        

    except KeyError:
        print(f'<KeyError> One or more keys not found {line}.')
    
    # Writing output to CSV file
    try:
        row = f'{ID2},{test_type},{overall_score_2},{fcp2},{si2},{lcp2},{tti2},{tbt2},{ls2}\n'
        file.write(row)
    except NameError:
        print(f'<NameError> Failing because of KeyError {line}.')
        file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')


# Setting up arguments for script
parser = argparse.ArgumentParser(description='Pagespeed Insight API script')
parser.add_argument("-m", "--mobile", action="store_true", help="Run mobile only test\n")
parser.add_argument("-d", "--desktop", action="store_true", help="Run desktop only test\n")

args = parser.parse_args()

# Pagespeed API Key
pagespeed_key = os.environ['pagespeed']

# Writing to CSV
with open('urls.txt') as pagespeedurls:
    download_dir = 'pagespeed-results.csv'
    file = open(download_dir, 'w+')
    content = pagespeedurls.readlines()
    content = [line.rstrip('\n') for line in content]

    columnTitleRow = "URL, Mobile/Desktop, Overall Score, First Contentful Paint, Speed Index, Largest Contentful Paint, Time To Interactive, Total Blocking Time, Cumulative Layout Shift\n"
    file.write(columnTitleRow)

    # This is the google pagespeed API structure
    for line in content:
        
        # Removes trailing forward slash from link if it's there
        new_line = line.rstrip("/")
        line = line.replace(line, new_line)

        # Run through parameters
        if args.desktop:
            x = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+line+'?strategy=desktop'

        elif args.mobile:
            x = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+line+'?strategy=mobile'
            
        # Check for both flag, this will run as default if one is not set.
        else:
            x = ['https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+line+'?strategy=desktop','https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+line+'?strategy=mobile']

        # If statement to see if API is needed for mobile, desktop or both.
        if len(x) == 2:
            for url in x:
                process_api_call(url)
        else: 
            process_api_call(x)

    file.close()