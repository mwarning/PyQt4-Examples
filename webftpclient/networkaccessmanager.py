
from PyQt4.QtCore import * 
from PyQt4.QtNetwork import * 
from PyQt4.QtWebKit import *
from ftpreply import FtpReply


class NetworkAccessManager(QNetworkAccessManager):
	
	def __init__(self, manager, parent):
		super(NetworkAccessManager, self).__init__(parent)
		print("NetworkAccessManager.init")

		self.setCache(manager.cache())
		self.setCookieJar(manager.cookieJar())
		self.setProxy(manager.proxy())
		self.setProxyFactory(manager.proxyFactory())

	def createRequest(self, operation, request, device):
		print("NetworkAccessManager.createRequest")
		if request.url().scheme() != "ftp":
			return QNetworkAccessManager.createRequest(self, operation, request, device)

		if operation == QNetworkAccessManager.GetOperation:
			# Handle ftp:// URLs separately by creating custom QNetworkReply objects.
			return FtpReply(request.url(), self)
		else:
			return QNetworkAccessManager.createRequest(self, operation, request, device)
