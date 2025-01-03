import openai
# import PyPDF2
import logging
import pymupdf
import base64
import os, io, json
from typing import TypedDict, List, Optional
from docx import Document

ClusterOfSkills = TypedDict('ClusterOfSkills', {
    "cluster": str,
    "skills": List[str]
})
CompatibleDataType = TypedDict('CompatibleDataType',
                    {
                        "name": str,
                        "email": str,
                        "contact": str,
                        "total_exp": str,
                        "current_city": str,
                        "curr_org": Optional[str],
                        "linkedin_url": Optional[str],
                        # "highest_deg": Optional[str],
                        "cluster": Optional[List[ClusterOfSkills]],
                        "edu": Optional[str],
                    })

_logger = logging.getLogger(__name__)

# Set your OpenAI API key
openai_api_key = os.environ['OPENAI_API']
if openai_api_key is None:
    raise ValueError("No OpenAI API key found! Please add an OpenAI API key.")

openai.api_key = openai_api_key

def extract_text_from_pdf64_pymupdf(pdf_data):
    try:
        doc = pymupdf.open(stream=pdf_data)
        text = ""

        for page in doc:
            page_text = page.get_text()
            if page_text:
                text += page_text
        if not text:
            return "", "Failed to extract any text from the provided file."
            # raise ValueError("No text extracted from the PDF file.")

        return text, ""
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return "", e

def extract_text_from_docx_pythondocx(doc_data):
    try:
        from io import BytesIO
        doc = Document(BytesIO(doc_data))
        text = []
        for para in doc.paragraphs:
            if para.text:
                text.append(para.text)

        if not text:
            return "", "Failed to extract any text from the provided file."
            # raise ValueError("No text extracted from the PDF file.")

        return '\n'.join(text), ""
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return "", e

