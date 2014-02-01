#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import * 
from PyQt4.QtWebKit import *
from ftpview import FtpView


def main():
	app = QApplication(sys.argv)

	view = FtpView()
	view.setUrl(QUrl("ftp://ftp.qt.nokia.com"))
	view.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()

