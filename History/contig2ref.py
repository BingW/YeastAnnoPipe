#coding: utf-8
contigs_path = "/Users/bingwang/Downloads/Skud_CTH/contigsAll/"
output_path = "/Users/bingwang/Downloads/Skud_CTH/Strains/"
import os
species = []
sequence = []
contig_num = []
for item in os.listdir(contigs_path):
    c_num = int(item[item.find("g")+1:item.find(".f")])
    contig_num.append(c_num)
    f = open(contigs_path + item)
    for line in f:
        if line[0] == ">":
            sp = line[1:].replace("\n","")
            try:
                species.index(sp)
            except:
                species.append(sp)
                sequence.append([])
        else:
            sequence[species.index(sp)].append(line)
    f.close()

for sp in species:
    f = open(output_path+sp+".fsa","w")
    for i in range(len(contig_num)):
        if contig_num[i] < 9000:
            f.write(">c"+str(contig_num[i])+" [org=Saccharomyces kudriavzevii] " + 
                "[moltype=genomic] [strain="+sp+"]")
        elif contig_num[i] > 9000:
            f.write(">c"+str(contig_num[i])+" [org=Saccharomyces kudriavzevii] " + 
                "[moltype=genomic] [strain="+sp+"] [note=Contigs 9001, 9002, 9004, and 9080 are present only in Gal+ strains. They are syntenic to the GAL pseudogenes and surrounding regions. Illumina reads from all strains were allowed to assemble to either the functional or pseudogene alleles in these regions, whereas all other contigs had only IFO1802 as the reference strain. For each strain, only one allele is present and leads to significant coverage. See the full Methods in Hittinger et al. 2010 (PMID:20164837) for details.]") 
        f.write("\n")
        f.write(sequence[species.index(sp)][i])
    f.close()
