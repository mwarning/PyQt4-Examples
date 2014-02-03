
from PyQt4 import QtNetwork
from ftpreply import FtpReply


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
		if request.url().scheme() != "ftp":
			return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, device)

		if operation == QtNetwork.QNetworkAccessManager.GetOperation:
			# Handle ftp:// URLs separately by creating custom QNetworkReply objects.
			return FtpReply(request.url(), self)
		else:
			return QtNetwork.QNetworkAccessManager.createRequest(self, operation, request, device)
