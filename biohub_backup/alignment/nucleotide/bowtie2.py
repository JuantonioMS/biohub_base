from pathlib import Path
import os

class Bowtie2:

    def __init__(self, sequences, genome, directory = Path()):
        pass

        self.sequences = sequences
        self.genome = genome
        self.directory = directory

        self.index = self.indexing()

        self.sam = self.aligning()

        self.bam = self.bam2Sam()

        self.sortedBam = self.sortBam()


    def indexing(self):

        print("Indexando")
        index = Path(f"{self.directory}/{self.genome.file.stem}_index")

        os.system(f"bowtie2-build --large-index --threads 10 -f {self.genome} {index}")

        return index


    def aligning(self):

        print("Alineando")
        sam = Path(self.directory, f"{self.genome.file.stem}.sam")
        print(sam)

        os.system(f"bowtie2 -f -p 10 -x {self.index} -U {self.sequences} -S {sam}")

        return sam


    def bam2Sam(self):

        bam = Path(self.directory, f"{self.genome.file.stem}.bam")

        os.system(f"sambamba view -S {self.sam} -f bam > {bam}")

        return bam


    def sortBam(self):

        sortedBam = Path(self.directory, f"{self.genome.file.stem}_sorted.bam")

        os.system(f"sambamba sort {self.bam} -o {sortedBam}")

        return sortedBam