#!/usr/bin/env python

#use python strings instead of QString
import sip
sip.setapi("QString", 2)

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from ftpview import FtpView


def main():
	app = QApplication(sys.argv)

	view = FtpView()
	view.setUrl(QUrl(u"ftp://ftp.qt.nokia.com"))
	view.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()

