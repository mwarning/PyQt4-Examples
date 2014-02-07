
#include <iostream>

#include "main.h"


QByteArray createHtmlPage() {
	QString content("<html><head><title>Test</title></head><body>");
	
	for(int i = 0; i < 100; ++i) {
		content += QString("number " +QString::number(i)  + " of 100<br>");
	}
	content += QString("</body></html>");
	
	return content.toUtf8();
}


NetworkReply::NetworkReply(const QUrl &url)
    : QNetworkReply()
{
	qDebug("NetworkReply.init");
	
	QTimer *timer = new QTimer(this);
	connect(timer, SIGNAL(timeout()),
            this, SLOT(setContent()));
	timer->start(1000);
	
    offset = 0;
    setUrl(url);
}

void NetworkReply::setContent()
{
	qDebug("NetworkReply.setContent");
	
	this->content = createHtmlPage();
	
	open(ReadOnly | Unbuffered);
	setHeader(QNetworkRequest::ContentTypeHeader, QVariant("text/html; charset=UTF-8"));
	setHeader(QNetworkRequest::ContentLengthHeader, QVariant(content.size()));
	emit metaDataChanged();
	emit readyRead();
	QCoreApplication::processEvents();
	emit finished();
}

void NetworkReply::abort()
{
	//qDebug("NetworkReply.abort\n");
}

qint64 NetworkReply::bytesAvailable() const
{
	qDebug("NetworkReply.bytesAvailable: %lli", content.size() - offset);
    return content.size() - offset;
}

bool NetworkReply::isSequential() const
{
	qDebug("NetworkReply.isSequential");
    return true;
}

qint64 NetworkReply::readData(char *data, qint64 maxSize)
{
	qDebug("NetworkReply.readData");
    if (offset < content.size()) {
        qint64 number = qMin(maxSize, content.size() - offset);
        memcpy(data, content.constData() + offset, number);
        offset += number;
        return number;
    } else
        return -1;
}
	
NetworkAccessManager::NetworkAccessManager(QNetworkAccessManager *manager, QObject *parent)
    : QNetworkAccessManager(parent)
{
	qDebug("NetworkAccessManager.init");
    setCache(manager->cache());
    setCookieJar(manager->cookieJar());
    setProxy(manager->proxy());
    setProxyFactory(manager->proxyFactory());
}

QNetworkReply *NetworkAccessManager::createRequest(
    QNetworkAccessManager::Operation operation, const QNetworkRequest &request,
    QIODevice *device)
{
	qDebug("NetworkAccessManager.createRequest");

    if (operation == GetOperation)
        return new NetworkReply(request.url());
    else
        return QNetworkAccessManager::createRequest(operation, request, device);
}

WebView::WebView()
{
	qDebug("WebView.init");
	
    QNetworkAccessManager *oldManager = page()->networkAccessManager();
    NetworkAccessManager *newManager = new NetworkAccessManager(oldManager, this);
    page()->setNetworkAccessManager(newManager);

    page()->setForwardUnsupportedContent(true);

    connect(this, SIGNAL(urlChanged(const QUrl &)),
            this, SLOT(updateWindowTitle(const QUrl &)));

	connect(page(), SIGNAL(loadFinished(bool)),
            this, SLOT(onLoadFinish()));
}

void WebView::updateWindowTitle(const QUrl &url)
{
	qDebug("NetworkReply.updateWindowTitle");
    setWindowTitle(tr("FTP Client - %1").arg(url.toString()));
}

/* Check if all content was displayed */
void WebView::onLoadFinish()
{
	qDebug("onLoadFinish");
	if(page()->currentFrame()->toHtml().toUtf8() == createHtmlPage()) {
		qDebug("Success");
		//QCoreApplication::exit(0);
	} else {
		qDebug("Failed");
		//QCoreApplication::exit(1);
	}
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    WebView view;
    view.setUrl(QUrl("foo://bar.ham"));
    view.show();

    return app.exec();
}
