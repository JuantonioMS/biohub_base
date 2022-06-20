from rich import print as rprint
import os

class Check:

    def __init__(self, args):

        self.args = args

        rprint("Checking temporal working directory")
        rprint(f"[bold bright_cyan]Working directory:[/] {self.args.tmpDirectory.name} [italic bright_black]({self.args.tmpDirectory})[/]")
        self.checkWorkingDirectory()

        rprint("Checking query Fasta file")
        rprint(f"[bold bright_cyan]Fasta:[/] {self.args.query.name} [italic bright_black]({self.args.query})[/]")
        self.checkQueryFasta()

        rprint("Checking query Fasta file")
        rprint(f"[bold bright_cyan]Fasta:[/] {self.args.genome.name} [italic bright_black]({self.args.genome})[/]")
        self.checkGenomeFasta()


    def checkWorkingDirectory(self):
        import shutil

        # Si el directorio existe, lo borramos
        if self.args.tmpDirectory.exists():
            rprint(f"\t[bold bright_red]Working directory already exists![/] Deleting directory")
            shutil.rmtree(f"{self.args.tmpDirectory}")

        # Creando directorio
        rprint(f"\t[bold]Creating {self.args.tmpDirectory.name} directory.[/]")
        os.mkdir(f"{self.args.tmpDirectory}")


    def checkOutputFile(self):
        import os

        if self.args.output.exists():
            os.remove(f"{self.args.output}")

    def checkQueryFasta(self):
        pass


    def checkGenomeFasta(self):
        pass
