from __future__ import print_function

import os
import openai
import streamlit
import pickle
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def execute_gpt_command(params):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    promptText = createPromptText(params)
    print(promptText)
    # create a completion
    completion = openai.Completion.create(model="text-davinci-003",prompt=promptText, max_tokens=4000, temperature=0 )
    response = completion.choices[0].text
    return response

def createPromptText(params):
    print ("creating prompt")
    promptText = "Write Medical Necessity letter to insurance company named {insurance_company} for patient named {patient_name} , needs {treatment} treatment for {diagnosis}. Write letter in {tone} tone."
    promptText = promptText.replace("{insurance_company}", params["insuranceCompany"])
    promptText = promptText.replace("{treatment}", params["treatment"])
    promptText = promptText.replace("{diagnosis}", params["diagnosis"])
    promptText = promptText.replace("{tone}", params["tone"])

    if (bool (params["includeReferences"])):
        promptText = promptText + " Include scientific references from book."
    
    if (bool (params["includeTrialData"])):
        promptText = promptText + " Include trial data supporting FDA approval."
    
    if (bool (params["clinicalRationale"])):
        promptText = promptText + " Include clinical rationale behind the treatment."

    return promptText

def create_document_and_insert(text_content):
    """Shows usage of the Docs API.
    creates new document with text content provided
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    title = 'Letter of medical necessity'
    body = {
        'title': title
    }
    doc = service.documents().create(body=body).execute()
    title = doc.get('title')
    _id = doc.get('documentId')
    print(f'Created document with title: {title}, id: {_id}')

    # Text insertion
    requests = [
         {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': text_content
            }
        }
    ]
    result = service.documents().batchUpdate(documentId=_id, body={'requests': requests}).execute()



def unMaskTemplate (template, params):
    template = template.replace("{patient_name}", params["patientName"])
    template = template.replace("{Your Name}", params["doctor_name"])
    template = template.replace("[Your Name]", params["doctor_name"])
    return template
