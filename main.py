
from datetime import datetime
import os
from pathlib import Path
from pymongo import MongoClient
import jinja2
from selenium import webdriver
import json
from typing import List
import csv
import pandas as pd

final_export_path = "exports"

def print_pdfs():
    chrome_options = webdriver.ChromeOptions()
    appState = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
                "selectedDestinationId": "Save as PDF",
                "version": 2,
                "isHeaderFooterEnabled": False,
                "isLandscapeEnabled": True,
                "marginsType": 1,
                "mediaSize": {
                    "height_microns": 420000, 
                    "name": "ISO_A3",
                    "width_microns": 297000,
                    "custom_display_name": "A3"
                    },
                "isCssBackgroundEnabled": True}
    BASE_DIR = os.path.dirname(__file__)
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(appState),
             'savefile.default_directory': f"{BASE_DIR}/{final_export_path}/uncroppedPdfs", }
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('kiosk-printing')

    driver = webdriver.Chrome(f'{BASE_DIR}\\chromeDriver\\chromedriver.exe', options=chrome_options)
    for i in Path(f"{BASE_DIR}/{final_export_path}/html").iterdir():
        driver.get(f"file:///{BASE_DIR}/{final_export_path}/html/{i.name}")
        driver.execute_script("window.print();")
    driver.close()


if __name__ == "__main__":
    connection_string = "mongodb+srv://doadmin:baU7689V1S35w2Qu@db-mongodb-ams3-11593-83236c2d.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
    dataframe = pd.read_csv("data.csv")
    records = { (x["lastName"]+x["firstName"]): x for x in (dataframe.to_dict(orient="records"))}


    jinja_path = Path(__file__).parent / "templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(jinja_path), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('index.jinja2')

    client = MongoClient(connection_string)
    db = client['admin']
    collection = db['child']

    # create the export folder
    if not os.path.exists(final_export_path + "/html"):
        os.makedirs(final_export_path + "/html")

    if not os.path.exists(final_export_path + "/uncroppedPdfs"):
        os.makedirs(final_export_path + "/uncroppedPdfs")

    
    print(records)

    for i in collection.find():
        l = i['lastName'] + i['firstName']
        transportation_mode =  i["modeOfTransportation"].lower()
        if transportation_mode == "tren":
            transportation_mode = "cu mașina"
        elif transportation_mode == "autobuz/troleibuz":
            transportation_mode = "transportul public"

        print("" if l not in records else records[l])
        folderId = "B-1334" if l not in records else records[l]["folderId"] 
        try:
            birthDay = datetime.fromisoformat(i['birthDay'][:-1])
        except ValueError as e:

            birthDay = datetime.strptime(i['birthDay'], '%a %b %d %Y %H:%M:%S %Z%z')
        
        birthDay = birthDay.strftime("%d.%m.%Y")

        with open(f'exports/html/export-{l}.html', 'w', encoding="utf-8") as f:
            print(folderId)
            f.write(template.render(
                folderNumber = folderId, 
                lastName=i["lastName"],
                firstName=i["firstName"], 
                gender=i["gender"],
                birthDay=birthDay,
                birthPlace=i["birthPlace"],
                contactPhone=i["phone"],
                contactEmail=i["email"],
                prevSchool=i["previouosSchool"],

                fatherName=i["fathersName"],
                fatherJob=i["fathersJob"],
                fatherPhone=i["fathersMobilePhone"],
                fatherWorkPhone=i["fathersWorkPhone"],

                motherName=i["mothersName"],
                motherJob=i["mothersJob"],
                motherPhone=i["mothersMobilePhone"],
                motherWorkPhone=i["mothersWorkPhone"],

                landline = i["landlinePhone"],

                tutorName = i["tutorsName"],
                tutorJob = i["tutorsJob"],
                tutorPhone = i["tutorsMobilePhone"],
                tutorWorkPhone = i["tutorsWorkPhone"],

                homeType = i["HomeType"].lower(),
                homeTypeOther = i["HomeOther"],
                homeAddress = i["HomeAddress"],

                extracurricular = i["participatesInExtracurriculars"].lower(),
                extracurricularDetails = i["participatesInExtracurricularsOther"],

                stimulated = i["hasBeenStimulatedDuringExtracurriculars"],
                stimulatedDetails = i["hasBeenStimulatedDuringExtracurricularsOther"],

                hasComputer = i["whereHasAccessToComputer"].lower(),
                hasComputerOther = i["whereHasAccessToComputerOther"],
                transport = transportation_mode,
                distance= i["distanceToSchool"],
                ))

    print_pdfs()