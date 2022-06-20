from rich.table import Table
from rich.console import Console
from rich.progress import Progress


class Fasta:

    def __init__(self, verbose = True, **kwargs):
        self.verbose = verbose

        self.file = kwargs["file"]

        try:
            self.seqIDs = kwargs["seqIDs"]
        except KeyError:
            self.seqIDs = []

        try:
            self.sequences = kwargs["sequences"]
        except KeyError:
            self.sequences = []


        if self.file.exists():
            self.content = self.readFile()

        else:
            self.content = self.writeFile()

        if self.verbose:
            self.summaryFasta()


    def summaryFasta(self):

        # Tabla resumen del archivo fasta

        table = Table(title = f"{self.file.name}")

        table.add_column("Number", justify = "right", style = "bright_cyan", no_wrap = True)
        table.add_column("SeqID", justify = "left", style = "bright_green")
        table.add_column("Length", justify = "left", style = "bright_white")

        for index, seqID in enumerate(self.content):

            length = len(self.content[seqID])

            table.add_row(str(index + 1), seqID, str(length))

        table.add_row("Total", "All", str(sum([len(self.content[key]) for key in self.content])))

        console = Console()
        console.print(table)



    def readFile(self):

        content = dict()
        with self.file.open("r") as fasta:

            # Separando el fichero el bloques |seqID, sequence|
            fileContent = fasta.read().split(">")[1:]

            for block in fileContent:
                block = block.strip("\n").split("\n")

                seqID = block[0]
                sequence = "".join(block[1:]).upper()

                content[seqID] = sequence

        return content


    def writeFile(self):

        content = dict()

        # Escribiendo el nuevo fichero
        with self.file.open("w") as fasta:
            for seqID, sequence in zip(self.seqIDs, self.sequences):

                # Guardando la sencuencia en el atirbuto
                content[seqID] = sequence.upper()

                # Escribiendo el seqID y la secuencia en el archivo
                fasta.write(f">{seqID}\n{sequence.upper()}\n")

        return content


    def __str__(self):
        return str(self.file)

    def __repr__(self):
        return str(self)