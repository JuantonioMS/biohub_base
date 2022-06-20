"""
Modulo para la lectura de ficheros XML2 de Blast para el algoritmo Blastn

v.0.1

By: Juan Antonio Marín Sanz
Date: 29/11/2021
Location: Córdoba, Spain
"""

from pathlib import Path
import xml.dom.minidom

class BlastnXML2:

    def __init__(self, xml2File):

        self.xml2File = xml2File
        self.files = self.extractFiles()

    def extractFiles(self):

        # Iniciando el parseador
        xml2File = xml.dom.minidom.parse(f"{self.xml2File}")

        # Extraer el contenido del tag "xi:include"
        files = xml2File.getElementsByTagName("xi:include")

        # Creando objetos Path para cada query
        files = [Path(self.xml2File.parent, Path(query.getAttribute("href"))) for query in files]

        return files