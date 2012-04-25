#coding utf-8
import os
path = "/Users/bingwang/VimWork/YeastAnnoPipe/AUGUTUS/"
folder = [a for a in os.listdir(path) \
        if a.count(".") == 0]
for name in folder:
    for tobe_rename in os.listdir(path+name+"/"):
        cmd2 = "mv "+path+name+"/"+tobe_rename+" "+\
                path+name+"/"+tobe_rename.replace("augustus",name)
        print cmd2
        os.system(cmd2)


