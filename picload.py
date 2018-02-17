#!/usr/bin/env python3

import exifread
import os
import shutil
from datetime import datetime
from optparse import OptionParser


def cutAndPasteToDir(filepath,outputdir,copy):
    if not ( os.path.exists(outputdir) and os.path.isdir(outputdir)):
        os.mkdir(outputdir)
    if copy:
        print(shutil.copy2(filepath,outputdir))
    else:
        print(shutil.move(filepath,outputdir, copy_function=shutil.copy2))

def getInputdir(path):
    if path:
        return os.path.abspath(path)
    else:
        return os.getcwd()

def getOutputdir(path):
    if path:
        return os.path.abspath(path)
    else:
        return os.getcwd()


def main():
    usage = "usage: %prog [options] arg1 arg2\n The utility moves/copies pictures.\
    \nCreates a folder with the name date from exif information."
    p = OptionParser(usage=usage)
    p.add_option("-i","--inputdir",None,help = "The folder from which the files will be moved")
    p.add_option("-o","--outputdir",None,help = "The folder to which the files will be moved")
    p.add_option("-c","--copy",action = "store_true",default=False,help = "Copied files true")
    option, arguments = p.parse_args()
    inputdir = getInputdir(option.inputdir)
    outputdir = getOutputdir(option.outputdir)
    print("dir path:",inputdir)
    listfiles = os.listdir(path=inputdir)
    print("Files and folders detected:",len(listfiles))
    count = 0;
    for f in listfiles[:]:
        pf = os.path.join(inputdir,f)
        if os.path.isfile(pf):
            of = open(pf,"rb")
            tg = exifread.process_file(of)
            if tg.setdefault("Image DateTime",False):
                dt = datetime.strptime(tg.setdefault("Image DateTime").values,"%Y:%m:%d %H:%M:%S")
                subdir = os.path.join(outputdir,str(dt.date()))
                cutAndPasteToDir(pf,subdir,option.copy)
                count +=1
        else:
            listfiles.remove(f)
    print("Processed files:",len(listfiles))
    print("Moved/Copied files:",count)


if __name__ == '__main__':
    main()
