"""
Modulo para el almacenamiento de hits de Blast para el algoritmo Blastn

v.0.1

By: Juan Antonio Marín Sanz
Date: 29/11/2021
Location: Córdoba, Spain
"""

class BlastnHit:

    def __init__(self,
                 name = str(),
                 hitId = int(),
                 hspId = int(),
                 bitScore = float(),
                 score = int(),
                 evalue = float(),
                 gaps = int(),
                 length = int(),
                 queryStart = int(),
                 queryEnd = int(),
                 queryStrand = str(),
                 querySequence = str(),
                 hitSeqId = str(),
                 hitStart = int(),
                 hitEnd = int(),
                 hitStrand = str(),
                 hitSequence = str(),
                 midLine = str()):


        # Identifiación del hit
        self.name = name                # Hit nombre
        self.hitId = int(hitId) # Hit SeqId número
        self.hspId = int(hspId) # Hit número


        # Puntuaciones del hit
        self.score = int(score)       # Score crudo (0->x)
        self.bitScore = float(bitScore) # Score ajustado por Kappa y Lambda (0->x)
        self.evalue = float(evalue)     # Score ajustado por tamaño de query y base de datos (0<-x)


        # Características del hit
        self.gaps = int(gaps)     # Número de huecos
        self.length = int(length) # Longitud del hit


        # Localización de la query respecto al hit
        self.queryStart = int(queryStart) - 1 # Posición nucleótido de comienzo 0-based
        self.queryEnd = int(queryEnd) - 1     # Posición nucleótido de fin 0-based
        self.queryStrand = queryStrand        # Sentido de la query
        self.querySequence = querySequence    # Secuencia de la query

        if self.queryStrand == "Minus":
            self.queryStart, self.queryEnd = self.queryEnd, self.queryStart


        # Localización del hit
        self.hitSeqId = hitSeqId          # SeqId del hit
        self.hitStart = int(hitStart) - 1 # Posición nucleótido de comienzo 0-based
        self.hitEnd = int(hitEnd) - 1     # Posición nucleótido de fin 0-based
        self.hitStrand = hitStrand        # Sentido del hit
        self.hitSequence = hitSequence    # Secuencia del hit

        if self.hitStrand == "Minus":
            self.hitStart, self.hitEnd = self.hitEnd, self.hitStart


        # Secuencia intermedia
        self.midLine = midLine # Relación entre query y hit


    def __str__(self):
        message = f"Hit {self.hitId}:{self.hspId} of {self.name}\n"
        message += f"\tR:{self.score}; B:{self.bitScore}; E:{self.evalue}\n"
        message += f"\tSize {self.length}; Gaps{self.gaps}\n"
        message += f"\tHit {self.hitStart}->{self.hitEnd}({self.hitStrand})\n"
        message += f"\tQuery {self.queryStart}->{self.queryEnd}({self.queryStrand})\n"
        message += f"\tSeqID: {self.hitSeqId}"

        return message

    def __repr__(self):
        return str(self)