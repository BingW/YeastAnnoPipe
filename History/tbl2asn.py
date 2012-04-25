import os
path = "/Users/bingwang/Downloads/Skud_CTH/"
sbtfile = "/Users/bingwang/Downloads/Skud_CTH/HittingerEtAlNature2010.sbt"
def run_tbl2asn(sbtfile,fsafile):
    os.system("tbl2asn -t "+sbtfile+" -i "+fsafile+" -a s -V vb")
'''
for name in os.listdir(path):
    if name[name.rfind(".")+1:] == "fsa" and name.find("_") != -1:
        fsafile = path + name
        run_tbl2asn(sbtfile,fsafile)
'''
fsafile = "/Users/bingwang/Downloads/Skud_CTH/IFO1802_0.fsa"
run_tbl2asn(sbtfile,fsafile)
