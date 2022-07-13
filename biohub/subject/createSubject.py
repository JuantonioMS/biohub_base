import subprocess
from pathlib import Path
from biohub.subject import Subject
from biohub.utils import GeneralClass

class CreateSubject:

    def __init__(self, name: str, path: Path):

        if not isinstance(path, Path):
            self.path = Path(path)
        else:
            self.path = path

        self.name = name.replace(".", "_")

        self.newId = "bhSJ" + GeneralClass().newId()

        self.createDir()
        self.createXmlFile()
        self.createObject()


    def createDir(self):
        subprocess.call(f"mkdir {self.path}/{self.newId}", shell = True, executable = "/bin/bash")

    def createXmlFile(self):
        subprocess.call(f"touch {self.path}/{self.newId}/biohub_subject.xml", shell = True, executable = "/bin/bash")

    def createObject(self):

        subject = Subject(path = Path(f"{self.path}/{self.newId}/biohub_subject.xml"))

        subject.id = self.newId
        subject.date = subject.newDate()
        subject.name = self.name


        subject.saveToXml()

