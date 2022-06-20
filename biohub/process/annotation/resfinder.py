from pathlib import Path

from biohub.process import Process

class ResFinder(Process):

    def run(self,
            database = None):

        if not database:
            database = self.selectInput(backgrounds = ["assembly"],
                                        method = "backgrounds")

        tmpDir = Path(self.subject.path, "files/tmp")

        self.runCondaPackage(f"run_resfinder.py -ifa {self.subject.path}/{database} -acq -o {tmpDir}",
                             env = "biohub.resfinder")

        info = ["annotation", "gene resistance"]

        outputs = []
        for file in tmpDir.iterdir():
            if not file.is_dir():
                output = self.setOutput(file.suffix,
                                        backgrounds = [file.stem] + info)

                self.runCommand(f"cp {file} {self.subject.path}/{output}")

                outputs.append(output)

        self.runCommand(f"rm -rf {tmpDir}")

        for ouput in outputs:
            output.links = [file.id for file in outputs if file.id != output.id]


        if self.record:
            self.recordProcess([database], outputs, backgrounds = ["annotation", "gene resistance"])