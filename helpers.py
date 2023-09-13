import json
import requests
from datetime import datetime, timedelta

def get_airtable_records_in_view(airtable_api_token, base_id, table_id, view):
    view = view.replace(" ", "+")
    
    offset = ''
    i = 0
    records = []
    while offset != '' or i == 0:
        url = f'https://api.airtable.com/v0/{base_id}/{table_id}?view={view}&offset={offset}'
        headers = {"Authorization": f"Bearer {airtable_api_token}", "Content-Type": "application/json"}
        airtable_response = requests.get(url, headers=headers)
        airtable_response_content = json.loads(airtable_response.content)
        airtable_results_page = airtable_response_content['records']
        records.extend(airtable_results_page)
        try:
            offset = airtable_response_content['offset']
        except KeyError:
            offset = ''
        i += 1
    return records

def update_airtable_record(airtable_api_token, base_id, table_id, record_id, payload):
    headers = {"Authorization": f"Bearer {airtable_api_token}", "Content-Type": "application/json"}
    response =  requests.patch(f'https://api.airtable.com/v0/{base_id}/{table_id}/{record_id}', data=payload, headers=headers)
    return response

def get_start_and_end_dates():
    start_date_str = str(input('Enter start date (yyyy-mm-dd) > '))
    end_date_str = str(input('Enter end date (yyyy-mm-dd) > '))
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    return start_date, end_date