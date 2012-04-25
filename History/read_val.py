#coding:utf-8
import os
path = "/Users/bingwang/Downloads/Skud_CTH/Strains/"

for item in os.listdir(path):
    if item[item.rfind("."):] == ".val":
        print item

        Count_TerminalNs = 0
        TerminalNs = []
        Count_InternalNs = 0
        InternalNs = []
        Count_NoStop = 0
        NoStop = []
        Count_LeadingX = 0
        LeadingX = []
        Count_TrailingX = 0
        TrailingX = []
        Count_InternalStop = 0
        InternalStop = []
        Count_StopInProtein = 0
        StopInProtein = []
        Count_TooManyXs = 0
        TooManyXs = []
        Count_HighNs = 0
        HighNs = []
        Count_BadStart = 0
        BadStart = []
        Count_AmbiguousStart = 0
        AmbiguousStart = []
        Count_IllegalStart = 0
        IllegalStart = []
        Count_ShortSeq= 0
        ShortSeq = []


        f = open(path+item)
        for line in f:
            if line.find("[SEQ_INST.TerminalNs]") != -1:
                Count_TerminalNs += 1
                TerminalNs.append(line[line.find("lcl|")+4:line.find(": raw")])
            elif line.find("[SEQ_INST.InternalNsInSeqRaw]") != -1:
                Count_InternalNs += 1
                InternalNs.append(line[line.find("lcl|")+4:line.find(": raw")]) 
            elif line.find("[SEQ_FEAT.NoStop]") != -1:
                Count_NoStop += 1
                NoStop.append(line[line.find("-> [lcl|")+8:-2])
            elif line.find("[SEQ_INST.TrailingX]") != -1:
                Count_TrailingX += 1
                TrailingX.append(line[line.find("lcl|")+4:line.find(": raw")]) 
            elif line.find("[SEQ_INST.LeadingX]") != -1:
                Count_LeadingX += 1
                LeadingX.append(line[line.find("lcl|")+4:line.find(": raw")])
            elif line.find("[SEQ_FEAT.InternalStop]") != -1:
                Count_InternalStop += 1
                InternalStop.append(line[line.find("-> [lcl|")+8:-2])
            elif line.find("[SEQ_INST.StopInProtein]") != -1:
                Count_StopInProtein += 1
                StopInProtein.append(line[line.find("lcl|")+4:line.find(": raw")])
            elif line.find("[SEQ_FEAT.CDShasTooManyXs]") != -1:
                Count_TooManyXs += 1
                TooManyXs.append(line[line.find("-> [lcl|")+8:-2])
            elif line.find("[SEQ_INST.HighNContentPercent]") != -1:
                Count_HighNs += 1
                HighNs.append(line[line.find("lcl|")+4:line.find(": raw")])
            elif line.find("[SEQ_INST.BadProteinStart]") != -1:
                Count_BadStart += 1
                BadStart.append(line[line.find("lcl|")+4:line.find(": raw")])
            elif line.find("[SEQ_FEAT.StartCodon] Ambiguous start codon ") != -1:
                Count_AmbiguousStart += 1
                AmbiguousStart.append(line[line.find("-> [lcl|")+8:-2])
            elif line.find("[SEQ_FEAT.StartCodon] Illegal start codon ") != -1:
                Count_IllegalStart += 1
                IllegalStart.append(line[line.find("-> [lcl|")+8:-2])
            elif line.find("[SEQ_INST.ShortSeq]") != -1:
                Count_ShortSeq += 1
                ShortSeq.append(line[line.find("lcl|")+4:line.find(": raw")])
            else:
                print line
        f.close()

        f = open(path+item[:item.rfind(".")]+".report.txt","w")
        f.write(
          str(Count_HighNs)        + "\t\tContigs has too many Ns.\n"
        + str(Count_TerminalNs)    + "\t\tContigs has Ns at end or beginning of the sequence.\n"
        + str(Count_InternalNs)    + "\t\tContigs has internal Ns.\n"
        + str(Count_NoStop)        + "\t\tCDSs has no stop codon.\n"
        + str(Count_InternalStop)  + "\t\tCDSs has internal stpo codon.\n"
        + str(Count_LeadingX)      + "\t\tSequence starts with leading X.\n"
        + str(Count_TrailingX)     + "\t\tSequence ends with trailing X.\n"
        + str(Count_TooManyXs)     + "\t\tTranslatinos has too many Xs.\n"
        + str(Count_BadStart)      + "\t\tTranslations has wrong start codon.\n"
        + str(Count_AmbiguousStart)+ "\t\tTranslations start ambiguously.\n"
        + str(Count_ShortSeq)      + "\t\tTranslations too short.\n")
        f.write("####################################################\n")
        f.write("#              4.CDS has no stop codon             #\n")
        f.write("####################################################\n")
        for item in NoStop:
            f.write(item + "\n")
        f.write("####################################################\n")
        f.write("#        5.CDS has internal stop codon             #\n")
        f.write("####################################################\n")
        for item in InternalStop:
            f.write(item + "\n")
        f.write("####################################################\n")
        f.write("#                9.Wrong start codon               #\n")
        f.write("####################################################\n")
        for item in BadStart:
            f.write(item + "\n")
        f.write("####################################################\n")
        f.write("#    Where LeadingX and Ambiguous are  disagree    #\n")
        f.write("####################################################\n\n")
        f.write("item in LeadingX but not in AmbiguousStart:\n")
        for item in LeadingX:
            try:
                AmbiguousStart.index(item)
            except:
                f.write(item + "\n")
        
        f.write("item in AmbiguousStart but not in LeadingX:\n")
        for item in AmbiguousStart:
            try:
                LeadingX.index(item)
            except:
                f.write(item + "\n")

