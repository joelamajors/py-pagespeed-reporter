# Pagespeed-reporter
This script runs Pagespeed insight AND Lighthouse reports across a list of URLs. These reports will be saved in a CSV under the `sitename` folder under this repo. In addition, all JSON files are now stored there as well.



## Requirements
- Python 3
- Pagespeed Insights API key
  - (Refer to this link on getting started (https://developers.google.com/speed/docs/insights/v5/get-started)
- Add API key to environment variable
  - The variable name should be stored as `pagespeed`.
- Lighthouse npm installed globally
  - run `npm install -g lighthouse`

## First Time Use:
- Clone the repo

- CD into the directory

- Create virtual environment
  - `python3 -m venv venv`

- Activate virtual environment
  - Windows `venv/script/activate`
  - Mac/Linux `source venv/bin/activate`

- Run `pip3 install -r requirements.txt`

- Update the urls.txt with each url on their own line.

- Run (See Command Usage)


## Running after you've installed
- Activate virtual environment
  - Windows `venv/script/activate`
  - Mac/Linux `source venv/bin/activate`

- Update the urls.txt with each url on their own line.

- Run (See Command Usage)


### Command Usage:
`python3 ./py-pagespeed-reports.py`

or if `python` is your version 3.x

`python ./py-pagespeed-reports.py`

Once this is finished, you will see a folder generated with the site name, and sub folders for lighthouse and pagespeed. Inside each folder will be the .CSV report. 
