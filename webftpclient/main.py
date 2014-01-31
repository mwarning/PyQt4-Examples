#!/usr/bin/env python

from PyQt4.QtGui import *
from PyQt4.QtCore import * 
from PyQt4.QtWebKit import *
from ftpview import FtpView


if __name__ == "__main__":
	app = QApplication([])

	view = FtpView()
	view.setUrl(QUrl("ftp://ftp.qt.nokia.com"))
	view.show()

	app.exec_()

