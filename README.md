# gensept parser

This CLI tool converts a *.gp format file to a *.fas format file with shorter, but still accurate headers for sequence.
The tool is able to process multiple records in one *.gp file.

For example:
>H.sapiens-386828-INS
MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN

stands for:
gi: 386828
organism: Homo sapiens
gene name: INS
sequence: MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN


Usage: python gp2fasta.py [--help] <input_file.gp> [--id gi/locus] [-f 0|1|2] [--genename] [-s separator] [-a]
<input_file.gp>  Input file in GenPept format

Arguments:
  --id gi/locus    Specify identifier type (default: locus)
  -f 0|1|2         Format of organism name selection (default: 0) 
                    0: Abbreviated gene name in shorthand (e.g. H. sapiens).
                    1: Gene name in full species shorthand (e.g. HomSap).
                    2: Full species name (e.g. Homo sapiens).
  --genename       Include gene name in output
  -s separator     Specify separator character (default: '-')
  -a               Enable including additional informations:
                      P -> PREDICTED
                      s -> similar
                      h -> hypothetical protein
                      u -> unnamed protein product
                      n -> novel
                      p -> putative
                      o -> open reading frame
  --help           Show help message
