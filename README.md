# pagespeed-insight
Runs Googles Pagespeed insight report mobile, desktop or both across a list of URLs. 

## To run:
Clone the repo

CD into the directory

Update the urls.txt with each url on their own line.

### Command Usage:
Be default, the command will run both mobile and desktop tests. If you only want to run either mobile or desktop, then use the approperiate flags. 

`python ./pagespeed-insight.py`

```
optional arguments:
  -h, --help     show this help message and exit
  -m, --mobile   Run mobile only test
  -d, --desktop  Run desktop only test
  -b, --both     Run both mobile and desktop
```
  
  Once this is finished, you should see a CSV that's been created at the root of the project file with the URLs, type of test and the scores from the pagespeed insight report. 
