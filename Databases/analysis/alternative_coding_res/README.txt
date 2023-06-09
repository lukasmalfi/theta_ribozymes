use prodigal to predict protein copding genes for genetic code 11 (standart) and 15

prodigal -d output.fasta -g 11 -i ../combined_all_viral_sequences_v2.fasta -o res.txt -s startfile.txt -a proteins.faa

# -c would be for closed edges (dont allow genes to run outside)

prodigal -d output15.fasta -g 15 -i ../combined_all_viral_sequences_v2.fasta -o res15.txt -s startfile15.txt -a proteins15.faa


prodigal -d output4.fasta -g 4 -i ../combined_all_viral_sequences_v2.fasta -o res4.txt -s startfile4.txt -a proteins4.faa


 python3 get_CD.py -sc ../combined_all_viral_sequences_v2.fasta -o output -c4 proteins4.faa -c11 proteins.faa -c15 proteins15.faa 