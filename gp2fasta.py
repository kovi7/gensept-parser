#!/usr/bin/env python3
import sys
def parse_genpept(file_path, options):
    with open(file_path, 'r') as file:
        content = file.read()
    
    records = content.split('//\n')  # Splitting multiple records
    fasta_entries = []
    
    for record in records:
        if not record.strip():
            continue
        
        lines = record.split('\n')
        seq_id = "unknown"
        organism = "Unknown"
        definition = "No definition"
        additional_info = ""
        gene_name = "unknown"
        sequence = ""
        
        for line in lines:
            if line.startswith("LOCUS"):
                seq_id = line.split()[1] if not options["--id"]=="locus" else seq_id
            elif "GI:" in line:
                seq_id = line.split("GI:")[-1].strip() if options["--id"]=="gi" else seq_id
            elif line.startswith("SOURCE"):
                organism = line.split()
                if options["-f"] == 1:
                    abbrev_org = organism[1][0] + "." + organism[2]
                elif options["-f"] == 2:
                    abbrev_org = organism[1][0:3] + organism[2][0:3]
                else:
                    abbrev_org = organism
            
            elif line.startswith("DEFINITION") and options["-a"]:
                definition = line.split("DEFINITION")[-1].strip()
                if "PREDICTED" in definition: additional_info = "P"
                elif "similar" in definition: additional_info = "s"
                elif "hypothetical" in definition: additional_info = "h"
                elif "unnamed" in definition: additional_info = "u"
                elif "novel" in definition: additional_info = "n"
                elif "putative" in definition: additional_info = "p"
                elif "open reading frame" in definition: additional_info = "o"
            elif "gene=" in line:
                gene_name = line.split("gene=")[-1].replace('"', '')
            elif line.startswith("ORIGIN"):
                sequence = "".join(filter(str.isalpha, "".join(lines[lines.index(line) + 1:]))).upper()
        sep = options["-s"]
        fasta_header = f">{abbrev_org}{sep}{seq_id}"
        if options["--genename"]:
            fasta_header += f"{sep}{gene_name}"
        if options["-a"] and additional_info:
            fasta_header += f"{sep}{additional_info}"
        fasta_entries.append(f"{fasta_header}\n{sequence}")
    
    return "\n".join(fasta_entries)


def main():
    if len(sys.argv) < 2:
        print("To see a manual, type: python gp2fasta.py --help")
        sys.exit(1)

    elif "--help" in sys.argv:
        print("Usage: python gp2fasta.py [--help] <input_file.gp> [--id gi/locus] [-f 0|1|2] [--genename] [-s separator] [-a] \n" 
                "<input_file.gp>  Input file in GenPept format \n\n"
                "Arguments: \n"
                "--id gi/locus    Specify identifier type (default: locus)\n"
                "-f 0|1|2         Format of organism name selection (default: 0) \n"
                "                    0: Abbreviated gene name in shorthand (e.g. H. sapiens). \n"
                "                    1: Gene name in full species shorthand (e.g. HomSap). \n"
                "                    2: Full species name (e.g. Homo sapiens). \n"
                "--genename       Include gene name in output \n"
                "-s separator     Specify separator character (default: '-') \n"
                "-a               Enable including additional informations: \n"
                "                    P -> PREDICTED \n"
                "                    s -> similar \n"
                "                    h -> hypothetical protein \n"
                "                    u -> unnamed protein product \n"
                "                    n -> novel \n"
                "                    p -> putative \n"
                "                    o -> open reading frame \n"
                "--help           Show this help message")
        sys.exit(0)


    input_file = sys.argv[1]
    options = {
        "--id": "locus",
        "-f": 0,
        "--genename": False,
        "-s": "-",
        "-a": False}
    
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        key = args[i]

        if key in ["--id", "-f", "-s"]: 
            if i + 1 >= len(args): 
                print(f"Błąd: Argument {key} wymaga wartości.")
                sys.exit(1)
            if key == "-f":
                options[key] = int(args[i + 1]) 
            else:
                options[key] = args[i + 1]
            i += 2  

        elif key in ["--genename", "-a"]: 
            options[key] = True
            i += 1  

        else:
            print(f"Nieznana opcja: {key}")
            sys.exit(1)
    
    output_file = input_file.replace('.gp', '.fas')
    gp2 = parse_genpept(input_file, options)
    
    with open(output_file, 'w') as file:
        file.write(gp2)
    
    print(f"Conversion completed. Output saved to {output_file}")


if __name__ == "__main__":
    main()
