from openai import OpenAI
# import openai
import time
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import date
import pandas as pd


# import API_RowAppend file

def insert_thread_id(whatsapp_num, thread_id):
    print(whatsapp_num, thread_id)
    whatsapp_num = '\'' + whatsapp_num
    values = [[whatsapp_num, thread_id]]

    # SERVICE_ACCOUNT_FILE = r'C:\Users\Talha Abrar\Desktop\LUMS\SENIOR\Spring 2024\GEN AI\Project\OnlyBusiness\SpreadsheetAPI\onlybusinessdummy-8706fb48751e.json'
    SERVICE_ACCOUNT_FILE = r'SpreadsheetAPI\onlybusinessdummy-8706fb48751e.json'
    SPREADSHEET_ID = '1E_TLxnvSQgz2E7Y-5kFLJZtf8OogxPklmCQ819ip-vA'
    RANGE_NAME = 'Sheet2'

    # Authenticate and build the service
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API to append the data
    request = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': values}
    )
    response = request.execute()

    return


class Bot:
    def __init__(self, whatsapp_number, api_key="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", assistant_id="asst_8FWoRndfw1BUlalAHW0Xib45", thread_old=None, run_old=None):
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = assistant_id
        self.number = whatsapp_number
        if thread_old is None:
            self.thread = self.client.beta.threads.create()
            insert_thread_id(self.number, self.thread.id)
        else:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=thread_old)

        self.data = self.get_spreadsheet_data()

        self.assistant = self.client.beta.assistants.retrieve(
            assistant_id=self.assistant_id)
        # contains tuple of (query response) in ascending order (latest response at end of list)
        self.history = []

    def print_history(self):
        for msg, rsp in self.history:
            print(f"User: {msg}\nBot: {rsp}\n")

    def get_spreadsheet_data(self):

        # SERVICE_ACCOUNT_FILE = r'C:\Users\Talha Abrar\Desktop\LUMS\SENIOR\Spring 2024\GEN AI\Project\OnlyBusiness\SpreadsheetAPI\onlybusinessdummy-8706fb48751e.json'
        SERVICE_ACCOUNT_FILE = r'SpreadsheetAPI\onlybusinessdummy-8706fb48751e.json'
        SPREADSHEET_ID = '1E_TLxnvSQgz2E7Y-5kFLJZtf8OogxPklmCQ819ip-vA'
        RANGE_NAME = 'Sheet1'

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
        today_date = str(date.today())
        today_date = today_date.split('-')
        today_date.reverse()
        today_date = "-".join(today_date)
        query_results = df[df['Order Date'] == today_date]
        query_results = [query_results.columns.tolist()] + \
            query_results.values.tolist()
        return query_results

    def wait_on_run(self, run, thread):

        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)

        return run

    def insert_data_to_spreadsheet(self, values=None, order_id=None):
        # schema : [order_id, customer_id, customer_name, order date, order items, status, rider, Rider contact number, Delivery address, Amount, Rating]

        # values should be passed in the following format:

        
        # values = [["23", "69", "Zain Ali Khokhar", "01-03-2024", "HP Envy Screen Protector, HP Envy Hinge", "Delivered", "Sponge-Bob", "03248433434", "Out of Lahore", "$6666.44", "9", "Added through API"]]
        try:
        
            values[0][1] = self.number
            order_id = order_id +1 
            values[0][0] = order_id

            SERVICE_ACCOUNT_FILE = r'SpreadsheetAPI\onlybusinessdummy-8706fb48751e.json'
            SPREADSHEET_ID = '1E_TLxnvSQgz2E7Y-5kFLJZtf8OogxPklmCQ819ip-vA'
            RANGE_NAME = 'Sheet1'

            # Authenticate and build the service
            credentials = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])
            service = build('sheets', 'v4', credentials=credentials)

            # Call the Sheets API to append the data
            request = service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body={'values': values}
            )
            response = request.execute()

            return 'Successfully added order!', order_id
        
        except Exception as e:

            print('Failed to add order!')

    def call_required_function(self, tools_called, order_id):

        tool_outputs = []

        print(tools_called)

        returned_id = order_id
        for tool in tools_called:
            
            if (tool.function.name == 'insert_data_to_spreadsheet'):
                values_param = json.loads(tool.function.arguments)['values']
                
                response, returned_id = self.insert_data_to_spreadsheet(values=values_param, order_id = order_id)

                tool_outputs.append({'tool_call_id' : tool.id, 'output' : response})
            
        return tool_outputs, returned_id

    def send_message(self, message_content, order_id):


        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message_content,
        )
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )
        run = self.wait_on_run(run, self.thread)

        returned_id = order_id

        print(run.status)
        if (run.status == 'requires_action'):
            tool_outputs, returned_id = self.call_required_function(run.required_action.submit_tool_outputs.tool_calls, order_id)

            run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=self.thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
            )

        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id)

        response = messages.to_dict()["data"][0]["content"][0]['text']['value']
        self.history.append((message_content, response))
        return response, returned_id
