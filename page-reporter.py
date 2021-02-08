import requests
import argparse
import sys
import os
import json
import time

""" Functions Start """

# Pagespeed Insight Function - takes the requesting URL as a parameter
def process_api_call(u):

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
        overall_score = round(final["lighthouseResult"]["categories"]["performance"]["score"] * 100)
        overall_score_2 = str(overall_score)

        # First Contentful Paint
        fcp = round(final["lighthouseResult"]["audits"]["first-contentful-paint"]["score"] * 100)
        fcp2 = str(fcp)

        # Speed Index
        si = round(final["lighthouseResult"]["audits"]["speed-index"]["score"] * 100)
        si2 = str(si)

        # Largest Contentful Paint
        lcp = round(final["lighthouseResult"]["audits"]["largest-contentful-paint"]["score"] * 100)
        lcp2 = str(lcp)

        # Time To Interactive
        tti = round(final["lighthouseResult"]["audits"]["interactive"]["score"] * 100)
        tti2 = str(tti)        

        # Total Blocking Time
        tbt = round(final["lighthouseResult"]["audits"]["total-blocking-time"]["score"] * 100)
        tbt2 = str(tbt)

        # Cumulative Layout Shift
        ls = round(final["lighthouseResult"]["audits"]["cumulative-layout-shift"]["score"] * 100)
        ls2 = str(ls)

    except KeyError:
        print(f'<KeyError> One or more keys not found {line}.')
    
    # Writing output to CSV file
    try:
        row = f'{ID2},{test_type},{overall_score_2},{fcp2},{si2},{lcp2},{tti2},{tbt2},{ls2}\n'
        file.write(row)
    except NameError:
        print(f'<NameError> Failing because of KeyError {line}.')
        file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')


# Lighthouse function - runs Lighthouse node module
def process_lighthouse(link):
    os.popen(link)
    
    # Check if report is completed, if not, then wait until it's finished. 
    while not os.path.exists('./lighthouse_report.json'):
        time.sleep(30)
    
    if os.path.isfile('./lighthouse_report.json'):

    with open('./lighthouse_report.json', 'r', encoding='utf8') as json_data:
        loaded_json = json.load(json_data)
                
        # Calculating if test is for mobile or desktop
        if '--form-factor="mobile"' in link:
            lh_type = "Mobile"
        else:
            lh_type = "Desktop"
        
        # Getting scores
        lh_url = str(line)
        lh_performance = str(round(loaded_json["categories"]["performance"]["score"] * 100))
        lh_seo = str(round(loaded_json["categories"]["seo"]["score"] * 100))
        lh_accessibility = str(round(loaded_json["categories"]["accessibility"]["score"] * 100))
        lh_best_practice = str(round(loaded_json["categories"]["best-practices"]["score"] * 100))
        lh_fcp = str(round(loaded_json["audits"]["first-contentful-paint"]["score"] * 100))
        lh_speed_index = str(round(loaded_json["audits"]["speed-index"]["score"] * 100))
        lh_lcp = str(round(loaded_json["audits"]["largest-contentful-paint"]["score"] * 100))
        lh_interactice = str(round(loaded_json["audits"]["interactive"]["score"] * 100))
        lh_tbt = str(round(loaded_json["audits"]["total-blocking-time"]["score"] * 100))
        lh_cls = str(round(loaded_json["audits"]["cumulative-layout-shift"]["score"] * 100))

        try:
            row = f'{lh_url},{lh_type},{lh_performance},{lh_accessibility},{lh_best_practice},{lh_seo},{lh_fcp},{lh_speed_index},{lh_lcp},{lh_interactice},{lh_tbt},{lh_cls}\n'
            file.write(row)
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')
            file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')
    
    # Delete Lighthouse Report to prevent conflict between reports
    os.remove('./lighthouse_report.json')

""" Functions End """

# Setting up arguments for script
parser = argparse.ArgumentParser(description='Pagespeed Insight API script')
parser.add_argument("-m", "--mobile", action="store_true", help="Run mobile only test\n")
parser.add_argument("-d", "--desktop", action="store_true", help="Run desktop only test\n")

args = parser.parse_args()

# Pagespeed API Key
pagespeed_key = os.environ['pagespeed']

# Writing to CSV
with open('urls.txt') as pagespeedurls:
    download_dir = 'pagespeed-report.csv'
    file = open(download_dir, 'w+')
    content = pagespeedurls.readlines()
    content = [line.rstrip('\n') for line in content]

    columnTitleRow = "URL, Mobile/Desktop, Overall Score, First-Contentful-Paint, Speed Index, Largest-Contentful-Paint, Time-To-Interactive, Total-Blocking-Time, Cumulative-Layout-Shift\n"
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

# Writing to lighthouse CSV
with open('urls.txt') as lighthouseurls:
    download_dir = 'lighthouse-report.csv'
    file = open(download_dir, 'w+')
    content = lighthouseurls.readlines()
    content = [line.rstrip('\n') for line in content]

    columnTitleRow = "URL, Mobile/Desktop, Performance, Accessibility, Best-Practices, SEO, First-Contentful-Paint, Speed-index, Largest-Contentful-Paint, Interactive, Total-Blocking-Time, Cumulative-Layout-Shift\n"
    file.write(columnTitleRow)

    for line in content:

         # Run through parameters
        if args.desktop:
            lh_x = 'lighthouse '+line+' --only-categories="accessibility,best-practices,performance,seo" --quiet --chrome-flags="--headless" --output=json --output-path=./lighthouse_report.json --form-factor="desktop"'

        elif args.mobile:
            lh_x = 'lighthouse '+line+' --only-categories="accessibility,best-practices,performance,seo" --quiet --chrome-flags="--headless" --output=json --output-path=./lighthouse_report.json --form-factor="mobile" --screenEmulation.mobile --screenEmulation.width=360 --screenEmulation.height=640 --screenEmulation.deviceScaleFactor=2'
            
        # Check for both flag, this will run as default if one is not set.
        else:
            lh_x = ['lighthouse '+line+' --only-categories="accessibility,best-practices,performance,seo" --quiet --chrome-flags="--headless" --output=json --output-path=./lighthouse_report.json', 'lighthouse '+line+' --only-categories="accessibility,best-practices,performance,seo" --quiet --chrome-flags="--headless" --output=json --output-path=./lighthouse_report.json --form-factor="mobile" --screenEmulation.mobile --screenEmulation.width=360 --screenEmulation.height=640 --screenEmulation.deviceScaleFactor=2']

        # If statement for processing mobile, desktop or both lighthouse reports.
        if len(lh_x) == 2:
            for lh_url in lh_x:
                process_lighthouse(lh_url)
        else: 
            process_lighthouse(lh_x)

    file.close()
print("Reports have been generated!")