from pathlib import Path
from biohub.sequences.fasta import Fasta
from rich import print as rprint

class SequenceWrapper:

    def __init__(self, genome, blast, args):

        self.genome = genome
        self.blast = blast
        self.args = args

        self.fasta = self.search()

    def search(self):

        seqIds, sequences = [], []

        for query, result in self.blast.results.items():

            if result:
                result = result[0]
                rprint(result, end = "\n\n")

                if self.args.window > result.hitStart:
                    print("Aqui se modifica")
                    left = 0
                else:
                    left = result.hitStart - self.args.window




                completeSequence = self.genome.content[result.hitSeqId][left : result.hitEnd + self.args.window + 1]
                singleSequence = self.genome.content[result.hitSeqId][result.hitStart : result.hitEnd + 1]

                upSequence = self.genome.content[result.hitSeqId][left : result.hitStart]
                downSequence = self.genome.content[result.hitSeqId][result.hitEnd + 1 : result.hitEnd + self.args.window + 1]

                if result.hitStrand == "Minus":
                    upSequence, downSequence = downSequence, upSequence


                seqIds.append(f"{query}__single")
                sequences.append(f"{singleSequence}")
                seqIds.append(f"{query}_complete")
                sequences.append(f"{completeSequence}")

                if upSequence:
                    seqIds.append(f"{query}_up")
                    sequences.append(f"{upSequence}")

                if downSequence:
                    seqIds.append(f"{query}_down")
                    sequences.append(f"{downSequence}")

        return Fasta(verbose = True,
                     file = Path(self.args.tmpDirectory, f"tmp_{self.genome.file.stem}.fasta"),
                     seqIDs = seqIds,
                     sequences = sequences)