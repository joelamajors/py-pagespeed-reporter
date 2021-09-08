import requests
import os
import argparse
import json
import time
import concurrent.futures
import re
import subprocess

# Generate CSV data for lighthouse results
def lighthouse_csv_report(path):

    # Calculating if query is for mobile or desktop
    if '/lighthouse-reports/mobile' in path:
        lh_type = "Mobile"
    else:
        lh_type = "Desktop"

    with open(path, 'r', encoding='utf8') as json_data:

        loaded_json = json.load(json_data)

        # Getting scores
        lh_url = str(loaded_json["requestedUrl"])

        # Page Name
        reg_page_name = re.search('[^/]+(?=/$|$)', lh_url)
        page_name = reg_page_name.group(0)

        if page_name == domain_name:
            page_name = "home"


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
            row = f'{lh_url},{page_name},{lh_type},{lh_performance},{lh_accessibility},{lh_best_practice},{lh_seo},{lh_fcp},{lh_speed_index},{lh_lcp},{lh_interactice},{lh_tbt},{lh_cls}\n'
            lh_csv_base.write(row)
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')
            lh_csv_base.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')

# Generate CSV data for pagespeed results
def pagespeed_csv_report(path):

    # Calculating if query is for mobile or desktop
    if '/pagespeed-reports/mobile' in path:

        ps_type = "Mobile"
    else:
        ps_type = "Desktop"

    with open(path, 'r', encoding='utf8') as json_data:

        loaded_json = json.load(json_data)

        # Getting URL
        if '?strategy=desktop' in loaded_json['id']:
            ID2 = loaded_json['id']
            ID2 = ID2.replace('?strategy=desktop', '')

        elif '?strategy=mobile' in loaded_json['id']:
            ID2 = loaded_json['id']
            ID2 = ID2.replace('?strategy=mobile', '')

        # Page Name
        reg_page_name = re.search('[^/]+(?=/$|$)', ID2)
        page_name = reg_page_name.group(0)


        if page_name == domain_name:
            page_name = "home"

        # Overall Score
        overall_score = round(loaded_json["lighthouseResult"]["categories"]["performance"]["score"] * 100)
        overall_score_2 = str(overall_score)

        # First Contentful Paint
        fcp = round(loaded_json["lighthouseResult"]["audits"]["first-contentful-paint"]["score"] * 100)
        fcp2 = str(fcp)

        # Speed Index
        si = round(loaded_json["lighthouseResult"]["audits"]["speed-index"]["score"] * 100)
        si2 = str(si)

        # Largest Contentful Paint
        lcp = round(loaded_json["lighthouseResult"]["audits"]["largest-contentful-paint"]["score"] * 100)
        lcp2 = str(lcp)

        # Time To Interactive
        tti = round(loaded_json["lighthouseResult"]["audits"]["interactive"]["score"] * 100)
        tti2 = str(tti)

        # Total Blocking Time
        tbt = round(loaded_json["lighthouseResult"]["audits"]["total-blocking-time"]["score"] * 100)
        tbt2 = str(tbt)

        # Cumulative Layout Shift
        ls = round(loaded_json["lighthouseResult"]["audits"]["cumulative-layout-shift"]["score"] * 100)
        ls2 = str(ls)

        # Writing output to CSV file
        try:
            row = f'{ID2},{page_name},{ps_type},{overall_score_2},{fcp2},{si2},{lcp2},{tti2},{tbt2},{ls2}\n'
            ps_csv_base.write(row)
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')
            ps_csv_base.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')

# Generates sub folders for reports
def create_sub_folders(name):

    # Creating folders for data dump
    if not os.path.exists(name+"/lighthouse-reports"):
        os.makedirs(name+"/lighthouse-reports/desktop")
        os.makedirs(name+"/lighthouse-reports/mobile")

    if not os.path.exists(name+"/pagespeed-reports/"):
        os.makedirs(name+"/pagespeed-reports/desktop")
        os.makedirs(name+"/pagespeed-reports/mobile")

# Pagespeed Insight Function - takes the requesting URL as a parameter
def link_queries(link, output_name):

    # Append pagespeed query to link
    key = "&key="+pagespeed_key

    pagespeed_desktop = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+link+'?strategy=desktop'+key
    pagespeed_mobile = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='+link+'?strategy=mobile'+key

    pagespeed_links.add(pagespeed_desktop)
    pagespeed_links.add(pagespeed_mobile)

    # Desktop and mobile parameters for lighthouse reports
    lighthouse_desktop = (f'lighthouse {link} --only-categories="accessibility,best-practices,performance,seo" --quiet --chrome-flags="--headless" --output=json --output-path="{folder_name}/lighthouse-reports/desktop/{output_name}-desktop.json" 2>&1')

    lighthouse_mobile = (f'lighthouse {link} --only-categories="accessibility,best-practices,performance,seo" --quiet --chrome-flags="--headless" --output=json --output-path="{folder_name}/lighthouse-reports/mobile/{output_name}-mobile.json" --form-factor="mobile" --screenEmulation.mobile --screenEmulation.width=360 --screenEmulation.height=640 --screenEmulation.deviceScaleFactor=2 2>&1')

    lighthouse_links.add(lighthouse_desktop)
    lighthouse_links.add(lighthouse_mobile)

