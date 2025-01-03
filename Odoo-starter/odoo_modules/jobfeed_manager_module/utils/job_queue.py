import os
from datetime import datetime
from typing import TypedDict, Optional, List, Literal

from lxml import etree

# import time

file_dir = os.path.dirname(__file__)
file_name = os.path.join(file_dir, '../static/linkedin_q/job_feed.xml')

"""
To post to linkedin jobs, the system needs to have the following data:
[Required]:  
    Job ID <partnerJobId>
    Company Name <company>
    Job Title <title>
    Job Description <description>
    Location String <location>
    Apply URL <applyUrl>
    LinkedIn Company ID <companyId>

[Non-essential]:
    <skills> <skill/> <skill/> <skill/> </skills>
    <workplaceTypes>
    <listDate>
    <expirationDate>
    <salary> (Doubt)
    <jobtype>
    <experienceLevel>
    <city> <state> <country>
"""
JobType = TypedDict('JobType', {
    "partnerJobId": str,
    "company": str,
    "title": str,
    'description': str,
    "location": str,
    "applyUrl": str,
    "companyId": str,
    "skills": Optional[List[str]],
    "workplaceTypes": Optional[Literal['On-site', 'Remote', 'Hybrid']],
    "listDate": Optional[datetime],
    "expirationDate": Optional[datetime],
    "salary": Optional[str],
    "jobtype": Optional[Literal['FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERNSHIP', 'VOLUNTEER']],
    "experienceLevel": Optional[Literal['INTERNSHIP', 'ENTRY_LEVEL', 'EXECUTIVE', 'ASSOCIATE', 'MID_SENIOR_LEVEL', 'DIRECTOR', 'NOT_APPLICABLE']],
    "city": Optional[str],
    "state": Optional[str],
    "country": Optional[str],
})

def helper_job(job_data: JobType):
    print(job_data)

def create_xml():
    source = etree.Element("source")

    tree = etree.ElementTree(source)  # we write to a file using this variable.
    tree.write("job_queue.xml",
               xml_declaration=True,
               encoding='UTF-8',
               pretty_print=True)


def add_job(job_data: JobType):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_name, parser)
    source = tree.getroot()

    job = etree.SubElement(source, "job")

    # Required
    partner_job_id = etree.SubElement(job, "partnerJobId")
    company = etree.SubElement(job, "company")
    title = etree.SubElement(job, "title")
    description = etree.SubElement(job, "description")
    location = etree.SubElement(job, "location")
    apply_url = etree.SubElement(job, "applyUrl")
    company_id = etree.SubElement(job, "companyId")

    partner_job_id.text = etree.CDATA(job_data["partnerJobId"])
    company.text = etree.CDATA(job_data["company"])
    title.text = etree.CDATA(job_data["title"])
    description.text = etree.CDATA(f"{job_data['description']}")
    location.text = etree.CDATA(job_data["location"])
    apply_url.text = etree.CDATA(job_data["applyUrl"])
    company_id.text = etree.CDATA(job_data["companyId"])


    # Non essential
    if job_data["skills"] and len(job_data["skills"]) > 0:
        skills = etree.SubElement(job, "skills")
        for item in job_data["skills"]:
            skill = etree.SubElement(skills, "skill")
            skill.text = etree.CDATA(item)

    if job_data.get("workplaceTypes", None):
        workplace_types = etree.SubElement(job, "workplaceTypes")
        workplace_types.text = etree.CDATA(job_data["workplaceTypes"])

    if job_data.get("listDate", None):
        list_date = etree.SubElement(job, "listDate")
        list_date.text = etree.CDATA(job_data["listDate"].strftime("%m/%d/%Y"))

    if job_data.get("expirationDate", None):
        list_date = etree.SubElement(job, "expirationDate")
        list_date.text = etree.CDATA(job_data["expirationDate"].strftime("%m/%d/%Y"))

    if job_data.get("salary", None):
        print("seems like someone passed salary but still in doubt, so skip.")
        # salary = etree.SubElement(job, "salary")
        # salary.text = etree.CDATA(job_data["salary"])

    if job_data.get("jobtype", None):
        job_type = etree.SubElement(job, "jobtype")
        job_type.text = etree.CDATA(job_data["jobtype"])

    if job_data.get("experienceLevel", None):
        exp_lvl = etree.SubElement(job, "experienceLevel")
        exp_lvl.text = etree.CDATA(job_data["experienceLevel"])

    if job_data.get("city", None):
        city = etree.SubElement(job, "city")
        city.text = etree.CDATA(job_data["city"])

    if job_data.get("state", None):
        state_place = etree.SubElement(job, "state")
        state_place.text = etree.CDATA(job_data["state"])

    if job_data.get("country", None):
        country = etree.SubElement(job, "country")
        country.text = etree.CDATA(job_data["country"])
    # print(etree.tostring(job, pretty_print=True))

    source_tree = etree.ElementTree(source)
    source_tree.write(file_name,
               xml_declaration=True,
               encoding='UTF-8',
               pretty_print=True)


