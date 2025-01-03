import base64

def pdf_to_base64(file_path):
    with open(file_path, "rb") as pdf_file:
        encoded_pdf = base64.b64encode(pdf_file.read())
        return encoded_pdf.decode('utf-8')
    
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