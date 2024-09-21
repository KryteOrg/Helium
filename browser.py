import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtWidgets, QtGui
import os

class Window(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		self.entry = QLineEdit(self)
		self.entry.resize(250,30)
		self.entry.move(30,0)
		self.entry.installEventFilter(self)
		self.home = QPushButton("", self) 
		self.home.resize(30,30) 
		self.home.move(0,0)
		self.home.clicked.connect(self.homeev) 
		self.home.setStyleSheet("border-image: url(home.png) 0 0 0 0 stretch stretch;")
		self.search = QPushButton("", self) 
		self.search.resize(30,30) 
		self.search.move(270,0)
		self.search.clicked.connect(self.searchev) 
		self.search.setStyleSheet("border-image: url(search.png) 0 0 0 0 stretch stretch;")
		self.browser = QWebEngineView(self)
		self.browser.titleChanged.connect(self.title)
		self.browser.setUrl(QUrl('file://' + os.getcwd() + "/browser/start/index.html"))
		self.browser.move(0,30)
		self.setGeometry(300,300,500,500)
		self.setWindowTitle('Helium Web Browser')
		self.show()
	def title(self,x):
		QApplication.setApplicationName(x + " - Helium Web Browser")
	def resizeEvent(self, event):
		self.entry.resize(self.frameGeometry().width()-60,30)
		self.browser.resize(self.frameGeometry().width(),self.height()-30)
		self.search.move(self.frameGeometry().width()-30,0)
		QtWidgets.QMainWindow.resizeEvent(self, event)
	def searchev(self):
		if (self.entry.text().startswith("https://") or self.entry.text().startswith("http://")):
			self.browser.setUrl(QUrl(self.entry.text()))
		elif ("." in self.entry.text()):
			self.browser.setUrl(QUrl(self.entry.text()))
		else:
			self.browser.setUrl(QUrl("https://duckduckgo.com/?q=" + self.entry.text()))
	def homeev(self):
		self.browser.setUrl(QUrl('file://' + os.getcwd() + "/browser/start/index.html"))        
	def eventFilter(self, obj, event):
		if event.type() == QEvent.KeyPress and obj is self.entry:
			if event.key() == Qt.Key_Return and self.entry.hasFocus():
				if (self.entry.text().startswith("https://") or self.entry.text().startswith("http://")):
					self.browser.setUrl(QUrl(self.entry.text()))
				elif ("." in self.entry.text()):
					self.browser.setUrl(QUrl("http://" + self.entry.text()))
				else:
					self.browser.setUrl(QUrl("https://duckduckgo.com/?q=" + self.entry.text()))
		return super().eventFilter(obj, event)
app = QApplication(sys.argv)
ex = Window()
sys.exit(app.exec_())
