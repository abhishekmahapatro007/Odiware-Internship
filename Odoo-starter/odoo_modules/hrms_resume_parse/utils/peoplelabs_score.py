import time, requests, json, base64, tempfile, os, zipfile
from typing import List


# Authentication credentials
AUTH_USERNAME = "plabs"
AUTH_PASSWORD = "matching"

current_directory: str = os.path.dirname(os.path.abspath(__file__))

# Your existing code
url_submit = "http://34.224.85.157/submit"

#file_path = "/Users/prashantjoshi/Downloads/resume_as_base64_file(1).txt"
file_path_resume_zip = "./resume_archive.zip"
# task_id = None

def pdf_to_base64(file_path):
    with open(file_path, "rb") as pdf_file:
        encoded_pdf = base64.b64encode(pdf_file.read())
        return encoded_pdf.decode('utf-8')
    
def create_zip(file_list: List[str]):
    # Define the directory containing the files and the name of the zip file
    # folder_to_zip = current_directory
    zip_filename = f'{current_directory}/resume_archive.zip'

    # Create a new zip file
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        files_to_remove = []

        for file in file_list:
            zipf.write(file, arcname=os.path.basename(file))
            files_to_remove.append(file)

        # remove temp files
        for file in files_to_remove:
            os.remove(file)

    print(f'{zip_filename} created successfully.')
    return zip_filename
    
def submit_scoring_req(zip_loc: str, jd: str):
    with open(zip_loc, "rb") as file:
        files = {"file": file}
        data = {
            "job_description": f'{jd}'
        }

        try:
            response = requests.post(url_submit, files=files, data=data, auth=(AUTH_USERNAME, AUTH_PASSWORD))

            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")

            # Parse the response to get the task_id
            response_data = json.loads(response.text)
            task_id: str|None = response_data.get('task_id', None)

            if not task_id:
                print("Error: No task_id received in the response.")
                raise ValueError("ERR_NO_TASK_ID")

            return task_id
        except Exception as e:
            print("Error Occurred: ", e)
            # exit()
            return None

# Function to check status
def check_status(task_id):
    # URL for checking results
    url_result = f"http://34.224.85.157/result/{task_id}"
    print(url_result)
    response = requests.get(url_result, auth=(AUTH_USERNAME, AUTH_PASSWORD))
    print(response)
    return response.json()

def check_task(task_id):
    while True:
        print("timer", task_id)
        if task_id is not None:
            result = check_status(task_id)
            print(f"####### : {result}")
            if result['result'] != 'PROCESSING..':
                print("Task completed!")
                break
        time.sleep(15)
        
def trigger_single_file_parse(base64_utf8_str: str, job_desc: str):
    # print(type(base64_utf8_str))
    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.txt') as temp_file:
        v = base64_utf8_str

        temp_file.write(v)
        temp_file_name = temp_file.name

    print(temp_file_name)
    zip_loc = create_zip([temp_file_name])
    print(zip_loc)
    task_id = submit_scoring_req(zip_loc, job_desc)

    if task_id is None:
        raise ValueError("ERR_NO_TASK_ID")

    os.remove(zip_loc)
    return task_id
    # os.remove(temp_file_name)
    # return parsed_return