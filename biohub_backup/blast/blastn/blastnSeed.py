"""
Modulo para el almacenamiento de hits de Blast para el algoritmo Blastn

v.0.1

By: Juan Antonio Marín Sanz
Date: 29/11/2021
Location: Córdoba, Spain
"""

import xml.dom.minidom
from pathlib import Path
import numpy as np

from rich import print as rprint
from rich.progress import Progress

from biohub.sequences.fasta import Fasta
from biohub.blast.blastn.blastn import Blastn
from biohub.blast.blastn.blastn import BlastnXML2
from biohub.blast.blastn.blastn import BlastnXML


class BlastnSeeds:

    def __init__(self, seeds, genome, args):

        self.seeds = seeds
        self.genome = genome
        self.args = args

        self.args.evalue = self.estimateCutPoint()

        self.results = self.search()

    def estimateCutPoint(self):

        dbLen, hspLen, kappa, lamda, entropy = self.extractParametersValue()

        score = (self.args.size - self.args.misThreshold) * self.args.blastReward +\
                 self.args.misThreshold * self.args.blastPenalty -\
                 self.args.gapThreshold * self.args.blastOpenGap -\
                 0 * self.args.blastExtendGap

        bitScore = (lamda * score - np.log(kappa)) / np.log(2)

        evalue = hspLen * dbLen * pow(2, -1 * bitScore)

        rprint("[bright_white]Estimating e-value[/]")
        rprint(f"\t[bold bright_red]e-value[/]: [bright_white]{evalue}[/]")
        rprint(f"\t\t[bold bright_green]Seed size[/]: [bright_white]{self.args.size}[/]")
        rprint(f"\t\t[bold bright_green]Expected matches[/]: [bright_white]{self.args.size - self.args.misThreshold}[/]")
        rprint(f"\t\t[bold bright_green]Expected mismatches[/]: [bright_white]{self.args.misThreshold}[/]")
        rprint(f"\t\t[bold bright_green]Expected gap[/]: [bright_white]{self.args.gapThreshold}[/]")

        return evalue * 10

    def extractParametersValue(self):

        blast = Blastn(Fasta(file = Path(self.args.tmpDirectory, "decoy.fasta"),
                             seqIDs = [f"Decoy_len_{self.args.size}"],
                             sequences = ["A" * self.args.size]),
                       self.genome,
                       self.args,
                       directory = self.args.tmpDirectory)

        blastXml2 = BlastnXML2(blast.xml2File)
        blastXml = BlastnXML(blastXml2.files[0])


        infile = xml.dom.minidom.parse(f"{blastXml.xmlFile}")

        dbLen = int(infile.getElementsByTagName("db-len")[0].childNodes[0].data)
        hspLen = self.args.size - int(infile.getElementsByTagName("hsp-len")[0].childNodes[0].data)
        kappa = float(infile.getElementsByTagName("kappa")[0].childNodes[0].data)
        lamda = float(infile.getElementsByTagName("lambda")[0].childNodes[0].data)
        entropy = float(infile.getElementsByTagName("entropy")[0].childNodes[0].data)

        rprint("[bright_white]Scoring parameters extracted[/]")
        rprint(f"\t[bold bright_red]Database size[/]: [bright_white]{dbLen}[/]")
        rprint(f"\t[bold bright_red]HSP size[/]:      [bright_white]{hspLen}[/]")
        rprint(f"\t[bold bright_red]Kappa[/]:         [bright_white]{kappa}[/]")
        rprint(f"\t[bold bright_red]Lambda[/]:        [bright_white]{lamda}[/]")
        rprint(f"\t[bold bright_red]Entropy[/]:       [bright_white]{entropy}[/]")

        return dbLen, hspLen, kappa, lamda, entropy

    def search(self):

        results = dict()

        with Progress() as progress:

            task = progress.add_task("[bold bright_yellow]Performing Blast[/]...", total = len(self.seeds.seeds))

            for query, fasta in self.seeds.seeds.items():
                blast = Blastn(fasta,
                               self.genome,
                               self.args,
                               directory = self.args.tmpDirectory)

                results[query] = blast

                progress.update(task, advance = 1)

        return results