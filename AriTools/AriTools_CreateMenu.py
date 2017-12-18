# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import os, glob, collections

#フォルダ、ファイルをスキャンしてスクリプトパスが入った辞書を作成
def getScriptList():
	
	scripts = collections.OrderedDict()

	scriptPath = os.path.normpath(os.path.dirname(__file__))

	files = os.listdir(scriptPath)
	files.sort()

	for f in files:
		path = os.path.join(scriptPath,f)
		if os.path.isdir(path):
			path = os.path.join(path,'*.mel')
			mel = glob.glob(path)
			mel.sort()
			scripts[f] = mel
	
	return scripts

#melスクリプトをロード
def loadScript(category,fullpath):
	path = 'AriTools/' + category + '/' + os.path.basename(fullpath)
	mel.eval('source "'+path+'";')

#iconパス取得
def getIcon(melPath):
	iconPath = melPath.replace('.mel','.png')
	iconPath = iconPath.replace(os.sep,'/')

	if os.path.exists(iconPath):
		return iconPath
	else:
		return False

#textからAnnotationを取得
def getAnnotation(melPath):
	
	textPath = melPath.replace('.mel','.txt')
	
	if os.path.exists(textPath):
		with open(textPath) as f:
			lines = f.readlines()
			return lines[0]
	else:
		return False

def main():

	menuName = 'AriTools'

	ariTools = getScriptList()
	
	if cmds.menu(menuName, ex=True):
		cmds.deleteUI(menuName)

	cmds.menu(menuName, label=menuName, parent='MayaWindow', tearOff=True)

	#Ctrl+中クリックでポップアップメニュー版
	#cmds.popupMenu(menuName, ctl=True, button=2, markingMenu=True, p="viewPanes", allowOptionBoxes=1)

	for category in ariTools:

		cmds.menuItem(label=category, tearOff=True, subMenu=True)

		for melPath in  ariTools[category]:
			loadScript(category, melPath)
			melName = os.path.splitext(os.path.basename(melPath))[0]

			icon = getIcon(melPath)
			icon = '-i "%s"' % icon if icon else ''
			
			ann = getAnnotation(melPath)
			ann = '-ann "%s"' % ann.rstrip() if ann else ''

			cmd = 'menuItem -l "%s" %s %s -c "%s";' % (melName, icon, ann, melName)

			mel.eval(cmd)

		cmds.setParent('..',menu=True)

	cmds.menuItem(label=u'CG自習部屋 Mayaの時間', command=lambda *args:cmds.launch(web="http://cgjishu.net/"))
