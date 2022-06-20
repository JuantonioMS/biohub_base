import argparse
from pathlib import Path
import shutil
import os
from difflib import ndiff
from typing import Match

def similar(str1, str2):
    if str1 == str2:
        return set()
    else:
        differences = [dif[2:] for dif in ndiff(str1, str2) if dif[0] != " "]
        return set(differences)

def check(parent, sons):

    for index in range(len(parent)):
        candidates = []
        for son in sons:
            if son[:index] == parent[:index]:
                pass
            else:
                candidates.append(son)

        if candidates:
            for candidate in candidates:
                sons.remove(candidate)

            candidates = []

        if len(sons) == 1:
            break

    return sons




def run(args):

    args.input = Path(args.input).resolve()

    # Chequeo del directorio de salida
    if Path(args.output).exists():
        args.output = Path(args.output).resolve()
        shutil.rmtree(f"{args.output}")
    os.system(f"mkdir {args.output}")

    # Guardando todos los fastqs
    fastqs = [Path(args.input, fastq) for fastq in os.listdir(f"{args.input}") if not Path(args.input, fastq).is_dir()]
    fastqs.sort()

    fastqPairs = set()
    for fastq in fastqs:

        potentialMatch = []
        for brother in fastqs:
            differences = similar(str(fastq), str(brother))

            # Que se diferencien solo en los caracteres 1 y 2
            if len(differences) == 2:
                if "1" in differences and "2" in differences:
                    potentialMatch.append(brother)

        # En caso de que haya más de un posible match para la secuencia pareada
        if len(potentialMatch) != 1:
            potentialMatch = check(str(fastq), [str(p) for p in potentialMatch])
            potentialMatch = [Path(p) for p in potentialMatch]

        # En caso de que no se haya encontrado el archivo pareado
        if len(potentialMatch) != 1:
            print("No se ha encontrado un match correcto para la secuencia pareada!!!")
            raise ValueError

        # Nos quedamos con el unico elmento, ya que sino nos saltaría un error
        match = potentialMatch[0]

        pair = [f"{fastq}", f"{match}"]
        pair.sort()
        pair = tuple(pair)
        fastqPairs.add(pair)


    fastqPairs = list(fastqPairs)
    for pair in fastqPairs:
        forward = Path(pair[0])
        reverse = Path(pair[1])

        os.system(f"unicycler -1 {forward} -2 {reverse} -o {args.output}/tmp -t 10 --keep 0")
        os.system(f"cp {args.output}/tmp/assembly.fasta {args.output}/{forward.name.split('.')[0]}.fasta")
        shutil.rmtree(f"{args.output}/tmp")


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
