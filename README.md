# What is this?

This set of scripts is meant to be run on a local machine in your Terminal. Together, you can use them to:

1. Scrape your crossword solve times from New York Times Games and export as a CSV. 
2. Calculate running averages and solve time records for each day within a given time frame. Running averages and solve times are calculated for each day of the week separately (e.g. Monday will have its own set of running averages). The running averages will then populate / update in Airtable, so that you can easily see how your running solve time average has changed over time (hopefully trending downwards!) and when new records were set. 

# Setup

You'll need:

- Google Chrome
- Python 3.9+ with requirements installed
- New York Times Games subscription
- Apple ID with the same email address as your NYT Games subscription (for login purposes only -- you can't login to NYT with username/password directly when running Selenium)
- Airtable (Optional if you only want to scrape your solve times to a CSV, but not calculate/store running averages and records.)

## Install requirements

After cloning the repo, install with:

    pip install -r requirements.txt

As you update Chrome, you'll probbably need to upgrade Selenium:

    pip install selenium --upgrade

Upgrade Selenium if you see an error like this:

    selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 114
    Current browser version is 116.0.5845.179 with binary path /Applications/Google Chrome.app/Contents/MacOS/Google Chrome







