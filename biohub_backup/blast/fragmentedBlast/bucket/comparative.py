"""
Modulo para el almacenamiento de hits de Blast para el algoritmo Blastn

v.0.1

By: Juan Antonio Marín Sanz
Date: 29/11/2021
Location: Córdoba, Spain
"""

from pathlib import Path
from biohub.sequences.fasta import Fasta

class Comparative:

    def __init__(self, file):

        self.file = file

        self.pairs = self.read()

    def read(self):

        pairs = dict()

        with open(f"{self.file}", "r") as csv:

            content = csv.read().split("\n")[1:]
            if content[-1] == "":
                content = content[:-1]

            for line in content:
                genome, reference = line.split("\t")

                genome = Path(genome)
                reference = Path(reference)

                genome = Fasta(file = genome, verbose = False)
                reference = Fasta(file = reference, verbose = False)

                pairs[genome] = reference

        return pairs