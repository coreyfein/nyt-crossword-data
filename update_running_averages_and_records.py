import helpers
import requests
import json
import os
from dotenv import load_dotenv

def get_running_average(i, solve_time, running_total_time):
    day_number = i + 1     
    running_total_time += solve_time
    running_average = running_total_time / day_number
    return running_total_time, running_average

def get_running_best_time(solve_time, running_best_time):
    if running_best_time == False or running_best_time > solve_time:
        print("new record today")
        running_best_time = solve_time
        set_record_for_day_of_week = True
    else:
        set_record_for_day_of_week = False
    
    print(f"running_best_time: {running_best_time}")
    return running_best_time, set_record_for_day_of_week

def main():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        airtable_records_for_day_of_week_view = helpers.get_airtable_records_in_view(AIRTABLE_API_TOKEN, AIRTABLE_CROSSWORD_DATA_BASE_ID, AIRTABLE_CROSSWORD_TIMES_TABLE_ID, view=day)
        running_total_time = 0.0
        running_best_time = False
        for i, record in enumerate(airtable_records_for_day_of_week_view):
            record_id = record["id"]
            date = record["fields"]["Date"]
            print(f"date: {date}")
            solve_time = record["fields"]["Solve Time"]# in seconds -- this is what other duration fields expect  
            running_total_time, running_average = get_running_average(i, solve_time, running_total_time)
            running_best_time, set_record_for_day_of_week = get_running_best_time(solve_time, running_best_time)
            payload = {'fields':{'Running Average for Day of Week': running_average, 'Record for Day of Week as of Date': running_best_time, 'Set Record for Day of Week': set_record_for_day_of_week}}
            payload = json.dumps(payload)
            response = helpers.update_airtable_record(AIRTABLE_API_TOKEN, AIRTABLE_CROSSWORD_DATA_BASE_ID, AIRTABLE_CROSSWORD_TIMES_TABLE_ID, record_id, payload)
            print(f"Updated running average and best times as of {date}")

if __name__ == "__main__":
    load_dotenv()
    AIRTABLE_API_TOKEN = os.getenv("AIRTABLE_CROSSWORD_STATS_TOKEN")
    AIRTABLE_CROSSWORD_DATA_BASE_ID = os.getenv("AIRTABLE_CROSSWORD_DATA_BASE_ID")
    AIRTABLE_CROSSWORD_TIMES_TABLE_ID = os.getenv("AIRTABLE_CROSSWORD_TIMES_TABLE_ID")
    # AIRTABLE_CROSSWORD_TIMES_TABLE_ID = os.getenv("AIRTABLE_CROSSWORD_TIMES_TESTING_TABLE_ID")
    main()