
Test case for https://bugreports.qt-project.org/browse/QTBUG-27469

The test case works for revision 9d6c186f418ea77f202404408aa6692805038bea,
but revison 6d09a6ff6653aba1f36d66739f584d0795870eaa does not.

To check out a specific revision, use:
```
git clone git://gitorious.org/qt/qt.git
git checkout <revison>
```

The following stack traces are for the calls of NetworkReply::readData() in main.cpp.


Stack trace for the good version (9d6c18..). readData is called once.

```
Breakpoint 1, NetworkReply::readData (this=0x48bbc0, data=0x53f6c8 "\240\366S", maxSize=2048) at main.cpp:65
65              qDebug("NetworkReply.readData: %p %lli", data, maxSize);
(gdb) bt
#0  NetworkReply::readData (this=0x48bbc0, data=0x53f6c8 "\240\366S", maxSize=2048) at main.cpp:65
#1  0x00007ffff542164d in QIODevice::read (this=0x48bbc0, data=0x53f6c8 "\240\366S", maxSize=2048) at io/qiodevice.cpp:858
#2  0x00007ffff5421aa4 in QIODevice::read (this=0x48bbc0, maxSize=2048) at io/qiodevice.cpp:964
#3  0x00007ffff71a3de3 in WebCore::QNetworkReplyHandler::forwardData() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#4  0x00007ffff71a4a6f in WebCore::QNetworkReplyHandler::qt_static_metacall(QObject*, QMetaObject::Call, int, void**) ()
   from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#5  0x00007ffff54bd683 in QMetaObject::activate (sender=0x48bbc0, m=0x7ffff56547e0, local_signal_index=0, argv=0x0)
    at kernel/qobject.cpp:3546
#6  0x00007ffff551acfb in QIODevice::readyRead (this=0x48bbc0) at .moc/debug-shared/moc_qiodevice.cpp:105
#7  0x0000000000404bb4 in NetworkReply::setContent (this=0x48bbc0) at main.cpp:42
#8  0x0000000000405a28 in NetworkReply::qt_static_metacall (_o=0x48bbc0, _c=QMetaObject::InvokeMetaMethod, _id=0, _a=0x7fffffffd4c0)
    at moc_main.cpp:49
#9  0x00007ffff54bd683 in QMetaObject::activate (sender=0x488aa0, m=0x7ffff5655e40, local_signal_index=0, argv=0x0)
    at kernel/qobject.cpp:3546
#10 0x00007ffff551db93 in QTimer::timeout (this=0x488aa0) at .moc/debug-shared/moc_qtimer.cpp:148
#11 0x00007ffff54c696f in QTimer::timerEvent (this=0x488aa0, e=0x7fffffffddf0) at kernel/qtimer.cpp:280
#12 0x00007ffff54b804a in QObject::event (this=0x488aa0, e=0x7fffffffddf0) at kernel/qobject.cpp:1156
#13 0x00007ffff58d2edc in QApplicationPrivate::notify_helper (this=0x40a230, receiver=0x488aa0, e=0x7fffffffddf0)
    at kernel/qapplication.cpp:4495
```

Stack traces for the bad version (6d09a6..). readData is called twice.

```
Breakpoint 1, NetworkReply::readData (this=0x494620, data=0x547ee8 "\300~T", maxSize=512) at main.cpp:65
65              qDebug("NetworkReply.readData: %p %lli", data, maxSize);
(gdb) bt
#0  NetworkReply::readData (this=0x494620, data=0x547ee8 "\300~T", maxSize=512) at main.cpp:65
#1  0x00007ffff3cfa64d in QIODevice::read (this=0x494620, data=0x547ee8 "\300~T", maxSize=512) at io/qiodevice.cpp:858
#2  0x00007ffff3cfaaa4 in QIODevice::read (this=0x494620, maxSize=512) at io/qiodevice.cpp:964
#3  0x00007ffff3cfbafd in QIODevicePrivate::peek (this=0x4947e0, maxSize=512) at io/qiodevice.cpp:1467
#4  0x00007ffff3cfbc5b in QIODevice::peek (this=0x494620, maxSize=512) at io/qiodevice.cpp:1533
#5  0x00007ffff6e88e3c in QtMIMETypeSniffer::sniff() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#6  0x00007ffff6e88c79 in QtMIMETypeSniffer::QtMIMETypeSniffer(QNetworkReply*, QString const&, bool) ()
   from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#7  0x00007ffff6bb31df in WebCore::QNetworkReplyWrapper::receiveMetaData() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#8  0x00007ffff6bb69d0 in WebCore::QNetworkReplyWrapper::qt_static_metacall(QObject*, QMetaObject::Call, int, void**) ()
   from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#9  0x00007ffff3d96683 in QMetaObject::activate (sender=0x494620, m=0x7ffff3f2d7e0, local_signal_index=0, argv=0x0)
    at kernel/qobject.cpp:3546
#10 0x00007ffff3df3cfb in QIODevice::readyRead (this=0x494620) at .moc/debug-shared/moc_qiodevice.cpp:105
#11 0x0000000000404d54 in NetworkReply::setContent (this=0x494620) at main.cpp:42
#12 0x0000000000405bc8 in NetworkReply::qt_static_metacall (_o=0x494620, _c=QMetaObject::InvokeMetaMethod, _id=0, _a=0x7fffffffd4c0)
    at moc_main.cpp:49
#13 0x00007ffff3d96683 in QMetaObject::activate (sender=0x494a70, m=0x7ffff3f2ee40, local_signal_index=0, argv=0x0)
```
```
Breakpoint 1, NetworkReply::readData (this=0x494620, data=0x54c328 "\374\001", maxSize=1024) at main.cpp:65
65              qDebug("NetworkReply.readData: %p %lli", data, maxSize);
(gdb) bt
#0  NetworkReply::readData (this=0x494620, data=0x54c328 "\374\001", maxSize=1024) at main.cpp:65
#1  0x00007ffff3cfa64d in QIODevice::read (this=0x494620, data=0x54c328 "\374\001", maxSize=1024) at io/qiodevice.cpp:858
#2  0x00007ffff3cfaaa4 in QIODevice::read (this=0x494620, maxSize=1536) at io/qiodevice.cpp:964
#3  0x00007ffff6bb5ecd in WebCore::QNetworkReplyHandler::forwardData() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#4  0x00007ffff6bb2880 in WebCore::QNetworkReplyHandlerCallQueue::flush() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#5  0x00007ffff6bb27b8 in WebCore::QNetworkReplyHandlerCallQueue::unlock() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#6  0x00007ffff6bb2919 in WebCore::QueueLocker::~QueueLocker() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#7  0x00007ffff6bb377e in WebCore::QNetworkReplyWrapper::emitMetaDataChanged() ()
   from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#8  0x00007ffff6bb351f in WebCore::QNetworkReplyWrapper::receiveSniffedMIMEType() ()
   from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#9  0x00007ffff6bb3242 in WebCore::QNetworkReplyWrapper::receiveMetaData() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#10 0x00007ffff6bb69d0 in WebCore::QNetworkReplyWrapper::qt_static_metacall(QObject*, QMetaObject::Call, int, void**) ()
   from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#11 0x00007ffff3d96683 in QMetaObject::activate (sender=0x494620, m=0x7ffff3f2d7e0, local_signal_index=0, argv=0x0)
    at kernel/qobject.cpp:3546
#12 0x00007ffff3df3cfb in QIODevice::readyRead (this=0x494620) at .moc/debug-shared/moc_qiodevice.cpp:105
#13 0x0000000000404d54 in NetworkReply::setContent (this=0x494620) at main.cpp:42
```
