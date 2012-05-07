#coding: utf-8
def gff_pharse(file_name):
    scaf = {}
    f = open(file_name)
    for line in f:
        if line[0] != "#":
            elements = line.split("\t")
            seqid = elements[0] 
            try:
                seqid = int(seqid)
            except:
                seqid = seqid[seqid.rfind("_")+1:]
                seqid = int(seqid)
            source = elements[1]
            ftype = elements[2]
            start = elements[3]
            end = elements[4]
            score = elements[5]
            strand = elements[6]
            phase = elements[7]
            attributes = elements[8]
            if ftype in ["CDS","pseudogene","ORF"]:
                try:
                    scaf[seqid][start+"_"+end] = ftype
                except:
                    scaf[seqid] = {}
                    scaf[seqid][start+"_"+end] = ftype
            elif ftype in ["gene","transcript","start_codon","stop_codon", \
                "single"]:
                pass
            elif ftype in ["gap","dispersed repeat","intergenic region", \
                "tRNA"]:
                pass
            elif ftype in ["initial","intron","terminal","internal"]:
                pass
            else:
                print ftype
    return scaf

gff_file_1 = "/Users/bingwang/VimWork/YeastAnnoPipe/Origin/Scer.gff"
gff_file_2 = "/Users/bingwang/VimWork/YeastAnnoPipe/AUGUTUS/Scer.gff"
Scaf_P = gff_pharse(gff_file_1)
Scaf_A = gff_pharse(gff_file_2)
for index in Scaf_P:
    for start_stop in Scaf_P[index]:
        try:
            if start_stop in Scaf_A[index]:
                print "COOL    \t #",index,"\t",start_stop
            else:
                print "DISAGREE\t P's#",index,"\t",start_stop
        except:
            print "DISAGREE\t P's#",index,"\t",start_stop
for index in Scaf_A:
    for start_stop in Scaf_A[index]:
        try:
            if start_stop in Scaf_P[index]:
                if Scaf_P[index][start_stop] == "CDS":
                    print "COOL    \t #",index,"\t",start_stop
            else:
                print "DISAGREE\t A's#",index,"\t",start_stop
        except:
            print "DISAGREE\t A's#",index,"\t",start_stop
