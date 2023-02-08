
import subprocess
inp_start="mkdir /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results/"+str(1)
subprocess.run(inp_start, shell=True)
inp_start="mkdir /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results_seqs/"+str(1)
subprocess.run(inp_start, shell=True)
inp_start="mkdir /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)
subprocess.run(inp_start, shell=True)
inp_start="mkdir /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/trnascan/"+str(1)
subprocess.run(inp_start, shell=True)
f=open("wgs_sample_paths.txt")
f_lin=f.readlines()

for i in range(len(f_lin)):
    f_lin[i]=f_lin[i].strip()

#get the total length_ split it into 60 parts?
length_total=len(f_lin)

length_part=int(length_total/60)

#global_fasta=""
def open_fils(filename):
    #where to save the found sequence locations, to later grep out the fasta stuff
    #or do directly in bash via grep, whats better?
    #global global_fasta
    #locations=[]

    filepath="/mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results/"+str(1)+"/"+filename+"_rnarobo_result.txt"
    filepath_fasta="/mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)+"/"+filename+".fa"
    f1=open(filepath)
    f_l1=f1.readlines()
    f1.close()
    #going thorugh the results in one file: check for start of found seq ("  "), then append the start position, end position, sequencename (important!) and sequence itself
    #counter=0
    #start=[]
    #end=[]
    seqnam=[]
    #sequence=[]
    #go trhough each line of rnarobo output
    for line in f_l1:
        if line[0:2]=="  ":
            line=line.strip().split()
            #start.append(line[0])
            #end.append(line[1])
            seqnam.append(line[2])
            counter=1
        #add the sequence of the ribozyme    
        #elif counter==1:
            #line=line.strip()
            #sequence.append(line)
            #counter=0
    #all reads where a ribozyme was found        
    unique_seqnam=set(seqnam)
    print(unique_seqnam)
    #look for all the 
    sequence_saving=""
    for seqnam in unique_seqnam:
        inp= "sed -n '/"+seqnam+" /,/>/p' "+filepath_fasta
        l=subprocess.run(inp,shell=True,capture_output=True,text=True)
        if len(l.stdout.split(">")) > 2:
            sequence_saving+=">".join(l.stdout.split(">")[:-1])
                    #print(seqnam)
        else:
            sequence_saving+=l.stdout
    f2=open("/mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results_seqs/"+str(1)+"/"+filename+"_seqs_rnarobo_result.txt","w")

    #sequence_saving2=">".join(sequence_saving.split(">")[:-1])
    f2.write(sequence_saving)
    f2.close
    #print(l.stdout)
for path in f_lin[length_part*1:length_part*(1+1)]:

    #extract the file to a new location, unzip it
    name=path.split("/")[-1].split(".")[0]
    ending=path.split("/")[-1].split(".")[-1]
    if ending=="gz":
        inp= "zcat "+path+" >> /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)+"/"+name+".fa"
    elif ending=="bz2":
        #dc to write to stdout and keep original file
        inp= "bzip2 -dc "+path+">> /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)+"/"+name+".fa"
    else:
        inp=""
    #run the decompression, depoedning on which ending we have    
    subprocess.run(inp, shell=True)

    #run rnarobo, with --nratio do exclude the bad quality baseppairs
    inp2= "/mnt/mnemo6/lukas/anaconda3/bin/rnarobo-2.1.0-linux64 -c --nratio 0.1 /mnt/mnemo6/lukas/Python/ribozymes/version4/motif2_precise.txt /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)+"/"+name+".fa >> /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results/"+str(1)+"/"+name+"_rnarobo_result.txt"
    subprocess.run(inp2, shell=True)

    #cutting out sequence and saving that, as well as adding it to global variable global_fasta, which then contains all potential seuqences to scan with trnascan
    open_fils(name)

    inp3= "rm /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/"+str(1)+"/"+name+".fa"
    subprocess.run(inp3, shell=True)
    #sed through the results and cut out interesting parts, save to file? then run trnascan, or in the end?
    inp4="/mnt/mnemo6/lukas/anaconda3/envs/sar3/bin/tRNAscan-SE -G --detail /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/rnarobo_results_seqs/"+str(1)+"/"+name+"_seqs_rnarobo_result.txt -o /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/trnascan/"+str(1)+"/"+name+"trna_result.txt -f /mnt/mnemo6/lukas/Python/ribozymes/phage_samples/v4/trnascan/"+str(1)+"/"+name+"trna_secondary.tbl"
    subprocess.run(inp4, shell=True)
