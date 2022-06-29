import subprocess
from pathlib import Path
from biohub import project, subject

from biohub.project import Project


class CreateProject:

    def __init__(self,
                 name: str,
                 path: Path,
                 subjects: list):

        if not isinstance(path, Path):
            self.path = Path(path)
        else:
            self.path = path

        self.name = name.replace(".", "_")

        self.createDir()
        self.createXmlFile()


    def createDir(self):
        subprocess.call(f"mkdir {self.path}/{self.name}",
                        shell = True,
                        executable = "/bin/bash")

        subprocess.call(f"mkdir {self.path}/{self.name}/files",
                        shell = True,
                        executable = "/bin/bash")


    def createXmlFile(self):
        subprocess.call(f"touch {self.path}/{self.name}/biohub_project.xml",
                        shell = True,
                        executable = "/bin/bash")


    def createObject(self, subjects):

        project = Project(path = Path(f"{self.path}/{self.name}/biohub_project.xml"))

        project.id = project.newId()
        project.date = project.newDate()

        project.subjects = [subject.id for subject in subjects]

        project.name = self.name

        project.saveToXml()