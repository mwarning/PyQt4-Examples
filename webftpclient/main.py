#!/usr/bin/env python

#use python strings instead of QString
import sip
sip.setapi("QString", 2)

import sys
from PyQt4 import QtCore, QtGui
from ftpview import FtpView


def main():
	app = QtGui.QApplication(sys.argv)

	view = FtpView()
	view.setUrl(QtCore.QUrl(u"ftp://ftp.qt.nokia.com"))
	view.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()

