from pathlib import Path

from biohub.process import Process

class Load(Process):

    """
    Proceso para realizar una carga de un fichero sobre un sujeto
    """


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