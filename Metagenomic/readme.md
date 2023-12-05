Here we analyze the metagenomic samples for the presence of Theta ribozymes, as well as tRNAs.

The following files are required:

motif2_precise.txt: The desciptor file for rnaRobo to identify Theta ribozymes.

wgs_sample_paths: The sample paths of all samples that should be analyzed.

example_scipt.py: Fullworkflow, which opens .gz or .bz samples from the above metnioned file, searches them with rnaRobo, then cuts out the contig/region in whcih a Theta ribozyme was detected and searches this region for tRNAs with tRNAscan-SE (due to computational time constraints).

The paths will need to be adjusted to your system/folder structure.
