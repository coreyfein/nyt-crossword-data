# What is this?

This set of scripts is meant to be run on a local machine in Terminal. Together, you can use them to:

1. Scrape your crossword solve times from New York Times Games and export as a CSV. 
2. Calculate running averages and solve time records for each day within a given time frame. Running averages and solve time records are calculated/stored for each day of the week separately (e.g. Monday will have its own set of running averages and solve time records). The data will then populate / update in Airtable, so that you can easily see how your running solve time average has changed over time (hopefully trending downwards!) and when new records were set. 

## Setup

You'll need:

- Google Chrome
- Python 3.9+ with requirements installed
- New York Times Games subscription
- Apple ID with the same email address as your NYT Games subscription (for login purposes only -- you can't login to NYT with username/password directly when running Selenium)
- Airtable (If you only want to scrape your solve times and export as a CSV, Airtable is options. If you want to calculate/store running averages and records, you'll need it)

## Requirements

After cloning the repo, install requirements with:

    pip install -r requirements.txt

As you update Chrome, you'll probbably need to upgrade Selenium:

    pip install selenium --upgrade

Upgrade Selenium if you see an error like this:

    selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 114
    Current browser version is 116.0.5845.179 with binary path /Applications/Google Chrome.app/Contents/MacOS/Google Chrome

## A Note on Scraped Solve Time Data

After running the script to scrape your solve time data (see next section), you'll end up with a CSV with two columns: date, solve_time. 

After the CSV is exported, search for solve times starting with `0:` -- those are either puzzles you haven't solved, or days where the script failed to properly scrape the data (you'll see that for a small minority of puzzles, the browser fails to log you in before scraping the data, and so it exports a time of just a few seconds since that's what the clock element reads). You can quickly check each of those days manually in a browser and then plug in the actual time (if you solved it) or delete the row (if you didn't solve it). Here's the URL for September 3, 2023, for example:

https://www.nytimes.com/crosswords/game/daily/2023/09/03

When I ran this on an almost 2 year period, there were roughly 20 days I needed to look up manually, so I decided not to spend time on a more elegant solution. (Almost always, the first day in the range given does not work properly.)

## Getting Solve Time Data

Run get_crossword_stats.py

When prompted, enter date range you'd like to get solve time data for.

Chrome will open up to a login page. Select "Continue with Apple." (If you try to login normally, it will detect that a "robot" is trying to login. Google login also does not seem to work, and I didn't try Facebook since Apple works.)

In the popup window, enter your Apple ID -- it must be the same email address that you use for your NYT Games subscription. If it has not been linked yet, you'll be asked if you want to link it (say yes).

Enter your Apple password, and then the security code (assuming it requires two-factor login for everyone).

When asked, select "Trust" to trust the browser and keep you logged in while the script runs.

Select "Continue" to complete the login. The popup window should close, and the main Chrome window should redirect to the puzzle for first date in your date range.

You can follow progress in Terminal -- a dictionary with all solve times retrieved will print as each day's time is retrieved. 

The CSV will be saved in the same directory as the script. 

Selenium can be pretty slow. After logging in, the script sometimes takes 15 - 45 seconds per puzzle on my computer. Keeping the Selenium window as the active window and not doing anything else while it runs seems to help speed things up. If you're running it for a large time frame, make sure your computer won't go to sleep. The CSV is updated for each puzzle that's scraped, so if the script does crash, you can rename the CSV for the correct date range and then pick up where it left off when you run it again.








