#!/usr/bin/env python2.7
#author:Nancy Lalluwadia
#date:6/5/2016
#About Program: WEB CRAWLER
#Implemented a robust text scraper that will connect to a page on www.shopping.com, and return a result for a given keyword. 
#Two queries can be performed using this program. The first query is getting the total number of results for a given keyword. 
#The second query is to find all results for a given keywords on a specified page. 
#
#Following are the URLs
#
#`http://www.shopping.com/products?KW=<keword>`
#`http://www.shopping.com/products~PG-<number>?KW=<keyword>"
#
#Query 1: (requires a single argument)
#`web_crawler.py <keyword>`
#Query 2: (requires two arguments)
#`web_crawler.py <page number> <keyword>`
#
#Ex1: >>>web_crawler.py clothing
#Ex2: >>>web_crawler.py 2 clothing
#Ex3: >>>web_crawler.py
#     >>>please enter product name you want to search: <keyword>(must be alphanumerical allowing space)
#	  >>>please enter page number: <page number>(must be int)
#web crawler's response will be saved in a html file and opened in your systems default brawser's new tab

import urllib
import webbrowser
import os
import sys
import re

class CONST(object):
    '''make constant variable as filename postfix'''
    FILE_URL = "_shopping.html"
    def __setattr__(self, *_):
        pass   

#functions start----------------------------------------------
    
def is_dir_exists(keyword):
    '''boolean check if directory named as value in keyword variable exists or not'''
    return os.path.exists(keyword)

def createDir(keyword):
    '''create directory named value in keyword variable'''
    try:
        os.makedirs(keyword)
        return True
    except:
        return False

def getFileName(keyword,page_no):
    '''return autogenerated filename for searched keyword'''
    return keyword+"_"+page_no+CONST.FILE_URL

def if_file_exists(keyword,page_no):
    '''check if file exists of given keyword in current directory'''
    return os.path.isfile(getFileName(keyword,page_no))

def getNewFile(keyword,page_no):
    '''open/create file in current directory in write mode'''
    return open(getFileName(keyword,page_no),'w')

def getFilePath(keyword,page_no):
    '''return customised path for keyword's file with its parent directory path'''
    return keyword+"/"+getFileName(keyword,page_no)

def getURI(givenurl,keyword,page_no):
    '''return uri for scraping on given website with given keyword and page number'''
    if page_no> 0:
        return givenurl+keyword+"/products~PG-"+page_no+"?KW="+keyword
    else:
        return givenurl+keyword+"/products?KW="+keyword
    
def openPageInBrowsertab(keyword,page_no):
    '''open dowloaded/crawled data response file in default browser's new tab'''
    webbrowser.open_new_tab(os.path.abspath(getFilePath(keyword,page_no)))

def isValidPage_no(pn):
    while pn <0 or not pn.isdigit():
        pn = raw_input("please enter positive integer as page number:").strip()
    return pn

def isValidKeyword(keyword):
    while not re.match('[\w ]+',keyword):
       keyword = raw_input("Please enter valid keyword:")
    return keyword

#functions end------------------------------------------------
#code start---------------------------------------------------
givenurl= "http://www.shopping.com/"
tag = "shopping"
page_no=str(0)

'''GET crawling values from user'''
args = len(sys.argv)
if args>2:
    keyword = sys.argv[2].strip()
    keyword= isValidKeyword(keyword)
    page_no = int(sys.argv[1].strip())
    page_no = str(isValidPage_no(page_no))
elif args == 2 :
    keyword = sys.argv[1].strip()
    keyword= isValidKeyword(keyword)
elif args == 1 :
    keyword = raw_input("please enter product name you want to search:").strip()
    keyword= isValidKeyword(keyword)
    page_no = raw_input("please enter page number:")
    page_no = str(isValidPage_no(page_no))

print("\nplease wait while we are fetching the page....\nIt will get opened in your default browser with path\n")
print(os.path.abspath(tag+"/"+getFilePath(keyword,page_no)))

'''Check the cached file else download respond in new file and open file in web browser'''
createDir(tag)
os.chdir(tag)

if not is_dir_exists(keyword):
    createDir(keyword)

os.chdir(keyword)
if if_file_exists(keyword,page_no):
    os.chdir("..")
    openPageInBrowsertab(keyword,page_no)
else:
    f = getNewFile(keyword,page_no)   
    givenurl_keyword = getURI(givenurl,keyword,page_no)
    handle_keyword = urllib.urlopen(givenurl_keyword)
    respond_keyword = handle_keyword.read()
    f.write(respond_keyword)
    f.close()
    os.chdir("..")
    openPageInBrowsertab(keyword,page_no)
	
#end code---------------------------------------------------------------------------------------------
