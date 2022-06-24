from datetime import datetime
import random
from pathlib import Path
import copy

from collections.abc import Iterable
from xml.etree.ElementTree import SubElement

class GeneralClass:

    def __init__(self, **kwargs):

        self.initAttributes(kwargs)


    #  --------------------Generators--------------------


    def newDate(self):
        return datetime.now()


    def newId(self, buffer = []):

        storage = "0123456789qerwrtyuiopasdfghjklzxcvbnmQERWRTYUIOPASDFGHJKLZXCVBNM"


        newId = ""

        while not newId:

            newId = "".join(random.choices(storage, k = 15))

            if newId in buffer:
                newId = ""

        return newId


    #  --------------------Built-in methods--------------------


    def initAttributes(self, kwargs):

        for attribute, value in kwargs.items():
            setattr(self, attribute, value)


        if hasattr(self, "xmlElement"):
            self.initXmlElement()

        if hasattr(self, "date"):
            self.reformatDate()

        if hasattr(self, "path"):
            self.reformatPath()


    def initXmlElement(self):

        for tag in self.xmlElement:

            subElement = True if len(list(tag.iter())) > 1 else False

            if subElement:

                aux = []
                for subTag in tag:
                    aux.append(subTag.text)

                setattr(self, tag.tag, aux)

            else:
                setattr(self, tag.tag, tag.text)

        for attrib in self.xmlElement.attrib:
            setattr(self, attrib, self.xmlElement.attrib[attrib])


    #  --------------------Reforma methods--------------------


    def reformatPath(self):

        if not isinstance(self.path, Path):
            self.path = Path(self.path)


    def reformatDate(self):

        if not isinstance(self.date, datetime):
            self.date = datetime.strptime(self.date, "%d/%m/%Y;%H:%M:%S")


    #  --------------------Getters and setters methods--------------------


    def getAttributes(self):
        return self.__dict__


    def __repr__(self):

        message = f"{type(self).__name__} id {self.id if hasattr(self, 'id') else None}\n"

        for attribute, value, in self.getAttributes().items():

            if isinstance(value, Iterable) and type(value) != str:
                message += f"\t{attribute}\n"
                for element in value:
                    message += f"\t\t{element}\n"

            else:
                message += f"\t{attribute} {value}\n"

        return message


    #  --------------------Xml builders--------------------


    def avoidAttrs(self):
        return ["date", "comment", "xmlElement"]


    def buildXmlElement(self, element):

        mask = {"processes" : "process",
                "links" : "link",
                "files" : "file",
                "inputs" : "input",
                "outputs" : "output",
                "backgrounds" : "background",
                "tags" : "tag"}

        avoid = self.avoidAttrs()

        element.attrib["date"] = datetime.strftime(self.date, "%d/%m/%Y;%H:%M:%S")
        element.attrib["comment"] = self.comment if hasattr(self, "comment") else ""

        for attribute, value in self.getAttributes().items():

            if attribute not in avoid:

                if isinstance(value, Iterable) and type(value) != str:

                    subElement = SubElement(element, attribute)

                    if isinstance(value, dict):
                        value = list(value.values())

                    for subValue in value:
                        subsubElement = SubElement(subElement, mask[attribute])
                        subsubElement.text = f"{subValue}"

                else:
                    subElement = SubElement(element, attribute)
                    subElement.text = f"{value}"

        return element


    def updateDictAttrs(self, aux = {}, buffer = {}):

        new = copy.deepcopy(buffer)

        for key, value in aux.items():
            if key in new:

                if isinstance(new[key], list):
                    new[key] = new[key] + value

                else:
                    new[key] = value

            else:
                new[key] = value

        return new


    def assertPath(self, path):

        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            raise FileExistsError(f"File {path} does not exists")

        return path