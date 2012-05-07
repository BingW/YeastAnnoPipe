#coding: utf-8
def gff_pharse(file_name):
    class scaf():
        def __init__(self,line):
            elements = line.split("\t")
            self.seqid = elements[0]
            self.source = elements[1]
            self.ftype = elements[2]
            #if self.ftype != "CDS":
            #    if self.ftype not in ["dispersed repeat","tRNA","pseudogene","intergenic region"]:
            #        print self.ftype
            self.start = elements[3]
            self.end = elements[4]
            self.score = elements[5]
            #print self.score
            #score should be a float number, E-value for similarity and P-value
            #for ab initio prediction 
            try:
                float(self.score)
            except:
                self.score = 0.0
            self.strand = elements[6]
            #if self.strand not in ["+","-"]:
            #    print self.strand
            self.phase = elements[7]
            if self.phase == "-":
                self.phase = "0"
            #if self.phase != "0":
            #    print self.phase
            self.attributes = {}
            for item in elements[8].strip().split(";"):
                self.attributes[item.split("=")[0]]=item.split("=")[1]
                #print item

    scaffold_dict = []
    f = open(file_name)
    for line in f:
        if line[0] != "#":
            scaffold_dict.append(scaf(line))
    return scaffold_dict

def write_scaf(scaf_list,write_file):
    f = open(write_file,"w")
    f.write("##gff-version 3\n")
    for a in scaf_list:
        if a.ftype == "CDS":
            f.write(a.seqid+"\t"+a.source+"\t"+a.ftype+"\t"+a.start+"\t"+\
                    a.end+"\t"+str(a.score)+"\t"+a.strand+"\t"+a.phase+"\n")
                    #"ID="+a.attributes["Name"]+"\n")

gff_file_1 = "/Users/bingwang/VimWork/YeastAnnoPipe/Origin/Scer.gff"
#gff_file_1 = "/Users/bingwang/VimWork/YeastAnnoPipe/AUGUTUS/Scer.gff"
gff_file_2 = "/Users/bingwang/VimWork/YeastAnnoPipe/Modify/Scer.gff"
Scaf_P = gff_pharse(gff_file_1)
write_scaf(Scaf_P,gff_file_2)
#Scaf_A = gff_pharse(gff_file_2)
