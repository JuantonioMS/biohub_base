from pathlib import Path

from biohub.process import Process

class Load(Process):

    """
    Proceso para realizar una carga de un fichero sobre un sujeto
    """
    
    def setInputs(self, **kwargs):
        return super().setInputs(**kwargs)
    
    def setOutputs(self, *args, **kwargs):
        return super().setOutputs(*args, **kwargs)
    
    def completeProcessAttrs(self, aux=None, processAttrs=...):
        return super().completeProcessAttrs(aux, processAttrs)
    
    def recordProcess(self, inputs, outputs, **kwargs):
        return super().recordProcess(inputs, outputs, **kwargs)
    
    def run(self, inputs: dict = ..., outputsAttrs: dict = ..., options: dict = ..., processAttrs: dict = ...):
        return super().run(inputs, outputsAttrs, options, processAttrs)


    def run(self,
            file: Path,
            processAttrs: dict = {},
            fileAttrs: dict = {}) -> None:


        if not isinstance(file, Path):
            file = Path(file)

        if file.exists():

            if "backgrounds" in processAttrs:
                processAttrs["backgrounds"].append("load single")
            else:
                processAttrs["backgrounds"] = ["load single"]

            output = self.setOutput("".join(file.suffixes), **fileAttrs)

            self.runCommand(f"cp {file} {Path(self.subject.path, output.path)}")


            if self.record:
                self.recordProcess([file], [output], **processAttrs)