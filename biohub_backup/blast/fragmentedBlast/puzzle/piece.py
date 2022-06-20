"""
Modulo para el almacenamiento de hits de Blast para el algoritmo Blastn

v.0.1

By: Juan Antonio Marín Sanz
Date: 29/11/2021
Location: Córdoba, Spain
"""

class Piece:

    def __init__(self, seqID = str(),
                       strand = str(),
                       start = int(),
                       end = int()):

        # Nombre de la secuencia de referencia
        self.seqID = seqID

        # Cadena en la que se sitúa
        self.strand = strand

        # Información de inicio y fin
        self.start = start
        self.end = end


    def extend(self, hit):

        if self.strand == "Plus":
            self.end = hit.hitEnd # Si es cadena directa, alargamos el final
        else:
            self.start = hit.hitStart # Si es cadena reversa, retrocedemos el comienzo



    def canExtend(self, hit, args, movement):

        # Si el hit que está en el mismo seqID
        if self.seqID == hit.hitSeqId:

            # Si el hit que entra en la misma cadena
            if self.strand == hit.hitStrand:
                if self.strand == "Plus":
                    return self.canExtendPlus(hit, args, movement)
                else:
                    return self.canExtendMinus(hit, args, movement)

            # Si el hit no está en la misma cadena, no podemos extender la pieza
            else:
                return False

        # Si el hit no está en el mismo contig
        else:
            return False


    def canExtendPlus(self, hit, args, movement):

        if self.end < hit.hitEnd <= self.end + args.aliasing + 0 + movement:
            return True
        else:
            return False

        """
        if self.start + movement == hit.hitStart:
            return True
        else:
            return False
        """


    def canExtendMinus(self,hit, args, movement):

        if self.start - 0 - args.aliasing - movement <= hit.hitStart < self.start:
            return True
        else:
            return False

        """
        if hit.hitStart == self.start - movement:
            return True
        else:
            return False
        """

    def __str__(self):
        return f"{self.seqID} {self.start}->{self.end} ({self.strand})"

    def __repr__(self):
        return str(self)