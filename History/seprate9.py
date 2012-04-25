# coding:utf-8
import os
format_type = ".fsa"

openfile = "/Users/bingwang/Downloads/Skud_CTH/IFO1802.fsa"
writefile_0 = "/Users/bingwang/Downloads/Skud_CTH/IFO1802_0.fsa"
writefile_9 = "/Users/bingwang/Downloads/Skud_CTH/IFO1802_9.fsa"
'''
path = "/Users/bingwang/Downloads/Skud_CTH/Strains/"
'''

def seprate(openfile,writefile_0,writefile_9):
    f = open(openfile)
    w0 = open(writefile_0,"w")
    w9 = open(writefile_9,"w")
    flag = True
    for line in f:
        if line[0] == ">":
            if format_type == ".tbl":
                num = int(line[line.find("c")+1:line.find("\n")])
            elif format_type == ".fsa":
                num = int(line[line.find("c")+1:line.find(" ")])
            
            if num >= 9000:
                flag = True
            else:
                flag = False
            if flag == True:
                w9.write(line)
            else:
                w0.write(line)
        else:
            if flag == True:
                w9.write(line)
            else:
                w0.write(line)
    f.close()
    w0.close()
    w9.close()
'''
for name in os.listdir(path):
    if name[name.rfind(".")+1:] == "fsa" and name.find("_") == -1:
        #print name
        if format_type == ".fsa":
            openfile = path + name
        elif format_type == ".tbl":
            openfile = "/Users/bingwang/Downloads/Skud_CTH/Skud_2.22.tbl"  
        writefile_common = path + name[:name.rfind(".")] + format_type
        #cmd = "cp "+openfile+" "+writefile_common
        #os.system(cmd)
        writefile_0 = path + name[:name.rfind(".")] + "_0" + format_type
        writefile_9 = path + name[:name.rfind(".")] + "_9" + format_type
        seprate(openfile,writefile_0,writefile_9)

'''
seprate(openfile,writefile_0,writefile_9)
