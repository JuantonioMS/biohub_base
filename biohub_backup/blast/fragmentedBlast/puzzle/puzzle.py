"""
Modulo para el almacenamiento de hits de Blast para el algoritmo Blastn

v.0.1

By: Juan Antonio Marín Sanz
Date: 29/11/2021
Location: Córdoba, Spain
"""

from biohub.blast.fragmentedBlast.puzzle.piece import Piece

class Puzzle:

    def __init__(self, args, query):

        self.query = query
        self.args = args
        self.puzzle = []


    def add(self, hit, movement):

        if len(self.puzzle) == 0:
            piece = Piece(seqID = hit.hitSeqId,
                          strand = hit.hitStrand,
                          start = hit.hitStart,
                          end = hit.hitEnd)

            self.puzzle.append(piece)


        # Si ya hay al menos una pieza en el puzzle
        else:
            template = self.puzzle[-1]

            # Si se puede extender la pieza existente con el nuevo hit
            if template.canExtend(hit, self.args, movement):
                template.extend(hit)
                self.puzzle[-1] = template

            # Si no se puede
            else:
                piece = Piece(seqID = hit.hitSeqId,
                              strand = hit.hitStrand,
                              start = hit.hitStart,
                              end = hit.hitEnd)
                self.puzzle.append(piece)


    def __str__(self):
        message = []

        for index, piece in enumerate(self.puzzle):
            message.append(f"Segment {index + 1}\t{piece.seqID}\t{piece.strand}\t{piece.start}\t{piece.end}\t{piece.end - piece.start + 1}\t{len(self.query)}")

        return "\n".join(message)

    def __repr__(self):
        return str(self)