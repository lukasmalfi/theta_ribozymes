#One example ob the parallelized scripts used to analyse metagenomic samples. 60 of those were generated and executed in parallel.

# Import the subprocess module
import subprocess

# Create directories for storing results
inp_start="mkdir /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results/"+str(1)
subprocess.run(inp_start, shell=True)
inp_start="mkdir /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results_seqs/"+str(1)
subprocess.run(inp_start, shell=True)
inp_start="mkdir /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)
subprocess.run(inp_start, shell=True)
inp_start="mkdir /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/trnascan/"+str(1)
subprocess.run(inp_start, shell=True)

# Open a file containing paths to sample files
f=open("wgs_sample_paths.txt")
f_lin=f.readlines()

# Remove newline characters from each line in the file
for i in range(len(f_lin)):
    f_lin[i]=f_lin[i].strip()

# Get the total number of samples and split it into 60 parts
length_total=len(f_lin)
length_part=int(length_total/60)

# Define a function for opening files
def open_fils(filename):
    # Define filepaths for the rnarobo results and fasta files
    filepath="/mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results/"+str(1)+"/"+filename+"_rnarobo_result.txt"
    filepath_fasta="/mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)+"/"+filename+".fa"
    
    # Open the rnarobo results file and read its contents
    f1=open(filepath)
    f_l1=f1.readlines()
    f1.close()
    
    # Create a list to store the names of sequences where a ribozyme was found
    seqnam=[]
    
    # Go through each line of the rnarobo output
    for line in f_l1:
        # If the line starts with two spaces, it contains information about a ribozyme
        if line[0:2]=="  ":
            # Split the line into its components and append the sequence name to the seqnam list
            line=line.strip().split()
            seqnam.append(line[2])
    
    # Get a list of unique sequence names
    unique_seqnam=set(seqnam)
    
    # Create a string to store the sequences
    sequence_saving=""
    
    # Go through each unique sequence name
    for seqnam in unique_seqnam:
        # Use sed to extract the sequence from the fasta file
        inp= "sed -n '/"+seqnam+" /,/>/p' "+filepath_fasta
        l=subprocess.run(inp,shell=True,capture_output=True,text=True)
        
        # If there are multiple sequences with the same name, join them together
        if len(l.stdout.split(">")) > 2:
            sequence_saving+=">".join(l.stdout.split(">")[:-1])
        else:
            sequence_saving+=l.stdout
    
    # Write the sequences to a file
    f2=open("/mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results_seqs/"+str(1)+"/"+filename+"_seqs_rnarobo_result.txt","w")
    f2.write(sequence_saving)
    f2.close

# Go through each sample file
for path in f_lin[length_part*1:length_part*(1+1)]:
    # Extract the file to a new location and unzip it
    name=path.split("/")[-1].split(".")[0]
    ending=path.split("/")[-1].split(".")[-1]
    if ending=="gz":
        inp= "zcat "+path+" >> /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)+"/"+name+".fa"
    elif ending=="bz2":
        inp= "bzip2 -dc "+path+">> /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)+"/"+name+".fa"
    else:
        inp=""
    subprocess.run(inp, shell=True)

    # Run rnarobo to find ribozymes in the sample
    inp2= "/mnt/mnemo6/lukas/anaconda3/bin/rnarobo-2.1.0-linux64 -c --nratio 0.1 /mnt/mnemo6/lukas/Python/ribozymes/version4/motif2_precise.txt /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)+"/"+name+".fa >> /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results/"+str(1)+"/"+name+"_rnarobo_result.txt"
    subprocess.run(inp2, shell=True)

    # Extract the sequences where ribozymes were found and save them to a file
    open_fils(name)

    # Remove the fasta file
    inp3= "rm /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)+"/"+name+".fa"
    subprocess.run(inp3, shell=True)

    # Run tRNAscan to find tRNAs in the sample
    inp4="/mnt/mnemo6/lukas/anaconda3/envs/sar3/bin/tRNAscan-SE -G --detail /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results_seqs/"+str(1)+"/"+name+"_seqs_rnarobo_result.txt -o /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/trnascan/"+str(1)+"/"+name+"trna_result.txt -f /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/trnascan/"+str(1)+"/"+name+"trna_secondary.tbl"
    subprocess.run(inp4, shell=True)
