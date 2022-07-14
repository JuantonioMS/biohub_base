from pathlib import Path

from biohub.process import Process

class Load(Process):

    """
    Proceso para realizar una carga de un fichero sobre un sujeto
    """

    def setOutputs(self, options = {}, inputs = {}, **kwargs):

        outputs = []

        if len(inputs) > 1:
            background = ["loaded single"]
        else:
            background = ["loaded linked"]

        for input in inputs:

            if input not in [" ", "_", ".", ","]:
                extraAttrs = input.split(";") #  La informacion recogida en la key se almacena
            else:
                extraAttrs = []


            output = self.selectOutput("".join(inputs[input].suffixes),
                                       **self.updateDictAttrs(aux = {"backgrounds" : background + extraAttrs},
                                                              buffer = kwargs))

            outputs.append(output)

        return outputs


    def runProcess(self, options = {}, inputs = {}, outputs = []):

        for input, output in zip(inputs.values(), outputs):
            self.runCommand(f"cp {input} {Path(self.subject.path, output.path)}")


    def completeProcessAttrs(self, processAttrs):

        aux = {"backgrounds" : ["load"]}

        return super().completeProcessAttrs(aux = aux, processAttrs = processAttrs)