from openai import OpenAI
from datetime import datetime
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import date
import pandas as pd
from dotenv import load_dotenv
import os
import time

# import API_RowAppend file

load_dotenv()

SERVICE_ACCOUNT_PATH = "../SpreadsheetAPI/onlybusinessdummy-8706fb48751e.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, SERVICE_ACCOUNT_PATH)
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


def show_json(obj):
    display(json.loads(obj.model_dump_json()))


def get_service():

    # Authenticate and build the service
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    service = build('sheets', 'v4', credentials=credentials)

    return service


class Bot:
    def __init__(self, whatsapp_number, api_key=os.getenv('OPENAI_API_KEY'), assistant_id="asst_8FWoRndfw1BUlalAHW0Xib45", thread_old=None, run_old=None, user_type="user"):
        self.client = OpenAI(api_key=api_key)
        if user_type == "user":
            self.assistant_id = assistant_id
        elif user_type == "admin":
            self.assistant_id = "asst_H8Tz1E3QJaEqA4HgRDi8ocsw"
        self.number = str(whatsapp_number)
        self.service = get_service()

        if thread_old is None:
            self.thread = self.client.beta.threads.create()
            self.insert_thread_id(self.number, self.thread.id)
        else:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=thread_old)

        self.data = self.get_spreadsheet_data()

        self.assistant = self.client.beta.assistants.retrieve(
            assistant_id=self.assistant_id)
        self.history = []
        self.order_placed = False

    def insert_thread_id(self, whatsapp_num, thread_id):
        print(whatsapp_num, thread_id)
        whatsapp_num = '\'' + whatsapp_num
        values = [[whatsapp_num, thread_id]]

        RANGE_NAME = 'Sheet2'

        # Call the Sheets API to append the data
        request = self.service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': values}
        )
        response = request.execute()



    def print_history(self):
        for msg, rsp in self.history:
            print(f"User: {msg}\nBot: {rsp}\n")

    def getRowOrder(self, order_id):
        order = []
        orders_data = self.get_spreadsheet_data()

        # & (orders_data['Customer ID'] == self.number)
        order = orders_data.loc[(orders_data['Order ID'] == order_id)]

        number = '+' + list(order['Customer ID'])[0]

        if number != self.number:
            return 'Tell the user they are not authorized to view this order!'

        if len(order) == 0:
            return 'Order not found!'
        else:
            order_val = order.to_numpy().tolist()
            return f' [order_id : {order_val[0][0]}, customer_id : {order_val[0][1]}, customer_name : {order_val[0][2]}, order date : {order_val[0][3]}, order items : {order_val[0][4]}, status : {order_val[0][5]}, Delivery address : {order_val[0][6]}, Amount : {order_val[0][7]}]'

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
            now = datetime.now()
            formatted_date_time = now.strftime('%d/%m/%y - %H:%M:%S')

            values[0][3] = formatted_date_time
            values[0][1] = self.number
            order_id = order_id + 1
            values[0][0] = order_id
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

            self.order_placed = True
            return f'Give the user a confirmation that their order has been placed', order_id

        except Exception as e:

            print('Failed to add order!', e)
            return "Failed to add order!", order_id

    def call_required_function(self, tools_called, order_id):

        tool_outputs = []

        print(tools_called)

        returned_id = order_id

        for tool in tools_called:
            if (tool.function.name == 'insert_data_to_spreadsheet'):
                values_param = json.loads(tool.function.arguments)['values']
                response, returned_id = self.insert_data_to_spreadsheet(
                    values=values_param, order_id=order_id)
                tool_outputs.append(
                    {'tool_call_id': tool.id, 'output': response})

            if (tool.function.name == 'get_row_order'):
                values_param = json.loads(tool.function.arguments)['order_id']
                response = self.getRowOrder(values_param)
                tool_outputs.append(
                    {'tool_call_id': tool.id, 'output': response})

            if (tool.function.name == 'get_spreadsheet_data'):
                response = self.get_spreadsheet_data()
                response = response.to_json()
                print("CHECK RESPONSE:", response)
                tool_outputs.append(
                    {'tool_call_id': tool.id, 'output': response})

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
            tool_outputs, returned_id = self.call_required_function(
                run.required_action.submit_tool_outputs.tool_calls, order_id)

            run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=self.thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id)

        response = messages.to_dict()["data"][0]["content"][0]['text']['value']


        print("--------------------------------------boolean-----------------------",self.order_placed)
        if self.order_placed is True:
            self.order_placed = False
            response = response + f"\n\nYour Order ID is: {returned_id}. You can use your Order ID for tracking your order."
        
        self.history.append((message_content, response))
        return response, returned_id
