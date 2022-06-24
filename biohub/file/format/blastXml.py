import xml.etree.ElementTree as ET

from biohub.file import File

class BlastOutput(File):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.tree = ET.parse(self.path)
        self.root = self.tree.getroot()

        self.hsps = self.getAllHsps()

    def getAllHsps(self):

        results = dict()

        for query in self.root.find("BlastOutput_iterations").findall("Iteration"):

            hsps = []

            for hit in query.find("Iteration_hits").findall("Hit"):

                for hsp in hit.find("Hit_hsps").findall("Hsp"):

                    hsps.append(Hsp(query, hit, hsp))

            results[query.find("Iteration_query-def").text] = hsps

        return results


class Hsp:

    def __init__(self, query, hit, hsp):

        self.query = query
        self.hit = hit
        self.hsp = hsp

        self.read()

        self.changes = self.getChanges()

    def read(self):

        self.name = ".".join([self.query.find("Iteration_query-def").text,
                              self.hit.find("Hit_num").text,
                              self.hsp.find("Hsp_num").text])

        self.contig = self.hit.find("Hit_def").text

        self.bitScore = self.hsp.find("Hsp_bit-score").text
        self.score = self.hsp.find("Hsp_score").text
        self.eValue = self.hsp.find("Hsp_evalue").text

        self.queryFrom = int(self.hsp.find("Hsp_query-from").text)
        self.queryTo = int(self.hsp.find("Hsp_query-to").text)
        self.queryFrame = int(self.hsp.find("Hsp_query-frame").text)

        self.hitFrom = int(self.hsp.find("Hsp_hit-from").text)
        self.hitTo = int(self.hsp.find("Hsp_hit-to").text)
        self.hitFrame = int(self.hsp.find("Hsp_hit-frame").text)

        self.queryLen = int(self.query.find("Iteration_query-len").text)
        self.hitLen = int(self.hsp.find("Hsp_align-len").text)

        self.matches = int(self.hsp.find("Hsp_identity").text)
        self.misMatches = self.queryLen - self.matches
        self.gaps = int(self.hsp.find("Hsp_gaps").text)

        self.concordance = self.matches / self.queryLen * 100

        self.querySequence = self.hsp.find("Hsp_qseq").text
        self.hitSequence = self.hsp.find("Hsp_hseq").text
        self.midSequence = self.hsp.find("Hsp_midline").text

    def getChanges(self):

        changes = []

        for index in range(len(self.midSequence)):

            if self.midSequence[index] == " ":
                changes.append(f"{index + 1}{self.querySequence[index]} -> {index + 1}{self.hitSequence[index]}")

        return changes


    def printChanges(self, length = 60):

        for index in range(0, len(self.midSequence), length):

            print(self.querySequence[index : index + length] + f"    {index + 1}-{index + length}",
                  self.midSequence[index : index + length],
                  self.hitSequence[index : index + length],
                  sep = "\n",
                  end = "\n\n")