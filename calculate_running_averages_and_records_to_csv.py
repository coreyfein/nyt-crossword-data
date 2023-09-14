import json
import csv
import helpers
from datetime import datetime, timedelta
from statistics import mean

def strip_leading_zeros_and_colons(time_to_strip):
    start_char = 0
    for char in time_to_strip:
        if char == "0" or char == ":":
            start_char += 1
        else:
            break

    return time_to_strip[start_char:]

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

def build_csv_rows(rows_pre_calculation):
    current_records_and_averages = {
        "Monday": {
            "record_seconds": None,
            "solve_times_seconds":[]
        },
        "Tuesday": {
            "record_seconds": None,
            "solve_times_seconds":[]
        },
        "Wednesday": {
            "record_seconds": None,
            "solve_times_seconds":[]
        },
        "Thursday": {
            "record_seconds": None,
            "solve_times_seconds":[]
        },
        "Friday": {
            "record_seconds": None,
            "solve_times_seconds":[]
        },
        "Saturday": {
            "record_seconds": None,
            "solve_times_seconds":[]
        },
        "Sunday": {
            "record_seconds": None,
            "solve_times_seconds":[]
        },
    }

    data_rows = []
    for row in rows_pre_calculation:
        date_str = row[0]
        solve_time_str = row[1]

        date_datetime = datetime.strptime(date_str, "%Y-%m-%d")
        day_of_week = date_datetime.strftime("%A")
        
        time_components = solve_time_str.split(":")
        if len(time_components) > 2: #solve time over an hour
            solve_time_seconds = (int(time_components[0]) * 3600) + (int(time_components[1]) * 60) + int(time_components[2])
        else: #solve time under an hour
            solve_time_seconds = (int(time_components[0]) * 60) + (int(time_components[1]))
        solve_time_minutes = "{:0.2f}".format(solve_time_seconds/60)

        if not current_records_and_averages[day_of_week]["record_seconds"] or current_records_and_averages[day_of_week]["record_seconds"] > solve_time_seconds:
            current_records_and_averages[day_of_week]["record_seconds"] = solve_time_seconds
            set_record_for_day_of_week = "New Record"
        else:
            set_record_for_day_of_week = ""
        current_records_and_averages[day_of_week]["solve_times_seconds"].append(solve_time_seconds)
        
        running_avg_for_day_of_week_seconds = round(mean(current_records_and_averages[day_of_week]["solve_times_seconds"]))
        running_avg_for_day_of_week_timedelta = timedelta(seconds=running_avg_for_day_of_week_seconds)        
        running_avg_for_day_of_week = strip_leading_zeros_and_colons(str(running_avg_for_day_of_week_timedelta))
        
        running_avg_for_day_of_week_minutes_with_decimals = "{:0.2f}".format(running_avg_for_day_of_week_seconds/60)

        record_for_day_of_week = strip_leading_zeros_and_colons(str(timedelta(seconds=current_records_and_averages[day_of_week]["record_seconds"])))
        record_for_day_of_week_minutes = "{:0.2f}".format(current_records_and_averages[day_of_week]["record_seconds"]/60)

        row = [date_str, day_of_week, solve_time_str, solve_time_minutes, running_avg_for_day_of_week, running_avg_for_day_of_week_minutes_with_decimals, record_for_day_of_week, record_for_day_of_week_minutes, set_record_for_day_of_week]
        data_rows.append(row)
    
    return data_rows

def main():
    print("The dates you enter here will be plugged into the CSV filename to find and update your solve times file.")
    start_date, end_date = helpers.get_start_and_end_dates()
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    rows_pre_calculation = []
    with open(f'solve_times_{start_date_str}_{end_date_str}.csv', 'r') as f:
        csvfile = csv.reader(f)
        for count, row in enumerate(csvfile):
            if count != 0:
                rows_pre_calculation.append(row)
    
    row_headers = ['date', 'day_of_week', 'solve_time', 'solve_time_minutes', 'running_avg_for_day_of_week', 'running_avg_for_day_of_week_minutes', 'record_for_day_of_week', 'record_for_day_of_week_minutes', 'set_record_for_day_of_week']
    data_rows = build_csv_rows(rows_pre_calculation)
    with open(f'solve_times_and_other_data_{start_date_str}_{end_date_str}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(row_headers)
        for row in data_rows:
            writer.writerow(row)

if __name__ == "__main__":
    main()