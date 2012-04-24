#coding: utf-8
import os
def gene_id(arg,fsa_file):
#TODO test whether geneid is installed
    cmd = "geneid "
    cmd += "b" if arg["Output_Start_codon"] == True else ""
    print cmd
'''
geneid	[-bdaefitnxszru]
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
    
'''
arg["O"]
gene_id()
