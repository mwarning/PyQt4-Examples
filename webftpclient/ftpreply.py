
from PyQt4 import QtCore, QtNetwork


class FtpReply(QtNetwork.QNetworkReply):

    def __init__(self, url, parent):
        super(FtpReply, self).__init__(parent)
        print("FtpReply.init")

        self.items = []
        self.content = ""

        self.ftp = QtNetwork.QFtp(self)
        self.ftp.listInfo.connect(self.processListInfo)
        self.ftp.readyRead.connect(self.processData)
        self.ftp.commandFinished.connect(self.processCommand)

        self.offset = 0
        self.units = ["bytes", "K", "M", "G", "Ti", "Pi", "Ei", "Zi", "Yi"]

        self.setUrl(url)
        self.ftp.connectToHost(url.host())

    def processCommand(self, _, err):
        print("FtpReply.processCommand")

        if err:
            self.setError(QtNetwork.QNetworkReply.NetworkError.ContentNotFoundError, "Unknown command")
            self.error.emit(QtNetwork.QNetworkReply.NetworkError.ContentNotFoundError)

        cmd = self.ftp.currentCommand()
        if cmd == QtNetwork.QFtp.ConnectToHost:
            self.ftp.login()
        elif cmd == QtNetwork.QFtp.Login:
            self.ftp.list(self.url().path())
        elif cmd == QtNetwork.QFtp.List:
            if len(self.items) == 1:
                self.ftp.get(url().path())
            else:
                self.setListContent()
        elif cmd == QtNetwork.QFtp.Get:
            self.setContent()

    def processListInfo(self, urlInfo):
        print("FtpReply.processListInfo")
        self.items.append(QtNetwork.QUrlInfo(urlInfo))

    def processData(self):
        print("FtpReply.processData")
        self.content += self.ftp.readAll()

    def setContent(self):
        print("FtpReply.setContent")
        self.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Unbuffered)
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, QVariant(len(self.content)))
        self.readyRead.emit()
        self.finished.emit()
        self.ftp.close()

    def setListContent(self):
        print("FtpReply.setListContent")
        u = self.url()
        if not u.path().endswith("/"):
            u.setPath(u.path() + "/")

        base_url = self.url().toString()
        base_path = u.path()

        self.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Unbuffered)
        content = (
            u'<html>\n'
            '<head>\n'
            '  <title>%s</title>\n'
            '  <style type="text/css">\n'
            '  th { background-color: #aaaaaa; color: black }\n'
            '  table { border: solid 1px #aaaaaa }\n'
            '  tr.odd { background-color: #dddddd; color: black\n }\n'
            '  tr.even { background-color: white; color: black\n }\n'
            '  </style>\n'
            '</head>\n\n'
            '<body>\n'
            '<h1>Listing for %s</h1>\n\n'
            '<table align="center" cellspacing="0" width="90%%">\n'
            '<tr><th>Name</th><th>Size</th></tr>\n' % (QtCore.Qt.escape(base_url), base_path))

        parent = u.resolved(QtCore.QUrl(".."))

        if parent.isParentOf(u):
            content += (u'<tr><td><strong><a href="%s">' % parent.toString()
            + u'Parent directory</a></strong></td><td></td></tr>\n')

        i = 0
        for item in self.items:
            child = u.resolved(QtCore.QUrl(item.name()))

            if i == 0:
                content += u'<tr class="odd">'
            else:
                content += u'<tr class="even">'

            content += u'<td><a href="%s">%s</a></td>' % (child.toString(), QtCore.Qt.escape(item.name()))

            size = item.size()
            unit = 0
            while size:
                new_size = size/1024
                if new_size and unit < len(self.units):
                    size = new_size
                    unit += 1
                else:
                    break

            if item.isFile():
                content += u'<td>%s %s</td></tr>\n' % (str(size), self.units[unit])
            else:
                content += u'<td></td></tr>\n'

            i = 1 - i

        content += u'</table>\n</body>\n</html>\n'

        self.content = content.encode('utf-8')

        self.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, QtCore.QVariant("text/html; charset=UTF-8"))
        self.setHeader(QtNetwork.QNetworkRequest.ContentLengthHeader, QtCore.QVariant(len(self.content)))
        self.readyRead.emit()
        self.finished.emit()
        self.ftp.close()

    def abort(self):
        print("FtpReply.abort")
        pass

    def bytesAvailable(self):
        print("FtpReply.bytesAvailable")
        return len(self.content) - self.offset

    def isSequential(self):
        print("FtpReply.isSequential")
        return True

    def readData(self, maxSize):
        print("FtpReply.readData")
        if self.offset < len(self.content):
            number = min(maxSize, len(self.content) - self.offset)
            data = self.content[self.offset:number]
            self.offset += number
            return data
        return None
