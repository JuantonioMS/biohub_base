import argparse
from pathlib import Path
import shutil
import os



def run(args):

    args.input = Path(args.input).resolve()

    # Chequeo del directorio de salida
    if Path(args.output).exists():
        args.output = Path(args.output).resolve()
        shutil.rmtree(f"{args.output}")
    os.system(f"mkdir {args.output}")

    # Guardando todos los fastas
    fastas = [Path(args.input, fasta) for fasta in os.listdir(f"{args.input}")]

    # Llamando al programa para los mlst
    for fasta in fastas:
        print(".............")
        os.system(f"mlst --csv {fasta} > {args.output}/{fasta.stem}.csv")

    # Juntando los resultados en un solo fichero
    os.system(f"{args.output}/*.csv > {args.output}/global.tsv")
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
