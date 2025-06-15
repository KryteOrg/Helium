import sys
from PySide6.QtCore import *
from PySide6.QtCore import QEvent, QByteArray
from PySide6.QtWidgets import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineUrlRequestInterceptor
from PySide6 import QtWidgets, QtGui
from PySide6.QtNetwork import QNetworkCookie
import os
import glob
import sys
import json
import urllib.request
import base64
import threading
import re
import pathlib
from urllib.parse import unquote
import urllib.request
import zipfile
import ssl

tabs = []

cookie_jar = 0

search = "https://duckduckgo.com?q="

home = ""

if os.name == "nt":
    home = str(pathlib.Path(os.environ["USERPROFILE"]) / "Documents")
    home = home.replace("\\", "/")
else:
    home = str(pathlib.Path.home())

print(home)

score = 0

if (os.path.isdir(home)):
    print("Checking folder integrity")

    if (os.path.isdir(home + "/.kryte")):
        print("Good")
        score += 1
    else:
        os.makedirs(home + "/.kryte")
        print("Created directory")

    if (os.path.isdir(home + "/.kryte/helium")):
        print("Good")
        score += 1
    else:
        os.makedirs(home + "/.kryte/helium")
        print("Created directory")

    if (os.path.isdir(home + "/.kryte/helium/cookies")):
        print("Good")
        score += 1
    else:
        os.makedirs(home + "/.kryte/helium/cookies")
        print("Created directory")

    if (os.path.isdir(home + "/.kryte/helium/extensions")):
        print("Good")
        score += 1
    else:
        os.makedirs(home + "/.kryte/helium/extensions")
        print("Created directory")

    if (os.path.isdir(home + "/.kryte/helium/passwords")):
        print("Good")
        score += 1
    else:
        os.makedirs(home + "/.kryte/helium/passwords")
        print("Created directory")

    if (os.path.isdir(home + "/.kryte/helium/settings")):
        print("Good")
        score += 1
    else:
        os.makedirs(home + "/.kryte/helium/settings")
        print("Created directory")

    if (os.path.isdir(home + "/.kryte/helium/start")):
        print("Good")
        score += 1
    else:
        os.makedirs(home + "/.kryte/helium/start")
        print("Created directory")

    if (os.path.isdir(home + "/.kryte/helium/webextensions")):
        print("Good")
        score += 1
    else:
        os.makedirs(home + "/.kryte/helium/webextensions")
        print("Created directory")

    if (score != 8):
        print("Downloading update")

        ssl._create_default_https_context = ssl._create_unverified_context

        urllib.request.urlretrieve(
            "https://kryte.org/helium/update/browserdata.zip",
            os.getcwd() + "/browserdata.zip")

        print("Extracting update")

        with zipfile.ZipFile(os.getcwd() + "/browserdata.zip", 'r') as zip_ref:
            zip_ref.extractall(home + "/.kryte/helium/")

        print("Done updating, removing temporary files")

        os.remove(os.getcwd() + "/browserdata.zip")

else:
    print("Home dir not found, Report this error to kryte, kryte@kryte.org")
    os.exit()


