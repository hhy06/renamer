 

# ARXIV file  renamer_45 v1.py
#
#v  1.10  rename files in all sub directories.
#v      1.01  no more __title__ behind file names.
#v45: works for dddd.dddd and dddd.ddddd as well

#45_v2: 2018 Nov. 1st
#fix problem of redundant x] after arxiv number. works on python 2.7.5.



import os,string,   sys  
import urllib,re, socket
import random,time

def namer(arxivNo):
    path='http://www.arxiv.org/abs/'+arxivNo

    print "require page:", path
    page=urllib.urlopen(path)
    begins= False
    
    try:
        for line in page:
            print line
            if line.find('<title>') >=0:
                beginner=line
                break
    except:
        print 'net error'
        return ""

    res=beginner
    finish=False
    while (not finish) and (len(res)>0):
        print finish, res
        
        
            
        if res[:7]=='<title>':
            res=res[7:]
        
        if ord(res[0]) in range(48,58) or res[0] in ['.','v','[',' ']:
            #res[0] =0,1,..9
            res=res[1:]
        if res[0]==']':
            res=res[1:]
            finish=True
        
     
    if res.find('</title>') >=0:
        res=res[:-8]


    illegal='\/:*?"<>|'    #illegal chars to remove
    for ichar in illegal:
        res  = res.replace(ichar, ' _')       

    
    return res 


def checkArxivName(file):  #file is stripped file name!

    #must be strictly dddd.dddd or dddd.ddddd or d
    #    

    if len(file)==7:
        if all([x.isdigit() for x in file]):
        #    return True
            return False # note that 7digit identifier is never sufficient!!!
        
        
    if len(file)==9 or len(file)==10:
        if not file[4]== '.':
            return False
        testrange=[n for n in range(len(file)) if not (n==4)]
        if all([file[i].isdigit() for i in testrange]):
            return len(file)
        
    return False        
        
 

dir = os.curdir
files = os.listdir(dir)  
 
for root, dirs, files in os.walk(dir):
    print "----------------------------------------"
    print root    
    print dirs
    
    for file in files:
        print file
  
        path=root
        if os.path.isfile(os.path.join(root,file))==False:
                continue

        if len(file)<11 or len(file)>15:
                continue
        
        if not file[-4:] == '.pdf':
            continue
        else:
            strippedfile=file[:-4] #strip .pdf

        ver=''
        if strippedfile[-1].isdigit() and strippedfile[-2]=='v':
            ver=strippedfile[-2:]
            strippedfile=strippedfile[:-2] #strip v3
        
        while strippedfile[-1]==' ':
            strippedfile=strippedfile[:-1]
            
            
        if not (checkArxivName(strippedfile)==False):
            arxivNo=strippedfile
            
            title=namer(arxivNo)
            
            while title[0]==' ':
                title=title[1:]
            
            stamp=str(time.struct_time(time.localtime()).tm_year)[-2:]+str(time.struct_time(time.localtime()).tm_mon)+str(time.struct_time(time.localtime()).tm_mday)
            newname=arxivNo+ver+' '+title +stamp+'.pdf'     

            print 'ori : ',  file
            print 'title: ', title
            print 'newname: ', newname
            print
            try:                
                os.rename(os.path.join(path,file),os.path.join(path,newname))
            except:
                print 'renaming failed'
