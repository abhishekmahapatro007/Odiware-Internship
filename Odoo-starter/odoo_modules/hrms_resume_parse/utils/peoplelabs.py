import requests
import json
import base64
import tempfile
import os
from typing import TypedDict, List, Optional

CompatibleDataType = TypedDict('CompatibleDataType',
                    {
                        "name": str,
                        "email": str,
                        "contact": str,
                        "total_exp": float,
                        "current_city": str,
                        "curr_org": Optional[str],
                        "highest_deg": Optional[str],
                        "cluster": Optional[List[dict[str, str|List[str]]]],
                        "edu": Optional[str],
                    })

def pdf_to_base64(file_path):
    with open(file_path, "rb") as pdf_file:
        encoded_pdf = base64.b64encode(pdf_file.read())
        return encoded_pdf.decode('utf-8')


def parse_pdf(base64resume: str):
    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # with open(f'{current_directory}/out_srinivasareddy.json', 'r') as file:
    #     return compatibility_layer_peoplelabs(json.load(file))
    return None, "Endpoint Unavailable"
    # Define the URL and the file path
    url_base64 = 'http://64.247.206.145:32153/upload'

    # Define the credentials
    username = 'admin'
    password = 'plabs123'

    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.txt') as temp_file:
        # create base64encode for pdf
        v = base64resume
        #  write to the temp file
        temp_file.write(v)
        temp_file_name = temp_file.name

    with open(temp_file_name, 'rb') as file:
        # Open the file in binary mode and prepare the files dictionary
        files = {'files[]': file}

        parsed_return = None

        try:
            # Send the POST request
            response = requests.post(url_base64, files=files, auth=(username, password), timeout=120)

            # Check the response

            if response.status_code == 200:
                print("Request successful!")
                print(f"Response: {response.status_code}")
                # print(response.text)
                d = response.json()
                # v = json.dumps(d, indent=2)
                # namesuffix = d["resume1"]["pi"]["name"].lower()
                # with open(f'out_{namesuffix}.json', 'w') as file_out:
                #     file_out.write(v)

                comp_return = compatibility_layer_peoplelabs(d)
                parsed_return = comp_return
            else:
                print(f"Request failed with status code: {response.status_code}")
                print("Response:")
                print(response.text)
                parsed_return = None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            err = "An unexpected error occurred. Unable to parse the resume."
            parsed_return = None

    os.remove(temp_file_name)
    return parsed_return, err

def compatibility_layer_peoplelabs(person_data):
    """
        name, email, contact, total_exp, current city
    """
    compatible_data: CompatibleDataType = {
        "name": person_data["resume1"]["pi"]["name"],
        "email": person_data["resume1"]["pi"]["email"],
        "contact": person_data["resume1"]["contact"]["contact"],
        "total_exp": person_data["resume1"]["total_exp"],
        "current_city": person_data["resume1"]["wex"][0]["location"],
        "cluster": person_data["resume1"]["cluster"],
        "edu": person_data["resume1"]["edu"][0]["degree"]
    }

    """
    note - recruiter said that last employer is filled as the most recent employer.
    meaning, for an immediate joiner, it will be last employer.
    For joiners who are still working, it is going to be current employer. Hence,
    the if statement has been commented out which checks another condition.
    """
    # if person_data["resume1"]["wex"][0]["end_year"] == "Till Date": # checks if person is still working
    if len(person_data["resume1"]["wex"]) > 0:
        compatible_data["curr_org"] = person_data["resume1"]["wex"][0]["company"]
    if len(person_data["resume1"]["edu"]) > 0:
        compatible_data["highest_deg"] = person_data["resume1"]["edu"][0]["degree"]

    return compatible_data