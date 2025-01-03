import logging
import os
from datetime import date, datetime
from typing import TypedDict

from lxml import etree

# import time

_logger = logging.getLogger(__name__)

file_dir = os.path.dirname(__file__)
file_name = os.path.join(file_dir, '../static/postjobfree_q/job_queue.xml')

PJF_JobType = TypedDict('PJF_JobType',
                    {"title": str, "date": date, "referencenumber": str, "url": str, "company": str, "location": str,
                     'description': str, "salary": str})

def helper_job(job_data: PJF_JobType):
    print(job_data)

def create_xml():
    source = etree.Element("source")

    tree = etree.ElementTree(source)  # we write to a file using this variable.
    tree.write("job_queue.xml",
               xml_declaration=True,
               encoding='UTF-8',
               pretty_print=True)


def add_job(job_data: PJF_JobType):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_name, parser)
    source = tree.getroot()

    job = etree.SubElement(source, "job")

    title = etree.SubElement(job, "title")
    date_t = etree.SubElement(job, "date")
    ref_nb = etree.SubElement(job, "referencenumber")
    url = etree.SubElement(job, "url")
    company = etree.SubElement(job, "company")
    location = etree.SubElement(job, "location")
    description = etree.SubElement(job, "description")
    salary = etree.SubElement(job, "salary")

    description_cdata = etree.CDATA(f"{job_data['description']}")

    title.text = job_data["title"]
    date_t.text = job_data["date"].strftime("%Y-%m-%d")
    ref_nb.text = job_data["referencenumber"]
    url.text = job_data["url"]
    company.text = job_data["company"]
    location.text = job_data["location"]
    description.text = description_cdata
    salary.text = job_data["salary"]

    # print(etree.tostring(job, pretty_print=True))

    source_tree = etree.ElementTree(source)
    source_tree.write(file_name,
               xml_declaration=True,
               encoding='UTF-8',
               pretty_print=True)


def edit_job(ref_nb: str, update_data: PJF_JobType):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_name, parser)
    source = tree.getroot()

    for element in source.iter():
        if element.text == ref_nb:
            parent = element.getparent()
            for ele in parent.iter():
                if ele.tag in update_data.keys():
                    xy: str = ele.tag
                    # noinspection PyTypedDict
                    ele.text = update_data.get(xy, None)
            # print(etree.tostring(parent, pretty_print=True))
            break

    
    source_tree = etree.ElementTree(source)
    source_tree.write(file_name,
               xml_declaration=True,
               encoding='UTF-8',
               pretty_print=True)

    # print(tree.xpath('//referencenumber')) # this is the way to write xpath. currently not used.

def remove_oldest_job():
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_name, parser)
    source = tree.getroot()

    # Find all <date> tags
    date_tags = tree.findall('.//date')

    # Initialize variables to find the oldest date
    oldest_date = None
    oldest_parent = None

    for date_t in date_tags:
        date_text = date_t.text
        date_obj = datetime.strptime(date_text, '%Y-%m-%d')

        if oldest_date is None or date_obj < oldest_date:
            oldest_date = date_obj
            oldest_parent = date_t.getparent()

    if oldest_parent:
        oldest_parent.getparent().remove(oldest_parent)
    
    source_tree = etree.ElementTree(source)
    source_tree.write(file_name,
               xml_declaration=True,
               encoding='UTF-8',
               pretty_print=True)

def delete_job(ref_nb):
    _logger.debug(">>>>>>>>>>>>>>> %s", ref_nb)
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_name, parser)
    source = tree.getroot()

    for element in source.iter():
        if element.text == ref_nb:
            parent = element.getparent()
            parent.getparent().remove(parent)
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
    add_job({"title": "Job title", 
             "url":"http://sdfsd.com", 
             "company": "A company", 
             "date": date(2033,12, 2),
             "description": "Sdfdsfdsfsdfsdsd sdfsdf sdf sdfsd fsdf sdfewwerwer wet werg sddsfas gh yht", 
             "location": "A good lcoatuon", 
             "referencenumber": "fsdf-2342342", 
             "salary": "234234.00"})
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