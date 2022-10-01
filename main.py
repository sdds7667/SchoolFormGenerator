
from pathlib import Path
from pymongo import MongoClient
import jinja2

if __name__ == "__main__":
    connection_string = "mongodb+srv://doadmin:2UsWo93E51F46C0m@db-mongodb-ams3-16805-99e412a3.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-ams3-16805"

    jinja_path = Path(__file__).parent / "templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(jinja_path), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('index.jinja2')

    with open('export.html', 'w', encoding="utf-8") as f:
        f.write(template.render(
            folderNumber = "B-1332", 
            lastName="Plămădeală", 
            firstName="Ion", 
            gender="Masculin",
            birthDay="2015.05.29",
            birthPlace="București",
            contactPhone="0722 222 222",
            contactEmail="example@example.com",
            prevSchool="nr. 175",
            fatherName="Plămădeală Ion ",
            fatherJob="inginer lorem ipsum dolor sit amet consectetur adipiscing",
            fatherPhone="0722 222 222",
            fatherWorkPhone="021 222 222",

            motherName="Plămădeală Maria",
            motherJob="inginer lorem ipsum dolor sit amet consectetur adipiscing",
            motherPhone="0722 222 222",
            motherWorkPhone="021 222 222",

            homeType = "bloc",
            homeTypeOther = "",
            homeAddress = "Str. Lorem Ipsum, nr. 1, bl. A, sc. A, ap. 1",
            ))