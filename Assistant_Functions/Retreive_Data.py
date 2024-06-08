

from dotenv import load_dotenv
import os, pandas as pd
load_dotenv()


SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

def get_spreadsheet_data(self):

        RANGE_NAME = 'Sheet1'

        # Call the Sheets API to append the data
        sheet = self.service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, majorDimension='ROWS').execute()

        sheet_values = sheet['values']
        column_names = sheet_values[0]
        print(column_names)
        data_rows = sheet_values[1:]

        df = pd.DataFrame(data_rows, columns=column_names)
        return df