#ifndef MAIN_H
#define MAIN_H

#include <QtGui>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QtNetwork>
#include <QNetworkAccessManager>
#include <QtWebKit/QtWebKit>
#if QT_VERSION >= 0x050200
#include <QtWebKitWidgets/QtWebKitWidgets>
#include <QtWebKitWidgets/QWebView>
#else
#include <QWebView>
#include <QWebFrame>
#include <QWebPage>
#endif
#include <QObject>
#include <QUrl>


class NetworkReply : public QNetworkReply
{
    Q_OBJECT

public:
    NetworkReply(const QUrl &url);
    void abort();
    qint64 bytesAvailable() const;
    bool isSequential() const;

private slots:
    void setContent();

protected:
    qint64 readData(char *data, qint64 maxSize);

    QByteArray content;
    qint64 offset;
};

class WebView : public QWebView
{
    Q_OBJECT

public:
    WebView();

private slots:
    void updateWindowTitle(const QUrl &url);
	void onLoadFinish();
};

class NetworkAccessManager : public QNetworkAccessManager
{
    Q_OBJECT

public:
    NetworkAccessManager(QNetworkAccessManager *oldManager, QObject *parent = 0);

protected:
    QNetworkReply *createRequest(Operation operation, const QNetworkRequest &request, QIODevice *device);
};

#endif
