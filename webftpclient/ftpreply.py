
from PyQt4.QtCore import * 
from PyQt4.QtNetwork import * 


class FtpReply(QNetworkReply):
	
	def __init__(self, url, parent):
		super(FtpReply, self).__init__(parent)
		print("FtpReply.init")

		self.items = []
		self.content = QByteArray()

		self.ftp = QFtp(self)
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
			self.setError(QNetworkReply.NetworkError.ContentNotFoundError, "Unknown command")
			self.error.emit(QNetworkReply.NetworkError.ContentNotFoundError)

		cmd = self.ftp.currentCommand()
		if cmd == QFtp.ConnectToHost:
			self.ftp.login()
		elif cmd == QFtp.Login:
			self.ftp.list(self.url().path())
		elif cmd == QFtp.List:
			if len(self.items) == 1:
				self.ftp.get(url().path())
			else:
				self.setListContent()
		elif cmd == QFtp.Get:
			self.setContent()

	def processListInfo(self, urlInfo):
		print("FtpReply.processListInfo")
		self.items.append(QUrlInfo(urlInfo))

	def processData(self):
		print("FtpReply.processData")
		self.content += self.ftp.readAll()

	def setContent(self):
		print("FtpReply.setContent")
		self.open(QIODevice.ReadOnly | QIODevice.Unbuffered)
		self.setHeader(QNetworkRequest.ContentLengthHeader, QVariant(self.content.size()))
		self.readyRead.emit()
		self.finished.emit()
		self.ftp.close()

	def setListContent(self):
		print("FtpReply.setListContent")
		u = self.url()
		if not u.path().endsWith("/"):
			u.setPath(u.path() + "/")

		base_url = self.url().toString()
		base_path = u.path()

		self.open(QIODevice.ReadOnly | QIODevice.Unbuffered)
		content = QString(
			"<html>\n"
			"<head>\n"
			"  <title>" + Qt.escape(base_url) + "</title>\n"
			"  <style type=\"text/css\">\n"
			"  th { background-color: #aaaaaa; color: black }\n"
			"  table { border: solid 1px #aaaaaa }\n"
			"  tr.odd { background-color: #dddddd; color: black\n }\n"
			"  tr.even { background-color: white; color: black\n }\n"
			"  </style>\n"
			"</head>\n\n"
			"<body>\n"
			"<h1>" + QString("Listing for %1").arg(base_path) + "</h1>\n\n"
			"<table align=\"center\" cellspacing=\"0\" width=\"90%\">\n"
			"<tr><th>Name</th><th>Size</th></tr>\n")

		parent = u.resolved(QUrl(".."))

		if parent.isParentOf(u):
			content += QString("<tr><td><strong><a href=\"" + parent.toString() + "\">"
				+ "Parent directory</a></strong></td><td></td></tr>\n")

		i = 0
		for item in self.items:
			child = u.resolved(QUrl(item.name()))

			if i == 0:
				content += QString("<tr class=\"odd\">")
			else:
				content += QString("<tr class=\"even\">")

			content += QString("<td><a href=\"" + child.toString() + "\">"
							   + Qt.escape(item.name()) + "</a></td>")

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
				content += QString("<td>" + QString.number(size) + " " + self.units[unit] + "</td></tr>\n")
			else:
				content += QString("<td></td></tr>\n")

			i = 1 - i

		content += QString("</table>\n</body>\n</html>\n")

		self.content = content.toUtf8()

		self.setHeader(QNetworkRequest.ContentTypeHeader, QVariant("text/html; charset=UTF-8"))
		self.setHeader(QNetworkRequest.ContentLengthHeader, QVariant(self.content.size()))
		self.readyRead.emit()
		self.finished.emit()
		self.ftp.close()

	def abort(self):
		print("FtpReply.abort")
		pass

	def bytesAvailable(self):
		print("FtpReply.bytesAvailable")
		return self.content.size() - self.offset

	def isSequential(self):
		print("FtpReply.isSequential")
		return True

	def readData(self, data, maxSize):
		print("FtpReply.readData")
		if self.offset < self.content.size():
			number = qMin(maxSize, content.size() - self.offset)
			memcpy(data, self.content.constData() + self.offset, number)
			self.offset += number
			return number
		else:
			return -1
