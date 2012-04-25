f = open("/Users/bingwang/Downloads/atest/original.orf")
g = open("/Users/bingwang/Downloads/atest/test.tbl","w")
for line in f:
    element = line.split(" ")
    try: 
        if element[0][0] == ">":
            system_name1 = element[0][element[0].find(":")+1:element[0].find("_")]
            system_name2 = element[0][element[0].find("g")+1:]
            system_name = system_name1 + system_name2
            g.write(">Feature "+element[3]+"\n")
            start = element[4].replace("\n","").split("-")[0]
            end = element[4].replace("\n","").split("-")[1]
            reverse = False
            try:
                if element[5] == "reverse":
                    reverse = True
            except:
                pass 

            if reverse == True:
                g.write("<"+end+"\t>"+start+"\tgene\n")
                g.write("\t\t\tgene\t"+element[1].replace(",","")+"_"+system_name+"\n")
                g.write("<"+end+"\t>"+start+"\tmRNA\n")
                g.write("\t\t\tproduct\t"+element[1].replace(",","")+"_"+system_name+"\n")
                g.write(end+"\t"+start+"\tCDS\n")
                g.write("\t\t\tproduct\t"+element[1].replace(",","")+"_"+system_name+"\n")
            else:
                g.write("<"+start+"\t>"+end+">\tgene\n")
                g.write("\t\t\tgene\t"+element[1].replace(",","")+"_"+system_name+"\n")
                g.write("<"+start+"\t>"+end+"\tmRNA\n")
                g.write("\t\t\tproduct\t"+element[1].replace(",","")+"_"+system_name+"\n")
                g.write(start+"\t"+end+"\tCDS\n")
                g.write("\t\t\tproduct\t"+element[1].replace(",","")+"_"+system_name+"\n")
    except:
        continue
f.close()
g.close()
