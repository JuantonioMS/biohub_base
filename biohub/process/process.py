import subprocess
from tabnanny import check
from biohub.file import File

from biohub.utils import GeneralClass
from biohub.file import File


from collections import namedtuple

FilePair = namedtuple("FilePair", ["orginal", "biohub"])

class Process(GeneralClass):

    def __init__(self,
                 test = False,
                 record = True,
                 threads = 4,
                 subject = None,
                 **kwargs):

        self.test = test
        self.record = record
        self.threads = threads
        self.subject = subject

        if not hasattr(self, "id"):
            self.id = self.newId()

        if not hasattr(self, "date"):
            self.date = self.newDate()

        super().__init__(**kwargs)


    def newId(self, buffer = []):
        return "bhPR" + super().newId(buffer)


    #  --------------------Run methods--------------------

    def runCondaPackage(self,
                        *args,
                        env: str = "base"):

        #  Búsqueda del shell de conda instalado en el sistema
        for element in subprocess.getoutput("which conda").split("/"):
            if "conda3" in element: condaShell = element

        #  Ruta completa a la shell de conda
        condaShell = f"~/{condaShell}/etc/profile.d/conda.sh"

        # Montando la llamada al paquete junto a la inicializacion de la shell y el entorno
        commandLine = " && ".join([f"{condaShell}"] + [f"conda activate {env}"] + list(args))

        if self.test:
            print(commandLine)

        else:
            print(commandLine)
            subprocess.call(f". {commandLine}",
                            shell = True,
                            executable = "/bin/bash")


    def runCommand(self, command: str) -> None:

        if self.test:
            print(command)

        else:
            subprocess.call(command, shell = True, executable = "/bin/bash")


    #  --------------------API run methods--------------------


    def selectInput(self,
                    backgrounds = [],
                    date = "latest",
                    processes = [],
                    id = "",
                    comment = "",
                    method = "order",
                    order = []):

        candidates = []

        if method != "order":

            if method == "backgrounds":

                for background in backgrounds:

                    if not candidates:
                        candidates = [file for file in self.subject.files.values() if background in file.backgrounds]
                    else:
                        candidates = [file for file in candidates if background in file.backgrounds]

            elif method == "date":
                pass # TODO

            elif method == "processes":

                for process in processes:

                    if not candidates:
                        candidates = [file for file in self.subject.files.values() if process in file.processes]
                    else:
                        candidates = [file for file in candidates if process in file.processes]

            elif method == "id":

                candidates = [file for file in self.subject.files.values() if id in file.id]

            elif method == "comment":

                candidates = [file for file in self.subject.files.values() if comment in file.comments]

            else:
                raise ValueError(f"{method} is not a valid method")

        else: #  Método por orden
            pass # TODO


        if len(candidates) != 1:
            raise ValueError(f"There are {len(candidates)} with that characteristic")
        else:
            return self.subject.files[candidates[0].id]


    def setInputs(self, **kwargs):
        pass


    def selectOutput(self, extension: str, **kwargs) -> File:

        kwargs["id"] = self.newId()
        kwargs["date"] = self.newDate()

        kwargs["path"] = "files/" + self.newId() + extension

        kwargs["processes"] = [self.id]

        return File(**kwargs)


    def setOutputs(self, *args, **kwargs):
        pass


    def runProcess(self, inputs, outputs, options):
        pass


    def processOptions(self, **kwargs):

        options = []

        for key, value in kwargs.items():
            options.append(key)
            if value:
                options.append(value)

        return " ".join(options)

    def recordProcess(self, inputs, outputs, **kwargs):

        self.tool = type(self).__name__ #  Nombre de la herramienta

        self.name = self.__class__.__bases__[0].__name__.lower() #  Nombre del proceso
        if self.name == "process": #  Si es una clase "por defecto" el nombre cambia al de la herramienta directamente
            self.name = self.tool.lower()

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.inputs = []

        for input in inputs.values():
            if isinstance(input, File):
                self.subject.files[input.id].processes.append(self.id)
                self.inputs.append(input.id)
            else:
                self.inputs.append(str(input))

        self.outputs = []

        for _, output in outputs:
            if isinstance(output, File):
                self.subject.files[output.id] = output
                self.outputs.append(output.id)
            else:
                self.outputs.append(str(output))

        self.subject.processes[self.id] = self


    def checkProcess(self):
        return True


    def completeProcessAttrs(self, aux = None, processAttrs = {}):

        return self.updateDictAttrs(aux = aux, buffer = processAttrs)


    def run(self,
            inputs: dict = {},
            outputsAttrs: dict = {},
            options: dict = {},
            processAttrs: dict = {}):

        inputs = self.setInputs(**inputs)

        options = self.processOptions(**options)

        outputs = self.setOutputs(options, **outputsAttrs)


        self.runProcess(inputs, outputs, options)

        if not self.checkProcess():
            raise ValueError("Process has not been completed successfully")

        if self.record:

            processAttrs = self.completeProcessAttrs(processAttrs = processAttrs)

            self.recordProcess(inputs, outputs, **processAttrs)

        return outputs


    #  --------------------XML methods--------------------


    def avoidAttrs(self):
        return ["threads", "test", "subject", "record"] + super().avoidAttrs()


    def buildXmlElement(self) -> None:

        import xml.etree.ElementTree as ET

        element = ET.Element("process")

        return super().buildXmlElement(element)


    def __str__(self) -> str:
        return f"{self.id}"
