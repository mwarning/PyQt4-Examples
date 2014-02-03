
from PyQt4 import QtWebKit
from downloader import Downloader
from networkaccessmanager import NetworkAccessManager


class FtpView(QtWebKit.QWebView):
    def __init__(self):
        super(FtpView, self).__init__()
        print("FtpView.init")

        oldManager = self.page().networkAccessManager()
        newManager = NetworkAccessManager(oldManager, self)
        self.page().setNetworkAccessManager(newManager)

        self.page().setForwardUnsupportedContent(True)
        self.downloader = Downloader(self, newManager)

        self.page().unsupportedContent.connect(self.downloader.saveFile)
        self.page().downloadRequested.connect(self.downloader.startDownload)

        self.urlChanged.connect(self.updateWindowTitle)

    def updateWindowTitle(self, url):
        print("FtpView.updateWindowTitle")
        self.setWindowTitle("FTP Client - %s" % url.toString())
