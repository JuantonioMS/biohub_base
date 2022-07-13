from biohub.utils import GeneralClass
from os.path import getsize

class File(GeneralClass):


    def newId(self, buffer = []):
        return "bhFL" + super().newId(buffer)


    @property
    def file(self):
        return self.path.name


    @property
    def name(self):
        return self.path.file[:-(len("." + self.suffixes) + 1)]


    @property
    def suffixes(self):
        return "".join(self.path.suffixes)


    @property
    def exists(self):
        return self.path.exists()


    @property
    def parent(self):
        return str(self.path.parent)

    @property
    def size(self):
        return getsize(self.path)


    def __str__(self):
        return str(self.path)


    def buildXmlElement(self) -> None:

        import xml.etree.ElementTree as ET

        element = ET.Element("file")

        return super().buildXmlElement(element)