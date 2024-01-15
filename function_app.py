import azure.functions as func
import logging
import json
import os
import requests
from msal import ConfidentialClientApplication

# Extract the bearer token from the MSAL result
def extract_token(result):
    token_dump = json.dumps(result)
    token_json=json.loads(token_dump)
    msal_token = token_json["access_token"]
    bearer_token = "{} {}".format("Bearer", msal_token)  
    print(bearer_token) 
    return bearer_token


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HttpExample")
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    CLIENT_SECRET = os.environ["CLIENT_SECRET"]  
    CLIENT_ID = os.environ["CLIENT_ID"]
    AUTHORITY = os.environ["AUTHORITY"]  

    config = {
    "authority": AUTHORITY,
    "client_id": CLIENT_ID,    
    "client_secret": CLIENT_SECRET
    }

    # Initialize the MSAL confidential client
    app = ConfidentialClientApplication(config["client_id"],
                                        authority=config["authority"],
                                        client_credential=config["client_secret"])
    
    # Acquire an access token for the app itself
    result = app.acquire_token_for_client(scopes=["https://org5e77ac3d.crm11.dynamics.com/.default"])


    bearer_token = extract_token(result)   

    crmrequestheaders = {
        'Authorization': bearer_token,
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8'        
    }


    # Get the first and last name from the request
    firstname = req.params.get('firstname')
    if not firstname:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            firstname = req_body.get('firstname')

    logging.info(firstname)

    lastname = req.params.get('lastname')
    if not lastname:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            lastname = req_body.get('lastname')    

    logging.info(lastname)           

    # Check for firstname and lastname and if they exist, create a contact in CRM
    if firstname and lastname:
        logging.info('lastname')      
        contactsdata={ "firstname": firstname , "lastname": lastname }
        try:
            crmres = requests.post('https://org5e77ac3d.crm11.dynamics.com/api/data/v9.2/contacts', 
                       headers=crmrequestheaders, 
                       data=json.dumps(contactsdata))
            return func.HttpResponse(f"Success: {crmres}")  
        except Exception as e:
            return func.HttpResponse(f"Error, {e}")              
    else:
        return func.HttpResponse(
             "This HTTP triggered function expects two parameters: firstname and lastname.",
             status_code=200
        )


