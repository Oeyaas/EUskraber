from tika import parser
from bs4 import BeautifulSoup
import re, datetime, csv, requests

def PageScraper(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    PDF_imgs = soup.find_all(src="https://www.consilium.europa.eu/register/images/pdf.png")

    for PDF_img in PDF_imgs:
        link = PDF_img.parent["href"]
        title = PDF_img.parent.parent.a.contents
        date = PDF_img.parent.parent.parent.parent.find("span").contents
        metadata, content = PDF_Scraper(link)

        with open("data.csv", "a+") as outfile:
            writer = csv.DictWriter(
                outfile,
                fieldnames=["date","title", "link", "content", "metadata"])
            writer.writerow({"link":link, "title":title, "date":date, "metadata":metadata, "content":content})


def PDF_Scraper(PDF_URL):
    parsed_input = parser.from_file(PDF_URL)

    PDF_metadata = parsed_input["metadata"]
    PDF_content = parsed_input["content"].strip()

    return metadata, content

for i in range(1, 11):
    PageScraper("https://www.consilium.europa.eu/register/en/content/out?document_date_from_date=&DOC_ID=&CONTENTS=&DOC_TITLE=&meeting_date_single_date=&DOC_SUBJECT=CONCL&meeting_date_to_date=&MEET_DATE=&document_date_to_date=&i=ADV&document_date_single_comparator=&DOS_INTERINST=&ROWSPP=25&document_date_single_date=&ORDERBY=DOC_DATE+DESC&DOC_LANCD=EN&meeting_date_single_comparator=&DOC_DATE=&typ=SET&NRROWS=500&meeting_date_from_date=&RESULTSET={i}".format(i = i))
