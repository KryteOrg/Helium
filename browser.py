import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtWidgets, QtGui
import os
import glob

tabs = []

class Window(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		global tabs
		self.tab = QtWidgets.QTabWidget(self)
		self.tab.addTab(QtWidgets.QLabel('Creating new tab...'), '+')
		browser = QWebEngineView(self)
		browser.setUrl(QUrl('file://' + os.getcwd() + "/browser/start/index.html"))
		self.tab.setTabsClosable(True)
		self.tab.tabCloseRequested.connect(self.tab.removeTab)
		self.tab.addTab(browser, 'Start')
		self.tab.setCurrentIndex(1)
		self.tab.move(0,30)
		self.tab.resize(250,30)
		self.tab.currentChanged.connect(self.tabEvent)
		self.entry = QLineEdit(self)
		self.entry.resize(250,30)
		self.entry.move(120,0)
		self.entry.installEventFilter(self)
		self.back = QPushButton("", self) 
		self.back.resize(30,30) 
		self.back.move(0,0)
		self.back.clicked.connect(self.tab.currentWidget().back) 
		self.back.setStyleSheet("border-image: url('browser/back.png') 0 0 0 0 stretch stretch; transform: scale(0.6);")
		self.forw = QPushButton("", self) 
		self.forw.resize(30,30) 
		self.forw.move(30,0)
		self.forw.clicked.connect(self.tab.currentWidget().forward) 
		self.forw.setStyleSheet("border-image: url('browser/forward.png') 0 0 0 0 stretch stretch;")
		self.home = QPushButton("", self) 
		self.home.resize(30,30) 
		self.home.move(90,0)
		self.home.clicked.connect(self.homeev) 
		self.home.setStyleSheet("border-image: url('browser/home.png') 0 0 0 0 stretch stretch;")
		self.key = QPushButton("", self) 
		self.key.resize(30,30) 
		self.key.move(60,0)
		self.key.clicked.connect(self.keymanager) 
		self.key.setStyleSheet("border-image: url('browser/key.png') 0 0 0 0 stretch stretch;")
		self.search = QPushButton("", self) 
		self.search.resize(30,30) 
		self.search.move(270,0)
		self.search.clicked.connect(self.searchev) 
		self.search.setStyleSheet("border-image: url('browser/search.png') 0 0 0 0 stretch stretch;")
		self.setGeometry(300,300,500,500)
		self.setWindowTitle('Helium Web Browser')
		self.show()
		self.tab.tabBar().tabButton(0, QTabBar.RightSide).resize(0,0)
		
	def updtitle(self,x):
		if (x.startswith("javascript:")):
			pass
		else:
			self.setWindowTitle(x)
			self.tab.setTabText(self.tab.currentIndex(),x)
			
	def tabEvent(self):
		if (self.tab.currentIndex() == 0):
			browser = QWebEngineView(self)
			browser.setUrl(QUrl('file://' + os.getcwd() + "/browser/start/index.html"))
			self.tab.addTab(browser, 'Start')
			self.tab.setCurrentIndex(self.tab.count() - 1)
			self.tab.currentWidget().page().titleChanged.connect(self.updtitle)
			self.tab.currentWidget().page().loadFinished.connect(self.loaded)
			self.back.clicked.connect(self.tab.currentWidget().back) 
			self.forw.clicked.connect(self.tab.currentWidget().forward) 
			self.home.clicked.connect(self.homeev) 
			self.search.clicked.connect(self.searchev) 
		if (self.tab.currentWidget().url().toString().startswith("javascript:")):
			pass
		else:
			self.entry.setText(self.tab.currentWidget().url().toString())
		if (self.tab.currentWidget().page().title().startswith("javascript:")):
			pass
		else:
			self.tab.setTabText(self.tab.currentIndex(),self.tab.currentWidget().page().title())
			self.setWindowTitle(self.tab.currentWidget().page().title())
		
	def resizeEvent(self, event):
		self.entry.resize(self.frameGeometry().width()-150,30)
		self.tab.resize(self.frameGeometry().width(),self.height()-30)
		self.search.move(self.frameGeometry().width()-30,0)
		QtWidgets.QMainWindow.resizeEvent(self, event)
		
	def searchev(self):
		if (self.entry.text().startswith("https://") or self.entry.text().startswith("http://")):
			self.tab.currentWidget().setUrl(QUrl(self.entry.text()))
		elif ("." in self.entry.text()):
			self.tab.currentWidget().setUrl(QUrl("http://" + self.entry.text()))
		else:
			self.tab.currentWidget().setUrl(QUrl("https://duckduckgo.com/?q=" + self.entry.text()))
	
	def keymanager(self):
		self.tab.currentWidget().setUrl(QUrl('file://' + os.getcwd() + "/browser/passwords/index.html"))
		
	def homeev(self):
		self.tab.currentWidget().setUrl(QUrl('file://' + os.getcwd() + "/browser/start/index.html"))        
		
	def loaded(self):
		if (self.tab.currentWidget().url() == QUrl('file://' + os.getcwd() + "/browser/start/index.html")):
			g = os.listdir("browser/extensions")
			for ex in g:
				print(ex)
				self.tab.currentWidget().page().runJavaScript("document.getElementById('par').innerHTML = document.getElementById('par').innerHTML + '<option>" + ex + "</option>'")
		g = os.listdir("browser/extensions")
		for ex in g:
			print(ex)
			file = open("browser/extensions/" + ex + "/main.js",'r')
			code = file.read()
			#self.tab.currentWidget().page().runJavaScript(code)
			self.tab.currentWidget().setUrl(QUrl('javascript:' + code))
			file.close()
		
	def eventFilter(self, obj, event):
		if event.type() == QEvent.KeyPress and obj is self.entry:
			if event.key() == Qt.Key_Return and self.entry.hasFocus():
				if (self.entry.text().startswith("https://") or self.entry.text().startswith("http://")):
					self.tab.currentWidget().setUrl(QUrl(self.entry.text()))
				elif ("." in self.entry.text()):
					self.tab.currentWidget().setUrl(QUrl("http://" + self.entry.text()))
				else:
					self.tab.currentWidget().setUrl(QUrl("https://duckduckgo.com/?q=" + self.entry.text()))
		return super().eventFilter(obj, event)
app = QApplication(sys.argv)
ex = Window()
sys.exit(app.exec_())
