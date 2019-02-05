import subprocess
from zs.bibtex.parser import parse_file
import os
import re
import string

PUBLICATION_MARKDOWN_FOLDER = "_publication"
BIBTEX_FOLDER = "./bibtex_files"
TEMP_FILE_FOLDER = "./tmp"

def get_bib_types():
	arr_bib_types = []
	for root, dirs, files in os.walk("."):
		# print root, dirs, files
		if root == BIBTEX_FOLDER:
			for one_file in files:
				if one_file.endswith(".bib"):
					arr_bib_types.append(one_file[:len(one_file)-4])
			break
	return arr_bib_types

def start_parsing():

	# remove all old publication files
	for root, dirs, files in os.walk("../"+PUBLICATION_MARKDOWN_FOLDER):
		for one_file in files:
			os.unlink(root+"/"+one_file)

	arr_bib_types = get_bib_types()
	for bib_type in arr_bib_types:
		bib_url = BIBTEX_FOLDER + "/" + bib_type + ".bib"
		tmp_url = TEMP_FILE_FOLDER + "/" + bib_type + ".txt"

		# create formatted reference text
		process = subprocess.Popen('pybtex-format '+bib_url+' '+tmp_url, shell=True, stdout=subprocess.PIPE)
		process.wait()

		array_text = []
		with open(tmp_url) as f:
			array_text = f.readlines()
		bibliography = parse_file(bib_url)
		for key, article in bibliography.iteritems():
			article["pub_type"] = bib_type
			article["title"] = article["title"].strip("{").strip("}")
			write_to_markdown_file(key, article, find_text_in_array(array_text, article['title']))

def find_text_in_array(array_text, text):
	for single_text in array_text:
		if str(text).lower().strip() in (single_text).lower():
			index_start =  str(single_text).find(' ')+1
			tmpstr=str(single_text)[index_start:] 
			tmpstr=re.sub(r'URL.*','',tmpstr)
			tmpstr=re.sub(r'doi.*','',tmpstr)
			tmpstr=re.sub(r'\\t', ' ', tmpstr)
			tmpstr=re.sub(r'\\r', ' ', tmpstr)
			tmpstr=re.sub(r'\\n', ' ', tmpstr)
			print tmpstr
			return tmpstr
	return None

def write_to_markdown_file(publication_abbr, article, formatted_text):
	#print article
	file = open("../"+PUBLICATION_MARKDOWN_FOLDER+"/"+publication_abbr+".md", "w")
	file.write("---"+"\n")
	# layout
	file.write("layout:     post"+"\n")
	# title
	if formatted_text:
		file.write("title:      \""+formatted_text.strip()+"\""+"\n")
                #print formatted_text
	else:
		file.write("title:      \""+article["title"].strip()+"\""+"\n")
	# date
	file.write("date:       "+str(article["year"])+"-01-01 00:00:01"+"\n")
	file.write("year:       "+str(article["year"])+"\n")
	file.write("pub_type:       "+str(article["pub_type"])+"\n")
        urldoi=True
        if "url" in article:
                file.write("link:       "+str(article["url"])+"\n")    
                urldoi=False
        if "doi" in article:		
                    file.write("doi:       "+"DOI  "+str(article["doi"])+"\n")
                    if urldoi:
                         if 'http' in str(article["doi"]):
                            file.write("link:       "+str(article["doi"])+"\n")   
                         else:
                            file.write("link:       "+"https://dx.doi.org/"+str(article["doi"])+"\n")   
	if "tagproject" in article:
		file.write("proj_type:       "+str(article["tagproject"])+"\n")
	# else:
	# 	file.write("proj_type:       "+""+"\n")
	file.write("---"+"\n")
	file.close()

start_parsing()