# def edit_job(ref_nb: str, update_data: JobType):
#     parser = etree.XMLParser(remove_blank_text=True)
#     tree = etree.parse(file_name, parser)
#     source = tree.getroot()
#
#     for element in source.iter():
#         if element.text == ref_nb:
#             parent = element.getparent()
#             for ele in parent.iter():
#                 if ele.tag in update_data.keys():
#                     ele.text = update_data[ele.tag]
#             # print(etree.tostring(parent, pretty_print=True))
#             break
#
#
#     source_tree = etree.ElementTree(source)
#     source_tree.write(file_name,
#                xml_declaration=True,
#                encoding='UTF-8',
#                pretty_print=True)
#
#     # print(tree.xpath('//referencenumber')) # this is the way to write xpath. currently not used.

def remove_oldest_job():
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_name, parser)
    source = tree.getroot()

    # Find all <date> tags
    date_tags = tree.findall('.//listDate')

    # Initialize variables to find the oldest date
    oldest_date = None
    oldest_parent = None

    for date in date_tags:
        date_text = date.text
        date_obj = datetime.strptime(date_text, '%m/%d/%Y')

        if oldest_date is None or date_obj < oldest_date:
            oldest_date = date_obj
            oldest_parent = date.getparent()

    if oldest_parent:
        oldest_parent.getparent().remove(oldest_parent)
    
    source_tree = etree.ElementTree(source)
    source_tree.write(file_name,
               xml_declaration=True,
               encoding='UTF-8',
               pretty_print=True)

def delete_job(job_id):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_name, parser)
    source = tree.getroot()

    for element in source.iter():
        if element.text == str(job_id):
            parent = element.getparent()
            parent.getparent().remove(parent)
            parent.remove(element)
            break

    
    source_tree = etree.ElementTree(source)
    source_tree.write(file_name,
               xml_declaration=True,
               encoding='UTF-8',
               pretty_print=True)



def main():
    # print("Executing creation of xml file")
    # create_xml()
    print("Executing addition of xml file")
    # add_job({"title": "Job title",
    #          "url":"http://sdfsd.com",
    #          "company": "A company",
    #          "date": "03-12-2342",
    #          "description": "Sdfdsfdsfsdfsdsd sdfsdf sdf sdfsd fsdf sdfewwerwer wet werg sddsfas gh yht",
    #          "location": "A good lcoatuon",
    #          "referencenumber": "fsdf-2342342",
    #          "salary": "234234.00"})
    # print("Editing of XML file")
    # x = time.time()
    # edit_job("fsdf-346834", {"location": "Kualalampur", "salary": "100", "title": "Mister Nefarious"})
    # y = time.time()
    # print(f"Finished in {y-x} sec")
    # print("Deleting of a tag in XML file")
    # x = time.time()
    # delete_job("fsdf-346834")
    # y = time.time()
    # print(f"Finished in {y-x} sec")