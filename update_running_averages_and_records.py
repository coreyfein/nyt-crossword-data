import helpers
import requests
import json
import os
from dotenv import load_dotenv

# def update_running_best_times(airtable_records_for_day_of_week_view):
#     try:
#         running_best_time = False
#         for i, record in enumerate(airtable_records_for_day_of_week_view):
#             solve_time = record["fields"]["Solve Time"]# in seconds -- this is what the Record for Day of Week as of Date field expects as data input
#             record_id = record["id"]
#             date = record["fields"]["Date"]
#             if running_best_time == False or running_best_time > solve_time:
#                 running_best_time = solve_time
#                 payload = {'fields':{'Record for Day of Week as of Date': running_best_time, 'Set Record for Day of Week': 1}}
#             else:
#                 payload = {'fields':{'Record for Day of Week as of Date': running_best_time}}
#             payload = json.dumps(payload)
#             response = helpers.update_airtable_record(AIRTABLE_API_TOKEN, AIRTABLE_CROSSWORD_DATA_BASE_ID, AIRTABLE_CROSSWORD_TIMES_TABLE_ID, record_id, payload)
#             print(f"Updated best times as of {date}")
#         success_updating_best_times = True
#     except:
#         success_updating_best_times = False

#     return success_updating_best_times

# def update_running_averages(airtable_records_for_day_of_week_view):
#     try:
#         running_total_time = 0.0
#         for i, record in enumerate(airtable_records_for_day_of_week_view):
#             day_number = i + 1
#             record_id = record["id"]
#             date = record["fields"]["Date"]
#             solve_time = record["fields"]["Solve Time"]# in seconds -- this is what the Running Average For Day of Week field expects as data input
#             running_total_time += solve_time
#             print(running_total_time)
#             running_average = running_total_time / day_number
#             payload = json.dumps({'fields':{'Running Average for Day of Week': running_average}})
#             response = helpers.update_airtable_record(AIRTABLE_API_TOKEN, AIRTABLE_CROSSWORD_DATA_BASE_ID, AIRTABLE_CROSSWORD_TIMES_TABLE_ID, record_id, payload)
#             print(f"Updated running average as of {date}")
#             day_number += 1
#         success_updating_running_averages = True
#     except:
#         print("Error occurred")
#         success_updating_running_averages = False
#     return success_updating_running_averages

def update_running_averages(i, record_id, date, solve_time, running_total_time):
    day_number = i + 1     
    running_total_time += solve_time
    running_average = running_total_time / day_number
    payload = json.dumps({'fields':{'Running Average for Day of Week': running_average}})
    response = helpers.update_airtable_record(AIRTABLE_API_TOKEN, AIRTABLE_CROSSWORD_DATA_BASE_ID, AIRTABLE_CROSSWORD_TIMES_TABLE_ID, record_id, payload)
    print(f"Updated running average as of {date}")

    return running_total_time, running_average

def update_running_best_times(record_id, date, solve_time, running_best_time):
    if running_best_time == False or running_best_time > solve_time:
        print("new record today")
        running_best_time = solve_time
        payload = {'fields':{'Record for Day of Week as of Date': running_best_time, 'Set Record for Day of Week': True}}
    else:
        payload = {'fields':{'Record for Day of Week as of Date': running_best_time}}
    print(f"running_best_time: {running_best_time}")
    payload = json.dumps(payload)
    response = helpers.update_airtable_record(AIRTABLE_API_TOKEN, AIRTABLE_CROSSWORD_DATA_BASE_ID, AIRTABLE_CROSSWORD_TIMES_TABLE_ID, record_id, payload)
    print(f"Updated best times as of {date}")

    return running_best_time

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
            running_total_time, running_average = update_running_averages(i, record_id, date, solve_time, running_total_time)
            running_best_time = update_running_best_times(record_id, date, solve_time, running_best_time)
            
        # success_updating_running_averages = update_running_averages(airtable_records_for_day_of_week_view)
        # print(f"success_updating_running_averages: {success_updating_running_averages}")
        # success_updating_best_times = update_running_best_times(airtable_records_for_day_of_week_view)
        # print(f"success_updating_best_times: {success_updating_best_times}")

if __name__ == "__main__":
    load_dotenv()
    AIRTABLE_API_TOKEN = os.getenv("AIRTABLE_CROSSWORD_STATS_TOKEN")
    AIRTABLE_CROSSWORD_DATA_BASE_ID = os.getenv("AIRTABLE_CROSSWORD_DATA_BASE_ID")
    AIRTABLE_CROSSWORD_TIMES_TABLE_ID = os.getenv("AIRTABLE_CROSSWORD_TIMES_TABLE_ID")
    main()