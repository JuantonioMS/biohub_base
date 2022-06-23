from curses import KEY_A1
from pathlib import Path
from turtle import back

from click import option

from biohub.process import FilePair
from biohub.process import Process

class ResFinder(Process):


    def setInputs(self, **kwargs):

        if kwargs: #  Se ha introducido un input manual
            pass

        else: #  Selección automática

            try:
                database = self.selectInput(backgrounds = ["assembly"],
                                        method = "backgrounds")

                return {"database" : database}

            except ValueError:
                raise ValueError("TODO")


    def setOutputs(self, options, **kwargs):

        outputs = []

        backgrounds = ["annotation", "gene resistance"]

        if "-c" in options or "--point" in options:
            pass

        if "-acq" in options or "--acquired" in options:

            outputs.append(FilePair("pheno_table.txt",
                                    self.selectOutput(".txt",
                                                      **self.updateDictAttrs(aux = {"backgrounds" : ["pheno table"] + backgrounds},
                                                                             buffer = kwargs))))

            outputs.append(FilePair("ResFinder_Hit_in_genome_seq.fsa",
                                    self.selectOutput(".fasta",
                                                      **self.updateDictAttrs(aux = {"backgrounds" : ["ResFinder Hit in genome seq"] + backgrounds},
                                                                             buffer = kwargs))))

            outputs.append(FilePair("ResFinder_Resistance_gene_seq.fsa",
                                    self.selectOutput(".fasta",
                                                      **self.updateDictAttrs(aux = {"backgrounds" : ["ResFinder Resistance gene seq"] + backgrounds},
                                                                             buffer = kwargs))))

            outputs.append(FilePair("ResFinder_results.txt",
                                    self.selectOutput(".txt",
                                                      **self.updateDictAttrs(aux = {"backgrounds" : ["ResFinder results"] + backgrounds},
                                                                             buffer = kwargs))))

            outputs.append(FilePair("ResFinder_results_tab.txt",
                                    self.selectOutput(".txt",
                                                      **self.updateDictAttrs(aux = {"backgrounds" : ["ResFinder results tab"] + backgrounds},
                                                                             buffer = kwargs))))

            outputs.append(FilePair("ResFinder_results_table.txt",
                                    self.selectOutput(".txt",
                                                      **self.updateDictAttrs(aux = {"backgrounds" : ["ResFinder results table"] + backgrounds},
                                                                             buffer = kwargs))))

            outputs.append(FilePair("std_format_under_development.json",
                                    self.selectOutput(".json",
                                                      **self.updateDictAttrs(aux = {"backgrounds" : ["std format under development"] + backgrounds},
                                                                             buffer = kwargs))))

        for _, output in outputs:
            output.links = [aux.id for _, aux in outputs if aux.id != output.id]

        return outputs


    def completeProcessAttrs(self, processAttrs):

        aux = {"backgrounds" : ["annotation", "gene resistance"]}

        return super().completeProcessAttrs(aux = aux, processAttrs = processAttrs)


    def runProcess(self, inputs, outputs, options):

        tmpDir = Path(self.subject.path, "files/tmp")

        print(inputs)

        self.runCondaPackage(" ".join(["run_resfinder.py",                               #  Línea de llamada al programa
                                       f"-ifa {self.subject.path}/{inputs['database']}", #  Línea de input
                                       options,                                          #  Línea de opciones
                                       f"-o {tmpDir}"]),                                 #  Línea para la salida
                             env = "biohub.resfinder")

        for original, output in outputs:

            self.runCommand(f"cp {tmpDir}/{original} {self.subject.path}/{output}")

        self.runCommand(f"rm -rf {tmpDir}")


    def run(self,
            inputs: dict = {},
            outputsAttrs: dict = {},
            options: dict = {"-acq" : ""},
            processAttrs: dict = {}):

        return super().run(inputs, outputsAttrs, options, processAttrs)