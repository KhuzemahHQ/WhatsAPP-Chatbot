from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Path to your service account key file

def insert_data_to_spreadsheet(values = None):
    # schema : [order_id, customer_id, customer_name, order date, order items, status, rider, Rider contact number, Delivery address, Amount, Rating]

    # values should be passed in the following format:

    #values = [["23", "69", "Zain Ali Khokhar", "01-03-2024", "HP Envy Screen Protector, HP Envy Hinge", "Delivered", "Sponge-Bob", "03248433434", "Out of Lahore", "$6666.44", "9", "Added through API"]]


    SERVICE_ACCOUNT_FILE = r'C:\Users\Ahad Imran\Desktop\GenAI\Project\onlybusinessdummy-8706fb48751e.json' 
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


insert_data_to_spreadsheet()
