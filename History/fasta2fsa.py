#codind: utf-8
import os

openfile = "/Users/bingwang/Downloads/Skud_CTH/reference/SkudContig.fasta.CTH"
writefile = "/Users/bingwang/Downloads/Skud_CTH/IFO1802.fsa"

def fasta2fsa(openfile,writefile):
    f = open(openfile)
    g = open(writefile,"w")
    for line in f:
        if line[0] == ">":
            line = line[:line.find("[contig")]
            line = "\n" + line.replace("["," [").replace("S_kudriavzevii","Saccharomyces kudriavzevii strain IFO1802")
            num = int(line[line.find("c")+1:line.find(" ")])
            if num >= 9000:
                line += " [note=Contigs 9001, 9002, 9004, and 9080 are present only in Gal+ strains. They are syntenic to the GAL pseudogenes and surrounding regions. Illumina reads from all strains were allowed to assemble to either the functional or pseudogene alleles in these regions, whereas all other contigs had only IFO1802 as the reference strain. For each strain, only one allele is present and leads to significant coverage. See the full Methods in Hittinger et al. 2010 (PMID:20164837) for details.]"
            line += "\n"
        else:
            line = line.replace("\n","").replace("\t","").replace(" ","").replace("\r","").replace("X","N")
        g.write(line)
    f.close()
    g.close()

fasta2fsa(openfile,writefile)
'''
contig_path = "/Users/bingwang/Downloads/Skud_CTH/contigsAll"
contig_list = os.listdir(contig_path)
print contig_list
'''
