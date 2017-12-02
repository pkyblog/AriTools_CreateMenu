# -*- coding: utf-8 -*-
import maya.utils
import sys

def AriTools_CreateMenu():
	from AriTools import AriTools_CreateMenu
	reload(AriTools_CreateMenu)
	AriTools_CreateMenu.main()

def main():
	sys.dont_write_bytecode = True
	maya.utils.executeDeferred(AriTools_CreateMenu)

if __name__ == "__main__":
	main()
