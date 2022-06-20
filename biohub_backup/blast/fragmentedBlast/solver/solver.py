from pathlib import Path

from rich import print as rprint

from biohub.blast.fragmentedBlast.puzzle.puzzle import Puzzle


class Solver:

    def __init__(self, blastnSeeds, args, queries):

        self.blastnSeeds = blastnSeeds
        self.args = args
        self.queries = queries

        self.results = self.solve()


    def solve(self):

        results = dict()

        for query, result in self.blastnSeeds.results.items():
            results[query] = self.singleSolve(query, result)

        return results


    def singleSolve(self, query, result):
        puzzle = Puzzle(self.args, self.queries.content[query])

        hits = list(result.results.values())

        movement = 0
        for hit in hits:
            # Hay al menos un hit
            if hit:
                hit = hit[0]
                puzzle.add(hit, movement)

                movement = 0

            # No hay hit para esta seed
            else:
                movement += self.args.aliasing

        return puzzle


    def __str__(self):

        message = []

        for query, solution in self.solutions.items():

            message.append(f"{query}\tSeqID\tStrand\tStart\tEnd\tLength\tTheorical lenght")
            message.append(str(solution))

        return "\n".join(message)

    def __repr__(self):
        return str(self)



    def singleSolve(self, query, result):
        puzzle = Puzzle(self.args, self.queries.content[query])

        hits = list(result.results.values())

        movement = self.args.aliasing
        for hit in hits:
            # Hay al menos un hit
            if hit:
                hit = hit[0]
                puzzle.add(hit, movement)

                movement = self.args.aliasing

            # No hay hit para esta seed
            else:
                movement += self.args.aliasing

        return puzzle