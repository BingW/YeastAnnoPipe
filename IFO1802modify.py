#coding:utf-8
import os
import sqlite3
Coon = sqlite3.connect('/Users/bingwang/VimWork/db/Scer.db')
C = Coon.cursor()
other2ID = {}
ID2Product = {}
ID2gene = {}
for row in C.execute("SELECT * FROM other2ID"):
    other2ID[row[0]] = row[1]
for row in C.execute("SELECT * FROM ID2Product"):
    ID2Product[row[0]] = row[1]
for row in C.execute("SELECT * FROM ID2Feature"):
    ID2gene[row[0]] = row[2] if row[2] != "" else row[1]

class Contig():
    def __init__(self,identity):
        self.obj = identity          #1
        self.obj_beg = 1             #2 C
        self.obj_end = 0             #3 C
        self.part_num = 1            #4
        self.component_type = "W"    #5  default      
        self.component_id = ""       #6a 
        self.component_beg = 1       #7a default
        self.component_end = 0       #8a 
        self.orentation = "+"        #9a default

        self.gap_beg = 0
        self.gap_end = 0
        self.gap_length = 0          #6b         it's Ns before a contig
        self.gap_type = "scaffold"   #7b default
        self.linkage = "yes"         #8b default
        self.linkage_evidence = "align_genus"   #9b default
        
        self.seq = ""
        self.cmt = ""
    
    def get_seq(self,beg,end):
        if beg < 0 or end < 0 or beg == end:
            return 0
        elif end > beg:
            if end > len(self.seq):
                return 0
            else:
                return self.seq[beg-1:end+3]
        else:
            if beg > len(self.seq):
                return 0
            else:
                return reverse(self.seq[end-4:beg])

 
class Sequence():
    def __init__(self,identity):
        self.original = ""

class Feature():
    def __init__(self,identity,product):
        sys_name = product.split("_")[0].replace("-P","").replace("-J","")
        contig = product.split("_")[1].split(".")[0].replace("Skud","")
        contig_i = product.split("_")[1].split(".")[1].replace("Skud","")
        contig = "0"*(4-len(contig))+contig
        contig_i = "0"*(2-len(contig_i))+contig_i
        self.identity = identity
        self.locus_tag = "SKUD_"+contig+contig_i
        if sys_name != "":
            gene = ID2gene[other2ID[sys_name]]
            self.gene = sys_name
            try:
                #self.product = ID2Product[other2ID[sys_name]].replace(",","")
                self.product = gene+"-like protein" if gene != "" else "hypothetical protein"
            except:
                #print sys_name
                self.product = "Unknown"
        else:
            self.gene = contig+contig_i 
            self.product = "hypothetical protein"
        self.left = 0
        self.left_complete = False
        self.right = 0
        self.right_complete = False
        self.reverse = False
        self.seq = ""
        self.refseq = ""
        self.note = product
        self.addition = ""
        self.affact = 0

        if self.product == "YPL249C-P_Skud9004.2":
            self.right_complete = False 
        if self.product == "YML052W-P_Skud9080.2":
            self.left_complete = False
            self.addition = "codon_start\t2"
        if self.product == "YML050W-P_Skud9080.3":
            self.right_complete = False 
    
    def judge_orf(self,strain_name):
        if self.seq == 0:
            return False
        if strain_name.find("IFO") != -1:
            if self.product.find("P_Skud90") != -1:
                return False

        if self.product == "YML052W-P_Skud9080.2":
            return True

        if self.seq[0:3] == "ATG":
            self.left_complete = True
        else:
            print "wrang_start codon @",self.product

        count = 0
        for i in range(0,len(self.seq),3):
            try:
                ["TGA","TAA","TAG"].index(self.seq[i:i+3])
                count += 1
                if self.right_complete == True:
                    continue
                elif not self.reverse:
                    self.right = self.left + i + 2
                elif self.reverse:
                    self.right = self.left - i - 2
                self.right_complete = True
            except:
                continue

        if count == 0:
            print "Modified: No stop codon @",self.product
            #print self.seq
        elif count > 2:
            print "Modified: mutiply stop codon @",self.product
            #print self.seq
        return True

