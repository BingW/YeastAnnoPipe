#-*- coding:utf-8 -*-
import os
path = "/Users/bingwang/Downloads/forDistribution/ORFsAll/"
suffix = "fasta"
tosuffix = "fsa"
for item in os.listdir(path):
    if item[item.rfind(".")+1:] == suffix:
        cmd = "mv "+path+item+" "+path+item[:item.rfind(".")+1]+tosuffix
        os.system(cmd)
