import os
import shutil
import datetime
import logging

setDir=""
LOGSET = True

class myLogg():
	def __init__(self,logset=False):
		d = datetime.datetime.now()
		self.filename = "log-%s-%s-%s"%(d.year,d.month,d.day)
		self.logset = logset
		if self.logset:
			logging.basicConfig(filename = self.filename,filemode="a",level = logging.INFO)
			logging.info(str(d))

	def info(self,msg=""):
		if self.logset:
			logging.info(msg)

logg = myLogg(LOGSET)

class myFile():

	def __init__(self):
		self.name = ""
		self.root = ""
		self.dt = None
	
	def date(self):
		if self.dt:
			return  datetime.date(self.dt.year,self.dt.month,self.dt.day)
		else: return None
			
	def __str__(self):
		return os.path.join(self.root,self.name)

def getFiles():
	root = os.getcwd()
	logg.info("read %s"%root)
	files = []
	for item in  os.listdir(root):
		picFile = myFile()
		picFile.name = item
		picFile.root = root
		picFile.dt =  datetime.datetime.fromtimestamp(os.path.getmtime(item))
		files.append(picFile)
	return files	

def run():
	for i in getFiles():
		print(i)

def createDir(files=[]):
#	ndt = datetime.datetime.now()
	cdate = None #datetime.date(ndt.year,ndt.month,ndt.day)
	dirs = set()
	for f in files:
		tmpdate = datetime.date(f.dt.year,f.dt.month,f.dt.day)
		if cdate != tmpdate:
			cdate = tmpdate
			dirPath = os.path.join(f.root,str(cdate))
			if os.path.exists(dirPath):
				if os.path.isdir(dirPath):
					logg.info("Is exists dir=%s"%dirPath)
					dirs.add(cdate)
			else:
				dirs.add(cdate)
	dirs = list(dirs)
	dirs.sort()
	for d in dirs:
		dirPath = os.path.join(f.root,str(d))
		if not os.path.exists(dirPath):
			logg.info("Is create dir=%s"%dirPath)
			os.mkdir( os.path.join(f.root,str(d)))
	for d in dirs:
		msg = "copy start dir: %s"%os.path.join(f.root,str(d))
		print(msg)
		logg.info(msg)
		for f in files:
			if d== f.date():
				setFile = os.path.join(f.root,str(d),f.name)
				if not os.path.exists(setFile) and str(d)!=f.name:
					shutil.copy2(str(f),setFile)
					logg.info("copy file=%s"%f.name)
		msg = "copy end dir: %s"%os.path.join(f.root,str(d))
		print(msg)
		logg.info(msg)



def getListF(fs=[]):
	with open("log","w") as f:
		for item in fs:
			f.write("name = %s,date = %s\n"%(item.name,str(item.dt)))

def printFiles(fs=[]):
	for f in fs:
		print(f)

createDir(getFiles())
#printFiles(getFiles())

