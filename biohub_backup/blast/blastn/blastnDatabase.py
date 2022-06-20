"""
Modulo para la creación de bases de datos Blast para el algoritmo Blastn

v.0.1

By: Juan Antonio Marín Sanz
Date: 29/11/2021
Location: Córdoba, Spain
"""

from os import system
from pathlib import Path

class BlastnDatabase:

    def __init__(self, genome, directory):

        """
        Clase BlastDatabase

        Creación de bases de datos para su uso en algoritmos Blastn

        Atributos:
            genome = Objeto Fasta para la secuencia de referencia
            directory = Objeto Path para el directorio de salida
            database = Objeto Path para la base de datos
        """

        self.genome = genome
        self.directory = directory

        # Creación de la base de datos
        self.file = self.create()


    def create(self):

        # Archivo de salida en el directorio de trabajo
        database = Path(self.directory, f"{self.genome.file.stem}.db")

        # Llamada al programa de terceros
        if Path(self.directory, f"{self.genome.file.stem}.db.ndb").exists():
            pass
        else:
            system(f"makeblastdb -in {self.genome.file} -dbtype nucl -out {database}")


        return database


    def __str__(self):
        return f"{self.file}"

    def __repr__(self):
        return str(self)


