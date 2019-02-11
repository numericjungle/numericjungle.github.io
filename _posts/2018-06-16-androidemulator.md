---
date: 2018-06-16 19:24:34.561305
layout: post
title: AndroidEmulator
description: "AndroidEmulator"
tags: []
comments: true
---
<!--excerpt-->

{% highlight python %}
import os
import time
import xml.etree.ElementTree as ET
os.chdir("E:\\projects\\scraper\\")

ADBPath = "C:\\Users\\sechangc\\AppData\\Local\\Android\\Sdk\\platform-tools\\"
pcDirOutput = "C:\\Users\\sechangc\\Documents\\AndroidEmulatorSD\\results\\_test\\"

def adb(cmd):
	return ADBPath+cmd

def run(cmd):
    #print("adb shell " + cmd)
    return os.popen(adb("adb shell " + cmd)).read()

def back():
    time.sleep(1)
    os.popen(adb("adb shell input keyevent 4"))

def prev():
    run("input keyevent KEYCODE_BACK")

def tap(x,y, delay=1):
    time.sleep(delay)
    #print("adb shell input tap {0:d} {1:d}".format(x, y))
    os.popen(adb("adb shell input tap {0:d} {1:d}".format(x, y)))

def dump_viewtree(filename):
    print(os.popen(adb("adb shell uiautomator dump /sdcard/lens/"+filename)).read())
    time.sleep(1)

def dump_screenshot(filename):
    print(os.popen(adb("adb shell screencap -p /sdcard/lens/"+filename)).read())
    time.sleep(1)

dump_viewtree("searchResult.xml")
def copyfromdev(srcfile, destdir, destfile):
    destfilePath = destdir + destfile
    print("adb pull /sdcard/lens/"+srcfile + " "+ destfilePath)
    print(os.popen(adb("adb pull /sdcard/lens/"+srcfile + " "+destfilePath)).read())
    time.sleep(0.2)

def copytodev(srcdir, srcfile, destfile):
    #remove old files. We expect 0 input files to be present when copy a file to device.
    print("adb shell rm /sdcard/DCIM/*")
    run("rm -fr /sdcard/DCIM/*")
    print("adb push " + srcdir + srcfile + " /sdcard/DCIM/"+destfile)
    print(os.popen(adb("adb push " + srcdir + srcfile + " /sdcard/DCIM/"+destfile)).read())
    time.sleep(0.3)

##############################################################
### run emulator from command line #######################
###########################################################
# get your device ID: C:\Program Files (x86)\Microsoft Emulator Manager\1.0>emulatorcmd.exe list /sku:Android /type:device /state:installed
def runEmulator():
	#os.popen("cd C:\Program Files (x86)\Microsoft Emulator Manager\1.0").read()
	os.popen("emulatorcmd.exe launch /sku:Android /id:226C76AC-9E9A-4EBD-A495-79E8C5C5292F").read()

import re
def bdrParser(bd):
	"""input:"[a,b][c,d]"; output: (a+b)/2, (c+d)/2"""
	b,d = re.compile(r",(\d+)\]").findall(bd)
	a,c = re.compile(r"\[(\d+),").findall(bd)
	avg = lambda x, y: int((int(x)+int(y))/2)
	return avg(a,c), avg(b,d)

def KillTextEditor():
	run("am force-stop com.rhmsoft.edit")

def KillWord():
	run("am force-stop com.microsoft.office.word")

def KillGdoc():
	run("am force-stop com.google.android.apps.docs.editors.docs")

def KillPinterest():
    run("am force-stop com.pinterest")

#################################################
## uploate image
#################################################
def searchImage():
	KillPinterest()
	# at home page
	run("am start -n com.pinterest/.activity.task.activity.MainActivity")
	tap(1100, 100) #tap Camera
	tap(800, 1500) #tap upload
	tap(400, 100)  #tap browsing
	tap(200, 300)  #tap folder
	tap(200, 300) # picture
	tap(600, 1750) # execute search

#################################################
## iteratively click all items in the search results
#################################################
def getPinterestSearchResultLocs(pcDir, filename):
	# at the search result page
	# dump current UI view
	filename = "searchResult.xml"
	dump_viewtree(filename)
	os.popen(adb("adb pull " + "/sdcard/lens/"+ filename + " " + pcDir + filename)).read()
	# get the pin image location
	root = ET.parse(pcDir + filename)
	root = root.findall(".//*[@resource-id='com.pinterest:id/recycler_adapter_view']")[0]
	res = []
	for child in root:
		#print(child.tag, child.attrib)
		bd = bdrParser(child.attrib['bounds'])
		res.append(bd)
	return res

#################################################
## output the pin URL from a PIN
#################################################
def copyPIDtoClipboard():
    # at Pinterest app, image
    # get PID url by click share it, paste into a text editor
    tap(200, 100) # options
    tap(100, 1720) # copy link

def copyURLtoGdoc():
	KillGdoc()
	run("am start -n  com.google.android.apps.docs.editors.docs/com.google.android.apps.docs.editors.kix.KixEditorActivity")

def copyURLtoWord():
	KillWord()
	run("am start -n com.microsoft.office.word/com.microsoft.office.apphost.LaunchActivity")
	tap(900, 500) #click blank
	tap(400, 400) #tap empty space

def copyURLtoEditor():
	# at anywhere
	KillTextEditor()
	run("am start -n com.rhmsoft.edit/.activity.MainActivity") #go to QuickEditor
	tap(200, 200) # tap the first line
	tap(1100, 100) # tap edit
	tap(1100, 400) # paste


#################################################
## get save button location
#################################################
def getTextEditorSaveButtonLoc(pcDir = pcDirOutput, filename = "saveButton.html"):
	# at the text editor save as mode
	# dump current UI view
	filename = "saveButton.xml"
	dump_viewtree(filename)
	os.popen(adb("adb pull " + "/sdcard/lens/"+ filename + " " + pcDir + filename)).read()
	# get the pin image location
	root = ET.parse(pcDir + filename)
	# expect only one tag matched
	root
	root = root.findall(".//*[@resource-id='com.rhmsoft.edit:id/fab']")
	for child in root:
		bd = bdrParser(child.attrib['bounds'])
		return bd

def getTextEditorSaveButtonLoc(pcDir = pcDirOutput, filename = "saveButton.html"):
	# at the text editor save as mode
	# dump current UI view
	filename = "saveButton.xml"
	dump_viewtree(filename)
	os.popen(adb("adb pull " + "/sdcard/lens/"+ filename + " " + pcDir + filename)).read()
	# get the pin image location
	root = ET.parse(pcDir + filename)
	# expect only one tag matched
	root
	root = root.findall(".//*[@resource-id='com.rhmsoft.edit:id/fab']")
	for child in root:
		bd = bdrParser(child.attrib['bounds'])
		return bd

def saveURLfromEditor(input):
	# at editor
	time.sleep(0.5)
	tap(1000, 100) # tap folder
	tap(1000, 400) # tap save as
	# in save as window
	saveButtonLoc = getTextEditorSaveButtonLoc()
	#print(saveButtonLoc[0], saveButtonLoc[1]) # tap save button in the list without delay before the ad banner pops up
	tap(saveButtonLoc[0], saveButtonLoc[1])
	time.sleep(0.5)
	run("input text {}".format(input))
	tap(1000, 1100) # tap save
	time.sleep(2.5)

def pullFolder(path):
	os.popen(adb("adb pull {} C://Users//sechangc//Documents//AndroidEmulatorSD//").format(path)).read()

def showCompletedFiles():
	run("ls /sdcard/lens")



{% endhighlight %}
