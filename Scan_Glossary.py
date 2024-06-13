import requests
import json
import pandas as pd

# Function to fetch data and create DataFrame
def fetch_data():

    with open('TableViewConfig for Business Glossary (Column Headers Renamed).json', 'r') as file:
        viewConfig = json.load(file)
        
    urlForFileId = "https://novelis-dev.collibra.com/rest/2.0/outputModule/export/excel-file?validationEnabled=true"    
    payloadForFileId = json.dumps(viewConfig)
    headersForFileId  = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic c3N1dHJhZGhhcjpTYW11Kl8zNDUxMjM=',

    }
    
    responseForFileId = requests.request("POST", urlForFileId , headers=headersForFileId, data=payloadForFileId)
    
    JSONres = json.loads(responseForFileId.text)
    fileId = JSONres["id"]

    #For saving the excel file
    url = "https://novelis-dev.collibra.com/rest/2.0/files/"+str(fileId)+""
    
    payload = {}
    headers = {
    'Authorization': 'Basic c3N1dHJhZGhhcjpTYW11Kl8zNDUxMjM=',
    
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    if response.status_code == 200:

        with open('data.xlsx', 'wb') as f:
            f.write(response.content)
            dataSet = pd.read_excel('data.xlsx')
            return dataSet
    else:
        return f"Failed to retrieve data: {response.status_code}"        
    
    