class WebEngineView(QWebEngineView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.page().windowCloseRequested.connect(self.close)

    def createWindow(self, windowType):
        popup = WebEngineView(self)
        popup.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        popup.resize(800, 600)

        if windowType == QWebEnginePage.WebWindowType.WebBrowserWindow:
            popup.setWindowTitle("Popup Window")
            popup.show()
            return popup

        elif windowType == QWebEnginePage.WebWindowType.WebDialog:
            popup.setWindowTitle("Web Dialog")
            popup.setWindowFlags(Qt.WindowType.Dialog)
            popup.show()
            return popup

        else:
            return popup

        return None


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global tabs
        global search
        self.setStyleSheet("background-color: #1E1E1E;")
        self.tab = QtWidgets.QTabWidget(self)
        self.tab.setStyleSheet("border: 0;")
        self.tab.addTab(QtWidgets.QLabel('Creating new tab...'), '+')
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.destroyTab)
        self.tab.move(0, 30)
        self.tab.resize(250, 30)
        self.tab.currentChanged.connect(self.tabEvent)
        self.entry = QLineEdit(self)
        self.entry.setStyleSheet("color: white;")
        self.entry.resize(100, 30)
        self.entry.move(210, 0)
        self.entry.installEventFilter(self)
        self.back = QPushButton("", self)
        self.back.resize(30, 30)
        self.back.move(0, 0)
        self.back.setStyleSheet(
            "border-image: url('" + home +
            "/.kryte/helium/back.png') 0 0 0 0 stretch stretch; transform: scale(0.6);"
        )
        self.forw = QPushButton("", self)
        self.forw.resize(30, 30)
        self.forw.move(30, 0)
        self.forw.setStyleSheet(
            "border-image: url('" + home +
            "/.kryte/helium/forward.png') 0 0 0 0 stretch stretch;")
        self.key = QPushButton("", self)
        self.key.resize(30, 30)
        self.key.move(60, 0)
        self.key.setStyleSheet(
            "border-image: url('" + home +
            "/.kryte/helium/key.png') 0 0 0 0 stretch stretch;")
        self.home = QPushButton("", self)
        self.home.resize(30, 30)
        self.home.move(90, 0)
        self.home.setStyleSheet(
            "border-image: url('" + home +
            "/.kryte/helium/home.png') 0 0 0 0 stretch stretch;")
        self.refresh = QPushButton("", self)
        self.refresh.resize(30, 30)
        self.refresh.move(120, 0)
        self.refresh.setStyleSheet(
            "border-image: url('" + home +
            "/.kryte/helium/refresh.png') 0 0 0 0 stretch stretch;")
        self.extension = QPushButton("", self)
        self.extension.resize(30, 30)
        self.extension.move(150, 0)
        self.extension.setStyleSheet(
            "border-image: url('" + home +
            "/.kryte/helium/extension.png') 0 0 0 0 stretch stretch;")
        self.cookie = QPushButton("", self)
        self.cookie.resize(30, 30)
        self.cookie.move(240, 0)
        self.cookie.setStyleSheet(
            "border-image: url('" + home +
            "/.kryte/helium/cookie.png') 0 0 0 0 stretch stretch;")
        self.search = QPushButton("", self)
        self.search.resize(30, 30)
        self.search.move(270, 0)
        self.search.setStyleSheet(
            "border-image: url('" + home +
            "/.kryte/helium/search.png') 0 0 0 0 stretch stretch;")
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Helium Web Browser')
        self.show()
        self.tab.tabBar().tabButton(0,
                                    QTabBar.ButtonPosition.RightSide).resize(
                                        0, 0)
        self.profile = QWebEngineProfile.defaultProfile()
        self.settings = self.profile.settings()
        self.settings.setAttribute(
            self.settings.WebAttribute.FullScreenSupportEnabled, True)
        self.cookie_store = self.profile.cookieStore()
        self.cookie_store.cookieAdded.connect(self.cookieAdded)
        for entry in os.scandir(home + "/.kryte/helium/cookies"):
            if entry.is_file():
                with open(entry.path) as f:
                    try:
                        c = json.loads(f.read())

                        cookie = QNetworkCookie()

                        cookie.setName(QByteArray(c["name"]))

                        cookie.setValue(
                            QByteArray(
                                base64.b64decode(c["value"].encode(
                                    "ascii")).decode("ascii")))

                        cookie.setDomain(c["domain"])

                        cookie.setPath(c["path"])

                        origin = QUrl("https://" + cookie.domain().lstrip('.'))

                        self.cookie_store.setCookie(cookie, origin)
                    except:
                        print("Cookie " + str(f) + " failed to load")
        try:
            if (sys.argv[1:][0]):
                self.createTab(sys.argv[1:][0])
        except:
            if os.name == "nt":
                self.createTab('file://' + home.replace("C:/", "/C:/") +
                               "/.kryte/helium/start/index.html")
                return

            self.createTab('file://' + home +
                           "/.kryte/helium/start/index.html")

        with open(home + "/.kryte/helium/settings/settings.json") as f:
            c = json.loads(f.read())

            search = c["search"]

        self.back.clicked.connect(self.tab.currentWidget().back)
        self.forw.clicked.connect(self.tab.currentWidget().forward)
        self.refresh.clicked.connect(self.tab.currentWidget().reload)
        self.home.clicked.connect(self.homeev)
        self.key.clicked.connect(self.keymanager)
        self.extension.clicked.connect(self.extev)
        self.search.clicked.connect(self.searchev)
        self.cookie.clicked.connect(self.cookiejv)

    def saveSettings(self, searcht):
        global search

        search = searcht

        with open(home + "/.kryte/helium/settings/settings.json", "w") as f:
            f.write('{"search": "' + searcht + '"}')

    def destroyTab(self, index):
        widget = self.tab.widget(index)
        widget.deleteLater()
        self.tab.removeTab(index)

    def handleSearch(self):
        global search
        if (self.entry.text().startswith("https://")
                or self.entry.text().startswith("http://")):
            self.tab.currentWidget().setUrl(QUrl(self.entry.text()))
        elif (self.entry.text().startswith("browser://")):
            _, _, res = self.entry.text().partition("browser://")
            self.tab.currentWidget().setUrl(
                QUrl('file://' + home + "/.kryte/helium/" + res))
        elif ("." in self.entry.text()):
            self.tab.currentWidget().setUrl(QUrl("http://" +
                                                 self.entry.text()))
        else:
            self.tab.currentWidget().setUrl(QUrl(search + self.entry.text()))

    def fullscreenReq(self, request):
        if request.toggleOn():
            self.showFullScreen()
        else:
            self.showNormal()
        request.accept()

    def cookieAdded(self, cookie):
        global cookie_jar

        print("Cookie added")

        cookie_jar += 1

        with open(
                home + "/.kryte/helium/cookies/" +
                cookie.name().data().decode("utf-8") + "-" + cookie.domain(),
                "w") as f:
            f.write('{"name": "' + cookie.name().data().decode("utf-8") +
                    '","value": "' +
                    base64.b64encode(cookie.value().data()).decode("ascii") +
                    '","domain": "' + cookie.domain() + '","path": "' +
                    cookie.path() + '"}')

    def updtitle(self, x):
        if (x.startswith("javascript:")):
            pass
        else:
            self.setWindowTitle(x + " - Helium Web Browser")
            self.tab.setTabText(self.tab.currentIndex(), x)

    def createTab(self, url):
        browser = WebEngineView(self)
        browser.setUrl(QUrl(url))
        browser.page().fullScreenRequested.connect(self.fullscreenReq)
        self.tab.addTab(browser, '...')
        self.tab.setCurrentIndex(self.tab.count() - 1)
        self.tab.currentWidget().page().titleChanged.connect(self.updtitle)
        self.tab.currentWidget().page().loadFinished.connect(self.loaded)
        self.tab.currentWidget().page().loadStarted.connect(self.loadStart)

    def tabEvent(self):
        if (self.tab.currentIndex() == 0):
            if os.name == "nt":
                self.createTab('file://' + home.replace("C:/", "/C:/") +
                               "/.kryte/helium/start/index.html")
                return

            self.createTab('file://' + home +
                           "/.kryte/helium/start/index.html")
        elif (self.tab.currentWidget().url().toString().startswith(
                "javascript:")):
            pass
        else:
            self.entry.setText(self.tab.currentWidget().url().toString())
            self.setWindowTitle(self.tab.currentWidget().page().title() +
                                " - Helium Web Browser")
            self.tab.setTabText(self.tab.currentIndex(),
                                self.tab.currentWidget().page().title())
            self.setWindowTitle(self.tab.currentWidget().page().title() +
                                " - Helium Web Browser")
            if (self.tab.currentWidget().page().url().toString().startswith(
                    "file://" + home + "/.kryte/helium/")):
                _, _, res = self.tab.currentWidget().page().url().toString(
                ).partition("browser/")
                self.entry.setText("browser://" + res)
            else:
                self.entry.setText(
                    self.tab.currentWidget().page().url().toString())
            try:
                self.back.clicked.disconnect()
            except Exception:
                pass
            try:
                self.forw.clicked.disconnect()
            except Exception:
                pass
            try:
                self.refresh.clicked.disconnect()
            except Exception:
                pass
            self.back.clicked.connect(self.tab.currentWidget().back)
            self.forw.clicked.connect(self.tab.currentWidget().forward)
            self.refresh.clicked.connect(self.tab.currentWidget().reload)
        if (self.tab.currentWidget().page().title().startswith("javascript:")):
            pass

    def resizeEvent(self, event):
        self.entry.resize(self.frameGeometry().width() - 300, 30)
        self.tab.resize(self.frameGeometry().width() + 2, self.height() - 28)
        self.search.move(self.frameGeometry().width() - 30, 0)
        self.cookie.move(self.frameGeometry().width() - 60, 0)
        QtWidgets.QMainWindow.resizeEvent(self, event)

    def extev(self):
        if os.name == "nt":
            self.tab.currentWidget().setUrl(
                QUrl('file://' + home.replace("C:/", "/C:/") +
                     "/.kryte/helium/webextensions/index.html"))
            return

        self.tab.currentWidget().setUrl(
            QUrl('file://' + home + "/.kryte/helium/webextensions/index.html"))

    def cookiejv(self):
        global cookie_jar

        total = sum([
            len(files)
            for r, d, files in os.walk(home + "/.kryte/helium/cookies/")
        ])

        if (QMessageBox.question(
                self,
                "Your cookie jar",
                "Total cookies: " + str(total) +
                "\nYummy!\n\nDo you want to clear all the cookies?",
                buttons=QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                defaultButton=QMessageBox.StandardButton.No) ==
                QMessageBox.StandardButton.Yes):
            files = glob.glob(os.getcwd() + '/browser/cookies/*')
            for f in files:
                os.remove(f)
            cookie_jar = 0

    def searchev(self):
        self.handleSearch()

    def keymanager(self):
        if os.name == "nt":
            self.tab.currentWidget().setUrl(
                QUrl('file://' + home.replace("C:/", "/C:/") +
                     "/.kryte/helium/passwords/index.html"))
            return

        self.tab.currentWidget().setUrl(
            QUrl('file://' + home + "/.kryte/helium/passwords/index.html"))

    def homeev(self):
        if os.name == "nt":
            self.tab.currentWidget().setUrl(
                QUrl('file://' + home.replace("C:/", "/C:/") +
                     "/.kryte/helium/start/index.html"))
            return

        self.tab.currentWidget().setUrl(
            QUrl('file://' + home + "/.kryte/helium/passwords/index.html"))

    def loadStart(self):
        g = os.listdir(home + "/.kryte/helium/extensions")
        for ex in g:
            print(ex)
            if (self.tab.currentWidget().page().url().toString() == "file://" +
                    home + "/.kryte/helium/webextensions/index.html"):
                self.tab.currentWidget().page().runJavaScript(
                    "document.getElementById('extlist').innerHTML = document.getElementById('extlist').innerHTML + '<a href=\"../extensions/"
                    + ex + "/window.html\">" + ex + "</a><br>'")

            file = open("browser/extensions/" + ex + "/main.js", 'r')
            code = file.read()
            self.tab.currentWidget().page().runJavaScript(code)
            file.close()

    def loaded(self):
        self.tab.setTabText(self.tab.currentIndex(),
                            self.tab.currentWidget().page().title())
        self.setWindowTitle(self.tab.currentWidget().page().title() +
                            " - Helium Web Browser")
        if (self.tab.currentWidget().page().url().toString().startswith(
                "file://" + home + "/.kryte/helium/")):
            _, _, res = self.tab.currentWidget().page().url().toString(
            ).partition("browser/")
            self.entry.setText("browser://" + res)
        else:
            self.entry.setText(
                self.tab.currentWidget().page().url().toString())

        if (re.search(r"/browser/extensions/.*/window.html#writeFile,.*$",
                      self.tab.currentWidget().page().url().toString())):
            _, _, res = self.tab.currentWidget().page().url().toString(
            ).partition("#writeFile,")

            writeSplit = res.split(",")

            print("write to: " + writeSplit[0])
            print("write what: " + writeSplit[1])

            with open(
                    home + "/.kryte/helium/extensions/" +
                    unquote(writeSplit[0]), "w") as f:
                f.write(
                    base64.b64decode(unquote(
                        writeSplit[1]).encode("ascii")).decode("ascii"))
                f.close()

        if (re.search(r"/browser/settings/index.html#newSearch,.*$",
                      self.tab.currentWidget().page().url().toString())):
            _, _, res = self.tab.currentWidget().page().url().toString(
            ).partition("#newSearch,")

            search = base64.b64decode(
                unquote(res.split(",")[0]).encode("ascii")).decode("ascii")

            self.saveSettings(search)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and obj is self.entry:
            if event.key() == Qt.Key.Key_Return and self.entry.hasFocus():
                self.handleSearch()
        return super().eventFilter(obj, event)


app = QApplication(sys.argv)
ex = Window()
sys.exit(app.exec())
