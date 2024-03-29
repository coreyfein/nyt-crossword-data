# What is this?

This set of scripts is meant to be run on your local machine. Together, you can use them to:

1. Scrape your crossword solve times from New York Times Games and export as a CSV. 
2. Calculate running averages and solve time records for each day within a given time frame. Running averages and solve time records are calculated/stored for each day of the week separately (e.g. Monday will have its own set of running averages and solve time records). You can choose to calculate and store this data locally (exported as a CSV), or calculate and store in Airtable so that you can easily see how your running solve time average has changed over time (hopefully trending downwards!) and when new records were set. 

## Setup

You'll need:

- Google Chrome
- Python 3.9+ with requirements installed
- New York Times Games subscription
- Apple ID or Facebook account with the same email address as your NYT Games subscription (for login purposes only -- you can't login to NYT with username/password directly when running Selenium)
- Airtable (Optional -- if you want to use something else to visualize your data, you don't need Airtable)

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

When prompted, enter the date range you'd like to get solve time data for.

A new Chrome window will open up to a login page. Let it load fully, then click either "Continue with Apple" or "Continue with Facebook." (If you try to login normally, it will detect that a "robot" is trying to login. Google login also does not seem to work.)

In the popup window, follow the prompts to enter your Apple or Facebook login credentials. This may include Two-Factor Authentication.

If asked, select "Trust" to trust the browser and keep you logged in while the script runs.

After you complete the login, close the popup window if it doesn't close automatically. 

The main Chrome window should redirect to the puzzle for the first date in your date range. You can follow progress in Terminal -- a dictionary with all solve times retrieved will print as each day's time is retrieved. 

The CSV will be saved in the same directory as the script. 

Selenium can be pretty slow. After logging in, the script usually takes 15 - 45 seconds per puzzle, though this will vary by machine. Keeping Selenium's Chrome window as the active window and not doing anything else while it runs seems to help speed things up. If you've entered a wide date range, make sure your computer won't go to sleep. However, the CSV is updated and saved after each puzzle that's scraped, so if the script does crash, you can rename the CSV for the correct date range and then pick up where it left off when you run it again.

## Calculating Running Solve Time Averages and Records

Before calculating your running solve time averages and records, make sure to finalize your solve time data (see [A Note on Scraped Solve Time Data](#a-note-on-scraped-solve-time-data)).

If you want to calculate your running solve time averages and records and store them locally, just run calculate_running_averages_and_records_to_csv.py -- that will export a CSV with all the data.

If you want to store your running solve time averages and records in Airtable, first complete the steps below (in "Airtable Setup"), and then run calculate_running_averages_and_records_airtable.py.

(Note: Airtable's free plan only allows 1,000 API calls per month. calculate_running_averages_and_records_airtable.py makes one call per hundred records (days) in your table to retrieve the records, then one call per record (day) to update the data.)

## Airtable Setup

Duplicate .env.example and rename it just .env

In Airtable, create a new base called Crossword Data. Open the base in your browser and take a look at the URL. The string after the first slash (starting with "app") is the base ID. Copy that and paste it in your .env file after AIRTABLE_CROSSWORD_DATA_BASE_ID=

Name your first table "Crossword Times" and take a look at the URL again. The string after the second slash (starting with "tbl") is the table ID. Copy that and paste it in your .env file after AIRTABLE_CROSSWORD_TIMES_TABLE_ID=

Delete any default fields and add the following fields to the Crossword Times table. 

1. "Date" (Date field). Date format should be ISO.
2. "Day of Week" (Formula field). The formula is:
    DATETIME_FORMAT({Date}, "dddd")
3. "Solve Time" (Duration field). Duration format: h:mm:ss
4. "Solve Time (Minutes)" (Formula field). The formula is:
    {Solve Time}/60
5. "Running Average for Day of Week" (Duration field). Duration format: h:mm:ss
6. "Record for Day of Week as of Date" (Duration field). Duration format: h:mm:ss
7. "Record for Day of Week as of Date (Minutes)" (Formula field). The formula is:
    {Record for Day of Week as of Date}/60
8. "Set Record for Day of Week" (Checkbox field)
9. "Running Average for Day of Week (Minutes)" (Formula field). The formula is:
    {Running Average for Day of Week}/60

Next, in the table:

- Sort by Date 1->9 (and toggle on "Automatically sort records")

- When you're done, it should look like this: https://airtable.com/apptu1Hkm1AyIcVdh/shrxTFmTCtajkXwmt

- Duplicate Grid view and rename it "Monday"

- Add a filter: Where Day of Week is Monday

- Duplicate that view, rename it "Tuesday" and then edit the filter for Tuesday. Repeat for each day of the week.

Now, go to https://airtable.com/create/tokens and create a new token with the following scopes:

- data.records:read
- data.records:write

Copy the token and paste it in your .env file after AIRTABLE_CROSSWORD_STATS_TOKEN=

You're now all set up. You will be able to paste in solve time data into the "Date" and "Solve Time" fields after running get_crossword_stats.py (see previous sections), and then calculate/store running averages and records by running update_running_averages_and_records.py (see next section).

## Visualizing the data in Airtable

Once you have the data, you can use Airtable or whatever software you prefer to visualize it. Here's how to graph some basic trends in Airtable.

(Note: Airtable's free plan only allows one extension per table. If you don't want to pay for it, you'll need to re-enter parameters every time you want to view a different trend.)

1. Click "Extensions" at the top right of the table
2. Click "Add an extension"
3. Choose "Chart"
4. Select a day of the week from the View dropdown
5. Select "Line" as your chart type
6. Select "Date" for your X-axis
7. Select "Field" for Y-axis, then select the field "Running Average for Day of Week (Minutes)

You should end up with a graph that looks like this: 

![Monday Solve Time Running Average](graphs/monday_running_average.png)
<h3 align="center">Monday Solve Time Running Average</h3>

</br>
And here's a simple way to visualize how your solve time record improved over time: in the extension, under Field, change the field to "Record for Day of Week as of Date (Minutes)"

![Monday Solve Time Records](graphs/monday_records.png)
<h3 align="center">Monday Solve Time Records</h3>