def reverse(seq):
    reverse = ""
    length = len(seq)
    for i in range(length):
        if seq[length-i-1] == "A" or seq[length-i-1] == "a":
            reverse += "T"
        elif seq[length-i-1] == "T" or seq[length-i-1] == "t":
            reverse += "A"
        elif seq[length-i-1] == "C" or seq[length-i-1] == "c":
            reverse += "G"
        elif seq[length-i-1] == "G" or seq[length-i-1] == "g":
            reverse += "C"
        else:
            reverse += "N"
    if len(reverse) != length:
        print "look @ reverse"
    return reverse

def write_agp(contigs,write_file):
    f = open(write_file,"w")
    for contig in contigs:
        if contig.part_num > 1:
            f.write(contig.obj+"\t")
            f.write(str(contig.gap_beg)+"\t")
            f.write(str(contig.gap_end)+"\t")
            f.write(str(contig.part_num-1)+"\t")
            f.write("N"+"\t")
            f.write(str(contig.gap_length)+"\t")
            f.write(contig.gap_type+"\t")
            f.write(contig.linkage+"\t")
            f.write(contig.linkage_evidence+"\n")
        f.write(contig.obj+"\t")
        f.write(str(contig.obj_beg)+"\t")
        f.write(str(contig.obj_end)+"\t")
        f.write(str(contig.part_num)+"\t")
        f.write(contig.component_type+"\t")
        f.write(contig.component_id+"\t")
        f.write(str(contig.component_beg)+"\t")
        f.write(str(contig.component_end)+"\t")
        f.write(contig.orentation+"\n")
    f.close()

def write_fsa(contigs,write_file):
    f = open(write_file,"w")
    for contig in contigs:
        f.write(contig.cmt + "\n")
        f.write(contig.seq + "\n")
    f.close()

def write_tbl(features,write_file):
    f = open(write_file,"w")
    featureID2features = {}
    for feature in features:
        if feature.identity not in featureID2features:
            featureID2features[feature.identity] = [feature]
        else:
            featureID2features[feature.identity].append(feature)

    for featureID in featureID2features:
        f.write(">Feature\t"+featureID2features[featureID][0].identity+"\n")
        left_right = []
        for feature in featureID2features[featureID]:
            #/discard no need CDS
            if feature.locus_tag in ["SKUD_205709","SKUD_165907",\
                    "SKUD_200408","SKUD_204206","SKUD_181805","SKUD_118503",\
                    "SKUD_187602"]:
                print feature.locus_tag
                continue
            #/
            if "<"+str(feature.left)+"\t>"+str(feature.right) not in left_right:

                f.write("<"+str(feature.left)+"\t>"+str(feature.right)+"\tgene\n")
                f.write("\t\t\tgene\t"+feature.gene+"\n")
                f.write("\t\t\tlocus_tag\t"+feature.locus_tag+"\n")
                f.write("<"+str(feature.left)+"\t>"+str(feature.right)+"\tmRNA\n")
                f.write("\t\t\tproduct\t"+feature.product+"\n")
                f.write("\t\t\tprotein_id\tgnl|HittingerWISC|"+feature.locus_tag+"\n")
                f.write("\t\t\ttranscript_id\tgnl|HittingerWISC|mrna."+feature.locus_tag+"\n")

                if feature.left_complete == True and feature.right_complete == True:
                    f.write(str(feature.left)+"\t"+str(feature.right)+"\tCDS\n")
                elif feature.left_complete == False and feature.right_complete == True:
                    f.write("<"+str(feature.left)+"\t"+str(feature.right)+"\tCDS\n")
                elif feature.left_complete == True and feature.right_complete == False:
                    f.write(str(feature.left)+"\t>"+str(feature.right)+"\tCDS\n")
                elif feature.left_complete == False and feature.right_complete == False:
                    f.write("<"+str(feature.left)+"\t>"+str(feature.right)+"\tCDS\n")
                else:
                    print "look @ function write_tbl!!"

                f.write("\t\t\tproduct\t"+feature.product+"\n")
                f.write("\t\t\tprotein_id\tgnl|HittingerWISC|"+feature.locus_tag+"\n")
                f.write("\t\t\ttranscript_id\tgnl|HittingerWISC|mrna."+feature.locus_tag+"\n")
                f.write("\t\t\tnote\t"+feature.note+"\n")
                if feature.addition:
                    f.write("\t\t\t"+feature.addition+"\n")
                left_right.append("<"+str(feature.left)+"\t>"+str(feature.right))

