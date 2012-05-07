#coding: utf-8
import os
def gene_id(arg,fsa_file):
#TODO test whether geneid is installed
    cmd = "geneid -"
    cmd += "b" if arg["Output_Start_codon"] == True else ""
    cmd += "d" if arg["Output_Donor_splice_sites"] == True else ""
    cmd += "a" if arg["Output_Acceptor_splice_sites"] == True else ""
    cmd += "e" if arg["Output_Stop_codons"] == True else ""
    cmd += "f" if arg["Output_Initial_exons"] == True else ""
    cmd += "i" if arg["Output_Internal_exons"] == True else ""
    cmd += "t" if arg["Output_Terminal_exons"] == True else ""
    cmd += "n" if arg["Output_introns"] == True else ""
    cmd += "x" if arg["Output_all_predicted_exons"] == True else ""
    cmd += "s" if arg["Output_Single_genes"] == True else ""
    cmd += "z" if arg["Output_Open_Reading_Frames"] == True else ""
    cmd += "r" if arg["Use_recursive_splicing"] == True else ""
    cmd += "u" if arg["Turn_on_UTR_prediction"] == True else ""
    #Only valid with -S option: HSP/EST/short read ends are used to determine UTR ends

    print cmd
'''
		[-TDAZU]
		[-p gene_prefix]
		[-G] [-3] [-X] [-M] [-m]
		[-WCF] [-o]
		[-j lower_bound_coord]
		[-k upper_bound_coord]
		[-N numer_nt_mapped]
		[-O <gff_exons_file>]
		[-R <gff_annotation-file>]
		[-S <gff_homology_file>]
		[-P <parameter_file>]
		[-E exonweight]
		[-V evidence_exonweight]
		[-Bv] [-h]
		<locus_seq_in_fasta_format>

	-T: Output genomic sequence of exons in predicted genes
	-D: Output genomic sequence of CDS in predicted genes
	-A: Output amino acid sequence derived from predicted CDS

	-p: Prefix this value to the names of predicted genes, peptides and CDS

	-G: Use GFF format to print predictions
	-3: Use GFF3 format to print predictions
	-X: Use extended-format to print gene predictions
	-M: Use XML format to print gene predictions
	-m: Show DTD for XML-format output 

	-j  <coord>: Begin prediction at this coordinate
	-k  <coord>: End prediction at this coordinate
	-N  <num_reads>: Millions of reads mapped to genome
	-W: Only Forward sense prediction (Watson)
	-C: Only Reverse sense prediction (Crick)
	-U: Allow U12 introns (Requires appropriate U12 parameters to be set in the parameter file)
	-F: Force the prediction of one gene structure
	-o: Only running exon prediction (disable gene prediction)
	-O  <exons_filename>: Only running gene prediction (not exon prediction)
	-Z: Activate Open Reading Frames searching

	-R  <exons_filename>: Provide annotations to improve predictions
	-S  <HSP_filename>: Using information from protein sequence alignments to improve predictions

	-E: Add this value to the exon weight parameter (see parameter file)
	-V: Add this value to the score of evidence exons 
	-P  <parameter_file>: Use other than default parameter file (human)

	-B: Display memory required to execute geneid given a sequence
	-v: Verbose. Display info messages
	-h: Show this help
        
    
'''
arg = {}
arg["Output_Start_codon"] = True
gene_id(arg,"afile")
