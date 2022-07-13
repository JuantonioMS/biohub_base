import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess
from xml.dom import minidom
from datetime import datetime

from biohub.utils import GeneralClass
from biohub.file.format import Xml
from biohub.file import File
from biohub.process import Process

class Subject(GeneralClass):


    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.xmlFile = Xml(path = self.path)
        self.path = self.xmlFile.parent

        if self.xmlFile.exists and self.xmlFile.size != 0:
            self.build()

        self.filesDir = Path(self.xmlFile.parent, "files")

        if not self.filesDir.exists():
            subprocess.call(f"mkdir {self.filesDir}", shell = True, executable = "/bin/bash")

        if not hasattr(self, "files"):
            self.files = {}

        if not hasattr(self, "processes"):
            self.processes = {}


    def newId(self, buffer = []):
        return "bhSJ" + super().newId(buffer)


    def build(self):

        metadata = self.xmlFile.root.find("metadata")
        files = self.xmlFile.root.find("files")
        processes = self.xmlFile.root.find("processes")

        self.buildMetadata(metadata)
        self.files = self.buildFiles(files)
        self.processes = self.buildProcesses(processes)


    def buildMetadata(self, metadata):

        for tag in metadata:
            setattr(self, tag.tag, tag.text)

    def buildFiles(self, files):

        aux = {}

        for file in files:

            file = File(xmlElement = file)
            aux[file.id] = file


        return aux


    def buildProcesses(self, processes):

        aux = {}

        for process in processes:

            process = Process(xmlElement = process)
            aux[process.id] = process

        return aux

    def buildXmlElement(self):

        import xml.etree.ElementTree as ET

        element = ET.Element("metadata")

        ET.SubElement(element, "id").text = self.id
        ET.SubElement(element, "name").text = self.name

        if hasattr(self, "date"):
            element.attrib["date"] = datetime.strftime(self.date, "%d/%m/%Y %H:%M:%S")

        if hasattr(self, "comment"):
            element.attrib["comment"] = self.comment

        return element


    def saveToXml(self):

        import xml.etree.ElementTree as ET

        root = ET.Element("subject")

        #  Metadata
        root.append(self.buildXmlElement())


        #  Files
        files = ET.SubElement(root, "files")
        for element in self.files.values():
            files.append(element.buildXmlElement())


        #  Processes
        processes = ET.SubElement(root, "processes")
        for element in self.processes.values():
            processes.append(element.buildXmlElement())

        with open(str(self.xmlFile), "wb") as outfile:

            prettyXml = minidom.parseString(ET.tostring(root)).toprettyxml(indent = "    ")

            outfile.write(prettyXml.encode("utf-8"))