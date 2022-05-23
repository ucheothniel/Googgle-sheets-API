#from __future__ import print_function

#import os.path
#from googleapiclient.errors import HttpError
#from google.auth.transport.requests import Request
#from google_auth_oauthlib.flow import InstalledAppFlow

#from google.oauth2.credentials import Credentials

from optparse import Values
from googleapiclient.discovery import build


from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
#This line defines the scope (google resources) which we want to authourize.

#First set credentials to none before setting the credetials for the serviceaccount
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

#The spreadsheet ID is the part of the googlesheet URL after /d/ and before /edit
SAMPLE_SPREADSHEET_ID = '1BFjHv_pOFDou4FErd_1P9Hw9c5mvuMOpoN3Aq_D2LDw'

# We excluded this line because we do not want to specify a range
# SAMPLE_RANGE_NAME = 'Class Data!A2:E'

service = build('sheets', 'v4', credentials=creds)

#call the sheets API, esnure to use '.spreadsheets' and not '.spreadsheet'
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range="TestSheet!A1:D4").execute()

#print(result) #this prints the entire results including the definition of the rows etc

#now we define the values themselves so we can print the values in the range specified
# and if there are no values in any row, return an empty set []
Values = result.get("values", [])

#print(Values)

#Now we have to define the new input to be sent to the sheet. Take note that a range needs to be specified
# for the new rows and colums the new data would beinserted into, so this code has to be finetuned, also
# we need to figure how to save the output of the web scraping into a variable list, that will be parsed into the 
#update request line below for body={values: *data to be added*}
# we might need an if else loop to ensure this is automated everytime there is a new data beingscrapped, so that
# the process is dynamic and automated. 
#Also we used valueInputOption USER_DEFINED to ensure the data us inputed just as a user would add info on the spread sheet directly.
#reference https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption 
# valueInputOption determines how the input should be interpreted


newInfo = [[4, "Abilash", 20, "2/3/2017"], [5, "DJ", 15, "6/7/2018"], [6, "Ahnaf", 25, "6/8/2019"], [7, "Claud", 28, "6/8/2022"]] 

request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                    range="TestSheet!A5:D", valueInputOption="USER_ENTERED", body={"values":newInfo})
response = request.execute()

print(response)


