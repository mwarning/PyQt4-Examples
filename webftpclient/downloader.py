
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


class Downloader(QObject):

	def __init__(self, parentWidget, manager):
		super(Downloader, self).__init__(parentWidget)
		print("Downloader.init")
		
		self.manager = manager
		self.reply = None
		self.downloads = {}
		self.path = ""
		self.parentWidget = parentWidget

	def chooseSaveFile(self, url):
		print("Downloader.chooseSaveFile")
		fileName = url.path().split("/").last()
		if not path.isEmpty():
			fileName = QDir(path).filePath(fileName)

		return QFileDialog.getSaveFileName(self.parentWidget, u"Save File", fileName);

	def startDownload(self, request):
		print("Downloader.startDownload")
		self.downloads[request.url().toString()] = self.chooseSaveFile(request.url())

		reply = self.manager.get(request)
		reply.finished.connect(self.finishDownload())

	def saveFile(self, reply):
		print("Downloader.saveFile")
		newPath = self.downloads[reply.url().toString()]

		if newPath.isEmpty():
			newPath = self.chooseSaveFile(reply.url())

		if not newPath.isEmpty():
			file = QFile(newPath)
			if file.open(QIODevice.WriteOnly):
				file.write(reply.readAll())
				file.close()
				path = QDir(newPath).dirName()
				QMessageBox.information(parentWidget, u"Download Completed", u"Saved '%s'." % newPath)
			else:
				QMessageBox.warning(parentWidget, u"Download Failed", u"Failed to save the file.")

	def finishDownload(self):
		print("Downloader.finishDownload")
		reply = self.sender()
		self.saveFile(reply)
		self.downloads.remove(reply.url().toString())
		reply.deleteLater()
