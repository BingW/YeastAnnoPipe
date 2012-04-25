# coding:utf-8
openfile = "/Users/bingwang/Downloads/Skud_CTH/reference/SkudORFs.fasta.CTH"
writefile = "/Users/bingwang/Downloads/Skud_CTH/Skud.tbl"
#openfile =  "/Users/bingwang/Downloads/atest/original.orf"
#writefile = "/Users/bingwang/Downloads/atest/test.tbl"

def convert_elements(line):
    element = line.split(" ")
    system_name1 = element[0][element[0].find(":")+1:element[0].find("_")]
    system_name2 = element[0][element[0].find("g")+1:]
    system_name = system_name1 + system_name2
    feature_line = ">Feature "+element[3]+"\n"

    start = str(int(element[4].replace("\n","").split("-")[0]))
    end = str(int(element[4].replace("\n","").split("-")[1]))
    reverse = False
    if line.find("reverse") != -1:
        reverse = True
    
    if element[1] == ",":
        element[1] = ""
    else:
        element[1] = element[1].replace(",","_")

    if reverse == True:
        gene_line = "<"+end+"\t>"+start+"\tgene\n"
        gene_name = "\t\t\tgene\t"+element[1]+system_name+"\n"
        tmRNA_line = "<"+end+"\t>"+start+"\tmRNA\n"
        tmRNA_name = "\t\t\tproduct\t"+element[1]+system_name+"\n"
        CDS_line = end+"\t"+start+"\tCDS\n"
        CDS_name = "\t\t\tproduct\t"+element[1]+system_name+"\n"
    else:
        gene_line = "<"+start+"\t>"+end+"\tgene\n"
        gene_name ="\t\t\tgene\t"+element[1]+system_name+"\n"
        tmRNA_line = "<"+start+"\t>"+end+"\tmRNA\n"
        tmRNA_name = "\t\t\tproduct\t"+element[1]+system_name+"\n"
        CDS_line = start+"\t"+end+"\tCDS\n"
        CDS_name = "\t\t\tproduct\t"+element[1]+system_name+"\n"
    elements = [feature_line,gene_line,gene_name,tmRNA_line,tmRNA_name,CDS_line,CDS_name]
    return elements

def orf2tbl():
    pass

def combine_elements(elements1,elements2):
    if elements1[0] == elements2[0]:
        feature_line = elements1[0]
    else:
        print "elements1, are not the same as elements2"
    if elements1[1] == elements2[1]:
        gene_line = elements1[1]
        gene_name = elements1[2] + elements2[2]
        tmRNA_line = elements1[3]
        tmRNA_name = elements1[4] + elements1[4]
        CDS_line = elements1[5]
        CDS_name = elements1[6] + elements1[6]
    else:
        print "elements1, are not the same as elements2"
    elements = [feature_line,gene_line,gene_name,tmRNA_line,tmRNA_name,CDS_line,CDS_name]
    return elements

def print_elements(elements):
    for item in elements:
        print item

f = open(openfile)
contigs = []
positions = []
orfs = []
flag = []
for line in f:
    if line[0] == ">":
        elements = convert_elements(line)
        try:
            i = contigs.index(elements[0])
            j = positions[i].index(elements[1])
            index = flag.index([i,j])
            orfs[index] = combine_elements(elements,orfs[index])
        except:
            try:
                i = contigs.index(elements[0])
                j = len(positions[i])
                positions[i].append(elements[1])
                orfs.append(elements)
                flag.append([i,j])
            except:
                contigs.append(elements[0])
                positions.append([])
                positions[contigs.index(elements[0])].append(elements[1])
                orfs.append(elements)
                i = len(contigs) - 1
                j = 0
                flag.append([i,j])
f.close()

g = open(writefile,"w")
for elements in orfs:
    for item in elements:
        g.write(item)
g.close()

