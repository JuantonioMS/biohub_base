"""
Modulo para la lectura de ficheros XML de Blast para el algoritmo Blastn

v.0.1

By: Juan Antonio Marín Sanz
Date: 29/11/2021
Location: Córdoba, Spain
"""

from os import system
from pathlib import Path

from biohub.blast.blastn.blastnDatabase import BlastnDatabase
from biohub.blast.blastn.blastnXml import BlastnXML
from biohub.blast.blastn.blastnXml2 import BlastnXML2



class Blastn:

    def __init__(self, queries, genome, args, directory = Path()):

        # Valor límete para el e-value
        try:
            if args.evalue:
                self.evalue = args.evalue
            else:
                self.evalue = 10 # Por defecto
        except AttributeError:
            self.evalue = 10 # Por defecto

        # Valor de recompensa por acierto
        try:
            self.reward = args.blastReward
        except AttributeError:
            self.reward = 1 # TODO

        # Valor de penalización por mismatch
        try:
            self.penalty = args.blastPenalty
        except AttributeError:
            self.penalty = -2 # TODO

        # Valor de penalización por abrir gap
        try:
            self.openGap = args.blastOpenGap
        except AttributeError:
            self.openGap = 5 # TODO

        # Valor de penalización por extender gap
        try:
            self.extendGap = args.blastExtendGap
        except AttributeError:
            self.extendGap = 2 # TODO

        # Objetos Fasta para queries y genoma de referencia
        self.queries = queries
        self.genome = genome

        # Directorio de salida
        self.directory = directory

        # Generando la base de datos
        self.database = self.createDatabase()

        # Llamando al algoritmo Blastn
        self.xml2File = self.call()

        # Resultados del blast
        self.results = self.getResults()


    def createDatabase(self):

        return BlastnDatabase(self.genome, self.directory)


    def call(self):

        parameters = f"-reward {self.reward} "
        parameters += f"-penalty {self.penalty} "
        parameters += f"-gapopen {self.openGap} "
        parameters += f"-gapextend {self.extendGap} "
        parameters += f"-evalue {self.evalue} "
        parameters += f"-outfmt 14"

        output = Path(self.directory, f"{self.queries.file.stem}.xml2")

        system(f"blastn {parameters} -db {self.database} -query {self.queries.file} -out {output}")

        return output


    def getResults(self):

        blastnXml2 = BlastnXML2(self.xml2File)

        aux = dict()
        for xmlFile, queryName in zip(blastnXml2.files, self.queries.content):

            aux[queryName] = BlastnXML(xmlFile).hits

        return aux

