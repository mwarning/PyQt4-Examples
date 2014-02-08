#!/usr/bin/env python

#use python strings instead of QString
import sip
sip.setapi("QString", 2)

import sys
from PyQt4 import QtGui, QtCore, QtNetwork, QtWebKit


class NetworkReply(QtNetwork.QNetworkReply):

    def __init__(self, url, parent):
        super(NetworkReply, self).__init__(parent)
        print("NetworkReply.init")

        self.content = ""
        self.offset = 0

        self.setUrl(url)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.setContent)
        timer.start(1000)

    def setContent(self):
        print("NetworkReply.setContent")

        content = u'<html><head><title>Test</title></head><body>'
        for i in range(0, 100):
            content += 'number %s of %s<br>' % (i, 100)
        content += u'</body></html>'

        self.content = content.encode('utf-8')
        self.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Unbuffered)
        self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, QtCore.QVariant("text/html; charset=UTF-8"))
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, QtCore.QVariant(len(self.content)))

        self.metaDataChanged.emit()
        self.readyRead.emit()
        self.finished.emit()

    def abort(self):
        print("NetworkReply.abort")
        pass

    def bytesAvailable(self):
        print("NetworkReply.bytesAvailable")
        return len(self.content) - self.offset + QtNetwork.QNetworkReply.bytesAvailable(self)

    def isSequential(self):
        print("NetworkReply.isSequential")
        return True

    def readData(self, maxSize):
        print("NetworkReply.readData")
        if self.offset < len(self.content):
            number = min(maxSize, len(self.content) - self.offset)
            data = self.content[self.offset:self.offset+number]
            self.offset += number
            return data
        return None


class NetworkAccessManager(QtNetwork.QNetworkAccessManager):

    def __init__(self, manager, parent):
        super(NetworkAccessManager, self).__init__(parent)
        print("NetworkAccessManager.init")

        self.setCache(manager.cache())
        self.setCookieJar(manager.cookieJar())
        self.setProxy(manager.proxy())
        self.setProxyFactory(manager.proxyFactory())

    def createRequest(self, operation, request, device):
        print("NetworkAccessManager.createRequest")

        if operation == QtNetwork.QNetworkAccessManager.GetOperation:
            return NetworkReply(request.url(), self)
        else:
            return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, device)


class WebView(QtWebKit.QWebView):
    def __init__(self):
        super(WebView, self).__init__()
        print("WebView.init")

        oldManager = self.page().networkAccessManager()
        newManager = NetworkAccessManager(oldManager, self)
        self.page().setNetworkAccessManager(newManager)

        self.page().setForwardUnsupportedContent(True)

        self.urlChanged.connect(self.updateWindowTitle)

    def updateWindowTitle(self, url):
        print("WebView.updateWindowTitle")
        self.setWindowTitle("Content View - %s" % url.toString())


def main():
    app = QtGui.QApplication(sys.argv)

    view = WebView()
    view.setUrl(QtCore.QUrl(u"foo://some_dummy_url"))
    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

