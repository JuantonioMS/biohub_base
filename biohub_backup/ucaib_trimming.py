import argparse
from pathlib import Path
import shutil
import os
from difflib import SequenceMatcher

def similar(str1, str2):
    if str1 == str2:
        return 0
    else:
        return SequenceMatcher(None, str1, str2).ratio()


def run(args):

    args.input = Path(args.input).resolve()

    # Chequeo del directorio de salida
    if Path(args.output).exists():
        args.output = Path(args.output).resolve()
        shutil.rmtree(f"{args.output}")
    os.system(f"mkdir {args.output}")

    # Guardando todos los fastqs
    fastqs = [Path(args.input, fastq) for fastq in os.listdir(f"{args.input}")]

    fastqPairs = set()
    for fastq in fastqs:
        """
        similarityValues = [similar(f"{fastq}", f"{brother}") for brother in fastqs]
        bestMatchIndex = similarityValues.index(max(similarityValues))

        brother = fastqs[bestMatchIndex]
        pair = [f"{fastq}", f"{brother}"]
        pair.sort()
        pair = tuple(pair)
        fastqPairs.add(pair)
        """
        
        # Caso de Irene
        name = str(fastq).strip(".fastq.gz")[:-1]
        pair = (f"{name}1.fastq.gz", f"{name}2.fastq.gz")
        fastqPairs.add(pair)

    fastqPairs = list(fastqPairs)
    for pair in fastqPairs:
        forward = pair[0]
        reverse = pair[1]

        print(forward)
        print(reverse)
        print("...........")
        os.system(f"trim_galore -j 4 --paired -o {args.output} {forward} {reverse}")

    # Juntando los resultados en un solo fichero
    #os.system(f"{args.output}/*.csv > {args.output}/global.tsv")
    # Borrando los ficheros temporales
    #os.system(f"rm {args.output}/*.csv")



def main():

    parser = argparse.ArgumentParser(description = "Búsqueda de secuencia en genomas, tanto completas como quebradas.")

    #  Parámetros posicionales
    #  Secuencia a buscar en un archivo fasta
    parser.add_argument("input",
                        help = "Directorio con los archivos Fasta con los genomas")

    parser.add_argument("output",
                        help = "Directorio de salida para guardar los resultados")

    args = parser.parse_args()

    run(args)

if __name__ == "__main__":
    main()