def write_cmt(coverage,strain_name,write_file):
    f = open(write_file,"w")
    f.write("StructuredCommentPrefix\t##Genome-Assembly-Data-START##\n")
    if strain_name == "IFO1802":
        f.write("Assembly Method\tPHRAP v. 0.990319\n")
    else:
        f.write("Assembly Method\tCustom (Hittinger et al. 2010. PMID: \
                20164837) v. March 2009\n")
    f.write("Assembly Name\tSaccharomyces_kudriavzevii_strain_"+strain_name+"_v1.0\n")
    f.write("Genome Coverage\t"+coverage+"\n")
    if strain_name == "IFO1802":
        f.write("Sequencing Technology\tSanger\n")
    else:
        f.write("Sequencing Technology\tIllumina GA\n")
    #if strain_name != "IFO1802":
    #    f.write("Assemble Method\treference guided assemblies based on AACI00000000\n")
    f.write("StructuredCommentSuffix\t##Genome-Assembly-Data-END##\n")
    f.close()

def check_fsa(filename):  #fsa file should be ">"-"seq"-">"-"seq"
    f = open(filename)
    flag = 0
    for line in f:
        if flag == 0 and line[0] == ">":
            flag = 1
            continue
        if flag == 1 and line[0] != ">":
            flag = 0
            continue
        else:
            print "check @fsa"
            return 0
    f.close()
    return 1 

def valid_contig(contig_id,contigs):
    for i,contig in enumerate(contigs):
        if contig.component_id == contig_id:
            return contig
    return 0

def lcountN(line):
    for i,base in enumerate(line):
        if base != "N":
            return i

def rcountN(line):
    for i in range(len(line)-1,-1,-1):
        if line[i] != "N":
            return len(line)-1-i

def run_tbl2asn(sbtfile,fsafile):
    os.system("tbl2asn -t "+sbtfile+" -p ~/Vimwork/ -a s -V vb -X C")
    #os.system("tbl2asn -t "+sbtfile+" -p ~/Vimwork/ -M n -Z discrep")
    #os.system("tbl2asn -t "+sbtfile+" -i "+fsafile+" -a s -V vb -X C")

def seq_coverage(strain_name):
    if strain_name == "FM1069":
        return str(7807789 * 30.5 / 11736856)+"x"     #FM1069
    elif strain_name == "FM1056":
        return str(3097180 * 36   / 11736856)+"x"     #FM1056
    elif strain_name == "FM1094":
        return str(2728243 * 36   / 11736856)+"x"     #FM1094
    elif strain_name == "FM1057":
        return str(3269665 * 34   / 11736856)+"x"     #FM1057
    elif strain_name == "ZP591":
        return str(12459524 * 34  / 11736856)+"x"     #FM1009/ZP591
    elif strain_name == "FM1071":
        return str(4544569 * 34   / 11736856)+"x"     #FM1071
    elif strain_name == "FM1078":
        return str(3138597 * 36   / 11736856)+"x"     #FM1078
    elif strain_name == "FM1079":
        return str(5087661 * 36   / 11736856)+"x"     #FM1079
    elif strain_name == "FM1072":
        return str(3081430 * 36   / 11736856)+"x"     #FM1072
    elif strain_name == "FM1073":
        return str(3882742 * 36   / 11736856)+"x"     #FM1073
    elif strain_name == "FM1074":
        return str(5347358 * 36   / 11736856)+"x"     #FM1074
    elif strain_name == "FM1062":
        return str(2786785 * 34   / 11736856)+"x"     #FM1062
    elif strain_name == "FM1075":
        return str(3104399 * 36   / 11736856)+"x"     #FM1075
    elif strain_name == "FM1076":
        return str(2763826 * 36   / 11736856)+"x"     #FM1076
    elif strain_name == "FM1077":
        return str(4472512 * 36   / 11736856)+"x"     #FM1077
    elif strain_name == "FM1066":
        return str(2864521 * 34   / 11736856)+"x"     #FM1066
    elif strain_name == "IFO1802":
        return str(3.4                      )+"x"     #IFO1802
    elif strain_name == "IFO10990":
        return str(3222318 * 34   / 11736856)+"x"     #IFO10990 
    elif strain_name == "IFO10991":
        return str(3294821 * 34   / 11736856)+"x"     #IFO10991
    elif strain_name == "IFO1803":
        return str(8542642 * 34   / 11736856)+"x"     #IFO1803
    elif strain_name == "FM1043":
        return str(635858 * 34    / 11736856)+"x"     #FM1043
    elif strain_name == "FM1054":
        return str(755492 * 34    / 11736856)+"x"     #FM1054
    else:
        print "ERROR: check strain_name".strain_name
        return None

