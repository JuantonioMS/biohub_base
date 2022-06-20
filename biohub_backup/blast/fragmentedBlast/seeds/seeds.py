from pathlib import Path
from rich.progress import Progress

from biohub.sequences.fasta import Fasta


class Seeds:

    def __init__(self, query, args, sample):

        self.query = query
        self.args = args

        self.sample = sample

        self.seeds, self.complete = self.fragmentQueries()

    def fragmentQueries(self):

        result = dict()

        seqIds, seqs = [], []

        with Progress() as progress:

            # Creando la tarea principal
            mainTask = progress.add_task("[bold bright_magenta]Total querys[/]...", total = len(self.query.content))

            # Crando las tareas por query
            subTasks = [progress.add_task(f"[bold magenta]{query}[/]...",
                                          total = len(list(range(0,
                                                                 len(sequence) + 1 - self.args.size,
                                                                 self.args.aliasing
                                                                )
                                                           )
                                                     )
                                         )
                       for query, sequence in self.query.content.items()]

            # Iterando por cada query
            for query, task in zip(self.query.content, subTasks):
                sequence =  self.query.content[query]

                seedIDs, seeds = [], []

                # Utilizamos el índice para seccionar las seeds
                # desde el principi0, hasta la longitud de la secuencia menos el tamaño del segmento + 1
                # con el salto del aliasing
                for index in range(0, len(sequence) + 1 - self.args.size, self.args.aliasing):

                    seedIDs.append(f"{query}_Seed_{len(seedIDs) + 1}")
                    seeds.append(sequence[index : index + self.args.size])

                    if "complete" in query:
                        seqIds.append(f"{query}_Seed_{len(seedIDs) + 1}")
                        seqs.append(sequence[index : index + self.args.size])

                    progress.update(task, advance = 1)

                result[query] = Fasta(verbose = False,
                                      file = Path(self.args.tmpDirectory, f"tmp_{self.sample}_{query}.fasta"),
                                      seqIDs = seedIDs,
                                      sequences = seeds)

                progress.update(mainTask, advance = 1)

            all = Fasta(verbose = False,
                        file = Path(self.args.tmpDirectory, f"tmp_{self.sample}.fasta"),
                        seqIDs = seqIds,
                        sequences = seqs)

        return result, all
