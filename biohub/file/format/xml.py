import xml.etree.ElementTree as ET

from biohub.file import File


class Xml(File):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if self.exists and self.size != 0:
            self.read()

    def read(self):

        self.tree = ET.parse(self.path)
        self.root = self.tree.getroot()
