from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

# Path to your service account key file


def fetch_thread(whatsapp_num="3248433434"):
    # schema : [order_id, customer_id, customer_name, order date, order items, status, rider, Rider contact number, Delivery address, Amount, Rating]

    SERVICE_ACCOUNT_FILE = r'onlybusinessdummy-8706fb48751e.json'
    SPREADSHEET_ID = '1E_TLxnvSQgz2E7Y-5kFLJZtf8OogxPklmCQ819ip-vA'
    RANGE_NAME = 'Sheet2'

    # Authenticate and build the service
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API to append the data
    sheet = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, majorDimension='ROWS').execute()

    sheet_values = sheet['values']
    column_names = sheet_values[0]
    data_rows = sheet_values[1:]

    df = pd.DataFrame(data_rows, columns=column_names)
    query_results = df[df['Phone Number'] == whatsapp_num]
    if len(query_results) > 0:
        return query_results['Thread ID'].values[0]
    else:
        return None


fetch_thread()
