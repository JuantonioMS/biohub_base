from pathlib import Path

from biohub.process import Process

class LoadLinked(Process):

    """
    Proceso para realizar una carga de un fichero sobre un sujeto
    """


    def run(self,
            subject,
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

            processAttrs["inputs"] = [str(file)]

            super().run(**processAttrs)

            output = self.setOutput("".join(file.suffixes), **fileAttrs)
            self.outputs = [output.id]

            self.runCommand(f"cp {file} {Path(subject.path, output.path)}")

            self.endRun(subject, [output])