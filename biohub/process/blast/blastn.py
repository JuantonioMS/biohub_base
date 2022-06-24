from pathlib import Path

from biohub.process import Process

class Blastn(Process):


    def setInputs(self, **kwargs):

        if "database" in kwargs:
            kwargs["database"] = self.assertPath(kwargs["database"])

        else:
            kwargs["database"] = self.selectInput(backgrounds = ["assembly"],
                                                  method = "backgrounds")

        if "query" in kwargs:
            kwargs["query"] = self.assertPath(kwargs["query"])
        else:
            kwargs["query"] = self.selectInput(backgrounds = ["query"],
                                               method = "backgrounds")

        return kwargs





    def setOutputs(self, *args, **kwargs):
        return super().setOutputs(*args, **kwargs)




    def run(self,
            database = None,
            query = None,
            deleteIndex = True):

        if not database:
            database = self.selectInput(backgrounds = ["assembly"],
                                        method = "backgrounds")

        if not query:
            query = self.selectInput(backgrounds = ["query"],
                                     method = "backgrounds")

        auxDatabase = Path(self.subject.path, "files/blast_tmp_database.db")

        if len(list(filter(lambda x: "blast_tmp_database.db" in str(x), auxDatabase.parent.iterdir()))) == 0:

            self.runCondaPackage(f"makeblastdb -in {self.subject.path}/{database} -dbtype nucl -out {auxDatabase}",
                                 env = "biohub.blast")

        output = self.setOutput(extension = ".tsv", backgrounds = ["blastn", "aligment"])
        self.runCondaPackage(f"blastn -outfmt 6 -db {auxDatabase} -query {query} -out {self.subject.path}/{output}",
                             env = "biohub.blast")

        if deleteIndex:
            self.runCommand(f"rm {auxDatabase}.*")

        if self.record:
            self.recordProcess([database, query], [output], backgrounds = ["blast", "blastn", "aligment"])