# Downloading Lighthouse JSON files
def lighthouse_data(link):

    process = subprocess.Popen(link, shell=True, stdout=subprocess.PIPE)
    process.wait()

# Downloading Pagespeed insight JSON files
def pagespeed_data(link):

    # Extract for getting URLs
    pagespeed_link_extract = re.search('(?<=url=)https?://.*(?=\?)', link)

    # Selector we use for accessing this
    parsed_link_extract = pagespeed_link_extract.group(0)

    # From the selector, do another Regex query
    pagespeed_page_extract = re.search('[^/]+(?=/$|$)', parsed_link_extract)

    # name of page
    pagespeed_file_name = pagespeed_page_extract.group(0)


    if pagespeed_file_name == domain_name:
        pagespeed_file_name = 'home'

    r = requests.get(link)
    final = r.json()

    # Check if request is for Mobile or Desktop
    if '?strategy=mobile' in link:
        test_type = "Mobile"

    else:
        test_type = "Desktop"

    # Paths for data dump
    pagespeed_path = "./"+folder_name+"/pagespeed-reports/"+test_type.lower()+"/"+pagespeed_file_name+"-"+test_type.lower()+".json"

    # Saving JSON file
    with open(pagespeed_path, "w+") as pagespeed_json_file:
        json.dump(final, pagespeed_json_file)


# Pagespeed API Key
pagespeed_key = os.environ['pagespeed']

# Storing links
pagespeed_links = set()
lighthouse_links = set()

# Variables to store paths to JSON files
lighthouse_csvs = set()
pagespeed_csvs = set()

# Cleans up terminal output
spaces = ' ' * 40

# Getting file name to save data dumps to
with open("urls.txt") as f:

    # Getting folder name, and checks
    name = f.readlines()

    folder_name = name[0]

    # Getting domain name, used for conditional to tell if this is the home page or not.
    domain_name = re.compile('https?://([A-Za-z_0-9.-]+).*')
    domain_name = domain_name.match(folder_name).group(1)

    # File name, which is the name of the client/site
    reg_folder_name = re.compile('(.*.//)([a-z]*)')
    folder_name = reg_folder_name.match(folder_name).group(2)

    # If directory doesn't exist, make it
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    # function to create sub folders
    create_sub_folders(folder_name)

    content = f.readlines()
    name = [line.rstrip('\n') for line in name]

    for line in name:

        reg_output_name = re.search('[^/]+(?=/$|$)', line)

        # Used to save the reports as the page name
        output_name = reg_output_name.group(0)

        # If the output name matches the domain name, then this is the home page
        if output_name == domain_name:
            output_name = 'home'

        # Calls function to add links to sets
        link_queries(line, output_name)

print(f" Generating Lighthouse JSON files..." + spaces, end="\r")

# Threading lighthouse report with the lighthouse_data() function
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(lighthouse_data, lighthouse_links)


print(f" Generating Pagespeed Insight JSON files..."  + spaces, end="\r")

# Threading pagespeed insight report with the pagespeed_data() function
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(pagespeed_data, pagespeed_links)


# Parase through JSON files and add them to set. We will use the set to run through each JSON file and update the CSV report
for paths, subdirs, files in os.walk(folder_name, topdown=False):

   # For each file, if it's a .json file, add this to the correct set.
   for name in files:
        full_path = os.path.join(paths, name)

        # if the file path is
        if 'lighthouse-reports' in full_path:
           lighthouse_csvs.add(full_path)

        else:
            pagespeed_csvs.add(full_path)

# Creating CSV for Lighthouse.
with open(folder_name+'/lighthouse-reports/lighthouse_report.csv', 'w+') as lh_csv_base:
    columnTitleRow = "URL, Page, Mobile/Desktop, Performance, Accessibility, Best-Practices, SEO, First-Contentful-Paint, Speed-index, Largest-Contentful-Paint, Interactive, Total-Blocking-Time, Cumulative-Layout-Shift\n"
    lh_csv_base.write(columnTitleRow)

    #Threading to generate Lighthouse results
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lighthouse_csv_report, lighthouse_csvs)


# Creating CSV for Pagespeed.
with open(folder_name+'/pagespeed-reports/pagespeed_report.csv', 'w+') as ps_csv_base:
    columnTitleRow = "URL, Page, Mobile/Desktop, Overall Score, First-Contentful-Paint, Speed Index, Largest-Contentful-Paint, Time-To-Interactive, Total-Blocking-Time, Cumulative-Layout-Shift\n"
    ps_csv_base.write(columnTitleRow)

    #Threading to generate Pagespeed CSV results
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(pagespeed_csv_report, pagespeed_csvs)

print(""*3)
print(" Reports have been generated!")
