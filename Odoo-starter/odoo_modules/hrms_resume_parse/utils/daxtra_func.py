import requests
import os
from .to_base64_string import pdf_to_base64
import json

current_directory = os.path.dirname(os.path.abspath(__file__))

def get_access_tkn():
    account_id = os.getenv('SECRET_KEY', "odiware")
    access_token_url = f"https://cvxdemo.daxtra.com/cvx/rest/auth/v1/access_token?account={account_id}"
    payload={}
    files={}
    headers = {}

    response = requests.request("GET", access_token_url, headers=headers, data=payload, files=files)

    # Check for errors
    if response.status_code == 200:
        # print("Resume parsed successfully!")
        parsed_tkn = response.text
        print(parsed_tkn)  # Print or process the parsed data as needed
        return parsed_tkn
    else:
        print(f"Failed to parse resume. Status code: {response.status_code}")
        print(response.text)  # Print the error message from Daxtra
        return None
    
def submit_resume(acs_tkn, base64pdf):
    # url = "https://cvxdemo.daxtra.com/cvx/rest/api/v1/profile/full/json"

    # payload={'account': acs_tkn,
    # 'file': base64pdf}
    # files=[

    # ]
    # headers = {}

    # response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # if response.status_code == 200:
    #     # print("Resume parsed successfully!")
    #     data = response.text
    #     json_data = json.loads(data)
    #     print(json_data["Resume"]["StructuredResume"]["ContactMethod"])  # Print or process the parsed data as needed
    #     return json_data
    # else:
    #     print(f"Failed to parse resume. Status code: {response.status_code}")
    #     print(response.text)  # Print the error message from Daxtra
    #     return None

    print(current_directory)
    with open(f'{current_directory}/parsed_resume.json', 'r') as file:
        return json.load(file)