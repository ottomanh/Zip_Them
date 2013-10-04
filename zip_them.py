#! /usr/bin/python

import zipfile
import os,stat,sys,shutil,time,random,string
from cStringIO import StringIO

sep=os.sep
def createZip(pat, name, rand):
	path=pat+sep+name
	def walktree (top = ".", depthfirst = True):
		names = os.listdir(top)
		if not depthfirst:
			yield top, names
		for name in names:
			try:
				st = os.lstat(os.path.join(top, name))
			except os.error:
				continue
			if stat.S_ISDIR(st.st_mode):
				for (newtop, children) in walktree (os.path.join(top, name),depthfirst):
					yield newtop, children
		if depthfirst:
			yield top, names

	list=[] #Add control for zipped dir if it exists or not
	if not os.path.exists('zipped'):
		os.makedirs('zipped')
	for (basepath, children) in walktree(path,False):
			for child in children:
				f=os.path.join(basepath,child)
				if os.path.isfile(f):
					f = f.encode(sys.getfilesystemencoding())
					list.append( f )

	f=StringIO()
	if rand=="1":
		n=30
		rand=''.join(random.choice(string.ascii_lowercase + string.ascii_lowercase + string.digits) for x in range(n))
		file = zipfile.ZipFile('zipped'+sep+rand+".zip", "w")		#Set a random name to the archive
	if rand=="2":
		file = zipfile.ZipFile('zipped/'+name+".zip", "w") #Set the directory name to the archive
	for fname in list: #File insertion into the archive
		nfname=os.path.join(os.path.basename(path),fname[len(path)+1:])
		file.write(fname, nfname , zipfile.ZIP_DEFLATED)
	if os.path.exists('Readme.txt'):
		file.write('Readme.txt', 'Readme.txt', zipfile.ZIP_DEFLATED) #Set Readme as name for the credits file
	file.close()

	f.seek(0)
	return f

def zip_dir(path):
	os.system('cls')
	time.clock()
	tt=0.0
	rand = raw_input("1 Generate random alphanumeric names for the archives\n2 Use the directory name\n")
	for name in os.listdir(path):
		if os.path.isdir(path+sep+name):
			if name=='zipped': break #If was found 'zipped' dir then skip
			createZip(path,name,rand)
			t=str("%.3f" %time.clock())
			tt+=time.clock()
			print name + " compressed in "+t+" secs."
	ttt=str("%.3f" %tt)
	print "Job Done! All dirs was compressed in "+ttt+"secs. Bye"
	time.sleep(1)
os.chdir(os.path.abspath(''))
choose = raw_input("Compress all directories placed in:\n1 Script root\n2 Custom path\n")
if choose=="2":
	var = raw_input("Enter directory path:\n C:\\")
	var = "C:"+sep+var
if choose=="1":
	var = os.getcwd()
else:
	print "Error"
	time.sleep(2) 
	sys.exit()

print "You entered "+ var
 
zip_dir(var)
