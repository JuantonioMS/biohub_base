"""
Modulo para la lectura de ficheros XML de Blast para el algoritmo Blastn

v.0.1

By: Juan Antonio Marín Sanz
Date: 29/11/2021
Location: Córdoba, Spain
"""

import xml.dom.minidom

from biohub.blast.blastn.blastnHit import BlastnHit

class BlastnXML:


    def __init__(self, xmlFile):

        self.xmlFile = xmlFile

        self.hits = self.extractHits()


    def extractHits(self):

        xmlFile = xml.dom.minidom.parse(f"{self.xmlFile}")

        name = xmlFile.getElementsByTagName("query-title")[0].childNodes[0].data

        hits = xmlFile.getElementsByTagName("Hit") # Hits recogidos
        auxHits = [] # Buffer sobre los que guardar los hits

        hitId = 1
        for hit in hits:

            seqId = str(hit.getElementsByTagName("title")[0].childNodes[0].data)

            hspId = 1
            hsps = hit.getElementsByTagName("Hsp")

            for hsp in hsps:

                score = int(hsp.getElementsByTagName("score")[0].childNodes[0].data)
                bitScore = float(hsp.getElementsByTagName("bit-score")[0].childNodes[0].data)
                evalue = float(hsp.getElementsByTagName("evalue")[0].childNodes[0].data)

                gaps = int(hsp.getElementsByTagName("gaps")[0].childNodes[0].data)
                length = int(hsp.getElementsByTagName("align-len")[0].childNodes[0].data)

                queryStart = int(hsp.getElementsByTagName("query-from")[0].childNodes[0].data)
                queryEnd = int(hsp.getElementsByTagName("query-to")[0].childNodes[0].data)
                queryStrand = str(hsp.getElementsByTagName("query-strand")[0].childNodes[0].data)
                querySequence = str(hsp.getElementsByTagName("qseq")[0].childNodes[0].data)

                hitStart = int(hsp.getElementsByTagName("hit-from")[0].childNodes[0].data)
                hitEnd = int(hsp.getElementsByTagName("hit-to")[0].childNodes[0].data)
                hitStrand = str(hsp.getElementsByTagName("hit-strand")[0].childNodes[0].data)
                hitSequence = str(hsp.getElementsByTagName("hseq")[0].childNodes[0].data)

                midLine = str(hsp.getElementsByTagName("midline")[0].childNodes[0].data)

                blast = BlastnHit(name = name,
                                  hitId = hitId,
                                  hspId = hspId,
                                  score = score,
                                  bitScore = bitScore,
                                  evalue = evalue,
                                  gaps = gaps,
                                  length = length,
                                  queryStart = queryStart,
                                  queryEnd = queryEnd,
                                  queryStrand = queryStrand,
                                  querySequence = querySequence,
                                  hitSeqId = seqId,
                                  hitStart = hitStart,
                                  hitEnd = hitEnd,
                                  hitStrand = hitStrand,
                                  hitSequence = hitSequence,
                                  midLine = midLine)

                auxHits.append(blast)

                hspId += 1
            hitId += 1

        return auxHits