def genbank_pipeline(strain_name):
    
    #/ if N>10 split contig, if contig<200 discard
    MAX_NS = 10
    MIN_CONTIG = 200
    #/
    coverage = seq_coverage(strain_name)
    #/ name of contig
    name_base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    name_suffix = []
    for base_1 in name_base:
        for base_2 in name_base:
            name_suffix.append(base_1+base_2) 
    #/

    #/fasta file input, should @ db/Skud_CTH/
    if strain_name == "IFO1802":
        fsa_input = "/Users/bingwang/VimWork/db/Skud_CTH/reference/"+strain_name+".fsa"
    else:
        fsa_input = "/Users/bingwang/VimWork/db/Skud_CTH/Strains/"+strain_name+".fsa"
    #/

    #/agp, fsa, cmt wirtefile
    agp_writefile = "/Users/bingwang/VimWork/"+strain_name+".agp"
    fsa_writefile = "/Users/bingwang/VimWork/"+strain_name+".fsa"
    cmt_writefile = "/Users/bingwang/VimWork/"+strain_name+".cmt"
    #/

    #write comment file
    write_cmt(coverage,strain_name,cmt_writefile)

    #/contig & features initial
    contigs = []
    features = []
    #/

    if check_fsa(fsa_input):
        f = open(fsa_input)
        for line in f:
            line = line.strip()
            if line[0] == ">":
                identity = line.split(" ")[0][1:]
            
            else:
                elements = line.split("N"*MAX_NS)
                count_contig = 0
                gap_length = 0

                for item in elements:
                    if len(item) > MIN_CONTIG:
                        contig_length = len(item)-lcountN(item)-rcountN(item)

                        if contig_length > MIN_CONTIG:
                            count_contig += 1
                            contig = Contig(identity)
                            
                            contig.part_num = count_contig
                            contig.component_end = contig_length
                            contig.gap_length = gap_length+lcountN(item)
                            if count_contig > len(name_suffix):
                                print "ERROR: contig unm > "+len(name_suffix)
                            contig.component_id = identity+name_suffix[count_contig-1]

                            if count_contig == 1:
                                contig.obj_beg = 1
                                contig.obj_end = contig_length
                                obj_end_record = contig.obj_end
                            elif count_contig >1:
                                contig.part_num = contig.part_num*2-1
                                contig.gap_beg = obj_end_record+1
                                contig.gap_end = contig.gap_beg+contig.gap_length-1
                                contig.obj_beg = contig.gap_end+1
                                contig.obj_end = contig.obj_beg+contig_length-1
                                obj_end_record = contig.obj_end
                            else:
                                print "Error occur count_contig < 1"

                            if rcountN(item) > 0:
                                contig.seq = item[lcountN(item):-rcountN(item)]
                            elif rcountN(item) == 0:
                                contig.seq = item[lcountN(item):]
                            else:
                                print "Error occurs rcountN < 0"
                            
                            contig.cmt = ">"+contig.component_id+" "+"[org=Saccharomyces \
                                    kudriavzevii] [moltype=genomic][strain="+strain_name+"]"
                            if contig.obj == "c9001" or contig.obj == "c9002" or\
                              contig.obj == "c9004" or contig.obj == "c9080":
                                contig.cmt = ">"+contig.component_id+" "+"[org=Saccharomyces kudriavzevii] [moltype=genomic] [strain="+strain_name+"][note=Contigs 9001, 9002, 9004, and 9080 are present only in Gal+ strains. They re syntenic to the GAL pseudogenes and surrounding regions. Illumina reads from all strains were allowed to assemble to either the functional or pseudogene alleles in these regions, whereas all other contigs had only IFO1802 as the reference strain. For each strain, only one allele is present and leads to significant coverage. See the full Methods in Hittinger et al. 2010 (PMID:20164837) for details.]"

                            contigs.append(contig)
                            gap_length = rcountN(item) + MAX_NS

                        else:
                            gap_length += len(item) + MAX_NS
                            continue
                    else:
                        gap_length += len(item) + MAX_NS

    write_fsa(contigs,fsa_writefile)
    write_agp(contigs,agp_writefile)

    if strain_name == "IFO1802":
        tbl_writefile =  "/Users/bingwang/VimWork/"+strain_name+".tbl"
        orf_input = "/Users/bingwang/VimWork/db/Skud_CTH/reference/SkudORFs.fasta.CTH"
        f = open(orf_input)
        get_sequence = False
        for line in f:
            line = line.strip()
            if line[0] == ">":
                element = line.split(" ")
                feature_id = element[3] + "AA"
                the_contig = valid_contig(feature_id,contigs)

                if the_contig:
                    system_name = "Skud" + element[0][element[0].find("Contig")+6:]
                    scer_name = element[1].replace(",","_")
                    product = scer_name + system_name
                    feature = Feature(feature_id,product)
                    num = element[4].split("-")
                    
                    if line.find("reverse") == -1:
                        feature.reverse = False
                        feature.left = int(num[0])-the_contig.gap_length
                        feature.right = int(num[1])-the_contig.gap_length
                    elif line.find("reverse") != -1:
                        feature.reverse = True
                        feature.left = int(num[1])-the_contig.gap_length
                        feature.right = int(num[0])-the_contig.gap_length

                    feature.seq = the_contig.get_seq(feature.left,feature.right)
                    
                    if feature.judge_orf(strain_name):
                        get_sequence = True
                        feature.seq = the_contig.get_seq(feature.left,feature.right)
                        if feature.seq[0:3] != "ATG":
                            print feature.seq
                else:
                    continue

            elif get_sequence == True:
                feature.refseq = line
                features.append(feature)
                get_sequence = False

            else:
                continue
        f.close()
        write_tbl(features,tbl_writefile)

    path = "/Users/bingwang/VimWork/"
    sbtfile = "/Users/bingwang/VimWork/db/Skud_CTH/template_v2.sbt"
    run_tbl2asn(sbtfile,fsa_writefile)
    f = open("/Users/bingwang/VimWork/errorsummary.val")
    for line in f:
        print line
    f.close()
    #os.system("mv /Users/bingwang/VimWork/"+strain_name+".agp \
    #         /Users/bingwang/VimWork/upload2genebank/"+strain_name+".agp")
    #os.system("mv /Users/bingwang/VimWork/"+strain_name+".sqn \
    #             /Users/bingwang/VimWork/upload2genebank/"+strain_name+".sqn")
    #os.system("mv /Users/bingwang/VimWork/"+strain_name+".gbf \
    #             /Users/bingwang/VimWork/upload2genebank/"+strain_name+".gbf")
    #os.system("rm /Users/bingwang/Vimwork/"+strain_name+".*")

if __name__ == "__main__":
    # Strain_name_list = ["FM1069","FM1056","FM1094","FM1057","ZP591","FM1071","FM1078",\
    #     "FM1079","FM1072","FM1073","FM1074","FM1062","FM1075","FM1076","FM1077","FM1066",\
    #     "IFO1802","IFO10990","IFO10991","IFO1803"]
    #for strain_name in Strain_name_list:
    #    genbank_pipeline(strain_name)
    genbank_pipeline("IFO1802")