# Function to parse resume using GPT-3.5-turbo model
def parse_resume(resume_text):

    # print(">>>>>>>>>>>>>>>>>>\n INSIDE PARSER <<<<<<<<")
    prompt = f"""
    Parse and extract the following information from the resume and output as a stringified JSON with all newlines and 'enters' removed:

    - name:
    - email:
    - phone_number (no space):
    - current_city:
    - total_experience (only the year and month):
    - linkedin_url_of_the_candidate (if present in the resume):
    - education (only the highest degree):
      - degree:
      - institution:
      - graduation_year (only the year):
    - work_experience (only the latest year):
      - job_title:
      - company:
    - skills (categorize the spelling and typographically corrected skills as per array of - spoken_language_skills, technical_skills, business_skills, marketing_skills, design_skills, sales_skills, soft_skills, other_skills):

    Resume Text:
    {resume_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a resume parsing assistant. Do not send the markdown format and all the unspecified fields should be empty string or empty array."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,  # Adjust as needed based on expected response size
            temperature=0.12  # Temperature set to 0 for more deterministic output
        )

        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error during API call: {e}")
        return ""


def extract_text(file_base64):
    file_data = base64.b64decode(file_base64)

    if file_data.startswith(b'%PDF-'):
        return extract_text_from_pdf64_pymupdf(file_data)

    elif file_data.startswith(b'PK'):
        return extract_text_from_docx_pythondocx(file_data)

    return "", "Unknown file type received"

def compatibility_layer_gippity(person_data):
    """
        name, email, contact, total_exp, current city
    """
    trimmed_number = ""
    if isinstance(person_data["phone_number"], str):
        trimmed_number = person_data["phone_number"].strip().replace(" ", "")

    sv = person_data.get("skills", {})
    cluster: List[ClusterOfSkills] = []
    for keys in sv:
        skill_arr: list[str] = sv.get(keys)
        key_title: str = ' '.join(word.capitalize() for word in keys.split('_'))
        cluster.append({
            "cluster": key_title,
            "skills": skill_arr,
        })

    compatible_data: CompatibleDataType = {
        "name": person_data["name"],
        "email": person_data["email"],
        "contact": trimmed_number,
        "total_exp": person_data.get("total_experience", 0),
        "linkedin_url": person_data.get("linkedin_url_of_the_candidate", ""),
        "current_city": person_data.get("current_city", 0),
        "cluster": cluster,
        "edu": person_data["education"]["degree"],
        "curr_org": person_data["work_experience"]["company"]
    }

    # _logger.debug(compatible_data)

    """
    note - recruiter said that last employer is filled as the most recent employer.
    meaning, for an immediate joiner, it will be last employer.
    For joiners who are still working, it is going to be current employer. Hence,
    the if statement has been commented out which checks another condition.
    """
    return compatible_data

# Main function to handle input PDF and parse it
def main(resume: str):
    resume_text, file_read_err = extract_text(resume)
    #
    if not resume_text:
        _logger.error(f"Failed - {file_read_err}")
        return "", file_read_err

    parsed_info = parse_resume(resume_text)
    # TODO - remove the next commented line
    # parsed_info = """{"name":"Lujain Alsmadi","email":"lujainsmadi9495@gmail.com","phone_number":"+962777189466","current_city":"Amman, Jordan","total_experience":"2 years 7 months","linkedin_url_of_the_candidate":"linkedin.com/in/lujain-smadi","education":{"degree":"M.S in Computer Science","institution":"Jordan University of Science and Technology","graduation_year":"2021"},"work_experience":{"job_title":"Web Developer","company":"Alfa Bep"},"skills":{"spoken_language_skills":["English","Arabic"],"technical_skills":["HTML","CSS","JavaScript","Bootstrap","Laravel","PHP","MySQL","API","Swagger","Git"],"business_skills":[],"marketing_skills":[],"design_skills":[],"sales_skills":[],"soft_skills":["Communication Skills","Presentation Skills","Self Learning","Ability to learn","Problem Solving","Team Leading"],"other_skills":[]}}"""
    # parsed_info = """{"name":"Debiprasad Harichandan","email":"harichandan123@gmail.com","phone_number":"9611212900","current_city":"Bengaluru, India","total_experience":"11 years","linkedin_url_of_the_candidate":"","education":{"degree":"Master of Computer Application","institution":"Fakir Mohan University, Orissa","graduation_year":"2005"},"work_experience":{"job_title":"Senior Test Engineer","company":"Herbalife International"},"skills":{"spoken_language_skills":[],"technical_skills":["Selenium","Java","Automation","WebDriver","TestNG","BDD","Cucumber","SVN","Maven","GIT","API Testing","Postman","SQL Query","Functional Testing","Smoke Testing","Regression Testing","Sanity testing","User Acceptance Testing","TFS","Splunk","Conﬂuence","JIRA","Agile","Scrum","Manual Testing","Database Testing","HP QC (ALM)"],"business_skills":[],"marketing_skills":[],"design_skills":[],"sales_skills":[],"soft_skills":[],"other_skills":[]}}"""
    # _logger.debug(parsed_info)
    try:
        x = json.loads(parsed_info)
        # Below line is only for testing
        # x = json.loads(
        #     "{\"name\": \"A.NITESH PATRO\", \"email\": \"patronitesh.123@gmail.com\", \"phone_number\": \"919348788626\", \"education\": {\"degree\": \"Bachelor of Technology\", \"institution\": \"JUPITER COLLEGE , BHUBANESWAR\", \"graduation_year\": \"2018\"}, \"work_experience\": {\"job_title\": \"BUSINESS DEVLOPMENT MANAGER\", \"company\": \"THINK DIGITAL\", \"duration_start\": \"NOV 2022\", \"duration_end\": \"PRESENT\"}, \"skills\": [\"SALES\", \"Marketing\", \"Financial Service Consulting\", \"Client Relationship Management\", \"Strategic Marketing\", \"Market Trend Analysis\", \"Sales Strategy Development\", \"Content Creation\", \"Digital Channel Optimization\"]}"
        # )
        compatible_data = compatibility_layer_gippity(x)
        return compatible_data, ""
    except ValueError as e:
        _logger.error(e)
        return "", "Unexpected information parsed. Please try again. If the issue persist, contact the developer"
    except Exception as e:
        _logger.error(e)
        return "", "Unexpected Error has occurred. Failed to parse resume"
    # return parsed_info

