# -*- coding: utf-8 -*-
import os
import codecs
import xlwt
def run(savepath,srclang):
	wb = xlwt.Workbook()
	ws = wb.add_sheet('AppStrings-Code')
	# XCODE_PATH = "/Users/alfredreynold/ALFRED/DEV/Proj/en.lproj/"
	XCODE_PATH = "/Users/alfredreynold/ALFRED/DEV/Proj/Lang/French/"+srclang+".lproj/"
	localizableStringsFile = XCODE_PATH + 'Localizable.strings'
	f4= codecs.open(localizableStringsFile, 'r', encoding='utf-16')
	lines4 = f4.readlines()
	ctr = 0
	for l in lines4:
		if(l.find("=") != -1):
			lft,rgt = l.strip().split(' = ')
			lft = lft.strip().lower().replace('"','').replace(';','')
			rgt = rgt.strip().lower().replace('"','').replace(';','')
			print(lft," - ",rgt)

			if lft == rgt:
				key = l.strip().split(" = ")[0].replace('"','')
				# key = key.replace(',','^')
				value = l.strip().split(" = ")[1].replace('"','')
				value = value.replace(';','')
				# value = value.replace(',','^')
				ws.write(ctr,0,key)
				#ws.write(ctr,1,value)
				ctr = ctr + 1

	wb.save(savepath+'AppStrings-in-Xcode.xls')

	ws2 = wb.add_sheet('AppStrings-XIB')

	LPROJ_PATH = "/Users/alfredreynold/ALFRED/DEV/Proj/Lang/French/"+srclang+".lproj/"
	stringFileNames = []
	for files in os.listdir(LPROJ_PATH):
		if files.endswith(".strings") and os.path.exists(LPROJ_PATH+files.split('.')[0]+'.xib'):
			print files
			stringFileNames.append(files)

	ctr = 0
	for fn in stringFileNames:
		fpath = XCODE_PATH+fn
		print fpath
		f = codecs.open(fpath, 'r',encoding='utf-16')
		ws2.write(ctr,0,fn)
		ctr = ctr+1
		lines = f.readlines()
		for l in lines:
			if l.startswith('/*') is False and len(l.strip())>0:
				lft,rgt = l.strip().split(' = ')
				lft = lft.strip().lower().replace('"','').replace(';','')
				rgt = rgt.strip().lower().replace('"','').replace(';','')
				print(lft," - ",rgt)
				if True:
					string = l.strip().split(' = ')[-1].replace(";",'').replace('"','').strip()
					ws2.write(ctr,0,string)
					ctr = ctr+1
		f.close()
	wb.save(savepath+'AppStrings-in-Xcode.xls')

run('/Users/alfredreynold/ALFRED/Docs/LangFR/','fr')