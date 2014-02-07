Test case for https://bugreports.qt-project.org/browse/QTBUG-27469

The test case works for revision 9d6c186f418ea77f202404408aa6692805038bea,
but revison 6d09a6ff6653aba1f36d66739f584d0795870eaa does not.

To check out a specific revision, use:
```
git clone git://gitorious.org/qt/qt.git
git checkout <revison>
```

---

The following stack traces are for the calls of NetworkReply::readData() in main.cpp:

--

Stack trace for the good version (9d6c18..). readData is called once.

First call:
```
Breakpoint 1, NetworkReply::readData (this=0x48b110, data=0x533908 "\340\070S", maxSize=2048) at main.cpp:65
65              qDebug("NetworkReply.readData: %p %lli", data, maxSize);
(gdb) bt
#0  NetworkReply::readData (this=0x48b110, data=0x533908 "\340\070S", maxSize=2048) at main.cpp:65
#1  0x00007ffff542164d in QIODevice::read (this=0x48b110, data=0x533908 "\340\070S", maxSize=2048) at io/qiodevice.cpp:858
#2  0x00007ffff5421aa4 in QIODevice::read (this=0x48b110, maxSize=2048) at io/qiodevice.cpp:964
#3  0x00007ffff71a3de3 in WebCore::QNetworkReplyHandler::forwardData() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#4  0x00007ffff71a4a6f in WebCore::QNetworkReplyHandler::qt_static_metacall(QObject*, QMetaObject::Call, int, void**) ()
   from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#5  0x00007ffff54bd683 in QMetaObject::activate (sender=0x48b110, m=0x7ffff56547e0, local_signal_index=0, argv=0x0)
    at kernel/qobject.cpp:3546
#6  0x00007ffff551acfb in QIODevice::readyRead (this=0x48b110) at .moc/debug-shared/moc_qiodevice.cpp:105
#7  0x0000000000404bb4 in NetworkReply::setContent (this=0x48b110) at main.cpp:42
#8  0x0000000000405a28 in NetworkReply::qt_static_metacall (_o=0x48b110, _c=QMetaObject::InvokeMetaMethod, _id=0, _a=0x7fffffffd4c0)
    at moc_main.cpp:49
#9  0x00007ffff54bd683 in QMetaObject::activate (sender=0x487f80, m=0x7ffff5655e40, local_signal_index=0, argv=0x0)
    at kernel/qobject.cpp:3546
#10 0x00007ffff551db93 in QTimer::timeout (this=0x487f80) at .moc/debug-shared/moc_qtimer.cpp:148
#11 0x00007ffff54c696f in QTimer::timerEvent (this=0x487f80, e=0x7fffffffddf0) at kernel/qtimer.cpp:280
#12 0x00007ffff54b804a in QObject::event (this=0x487f80, e=0x7fffffffddf0) at kernel/qobject.cpp:1156
#13 0x00007ffff58d2edc in QApplicationPrivate::notify_helper (this=0x40a230, receiver=0x487f80, e=0x7fffffffddf0)
    at kernel/qapplication.cpp:4495
#14 0x00007ffff58d03d8 in QApplication::notify (this=0x7fffffffe2a0, receiver=0x487f80, e=0x7fffffffddf0)
    at kernel/qapplication.cpp:3877
#15 0x00007ffff549ef8e in QCoreApplication::notifyInternal (this=0x7fffffffe2a0, receiver=0x487f80, event=0x7fffffffddf0)
    at kernel/qcoreapplication.cpp:853
#16 0x00007ffff71be9a5 in QCoreApplication::sendEvent(QObject*, QEvent*) () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#17 0x00007ffff54dc8c9 in QTimerInfoList::activateTimers (this=0x40bf08) at kernel/qeventdispatcher_unix.cpp:611
#18 0x00007ffff54dd773 in QEventDispatcherUNIX::activateTimers (this=0x40b680) at kernel/qeventdispatcher_unix.cpp:868
#19 0x00007ffff54ddada in QEventDispatcherUNIX::processEvents (this=0x40b680, flags=...) at kernel/qeventdispatcher_unix.cpp:930
#20 0x00007ffff59ae458 in QEventDispatcherX11::processEvents (this=0x40b680, flags=...) at kernel/qeventdispatcher_x11.cpp:152
#21 0x00007ffff549c79c in QEventLoop::processEvents (this=0x7fffffffe210, flags=...) at kernel/qeventloop.cpp:149
#22 0x00007ffff549c930 in QEventLoop::exec (this=0x7fffffffe210, flags=...) at kernel/qeventloop.cpp:204
#23 0x00007ffff549f624 in QCoreApplication::exec () at kernel/qcoreapplication.cpp:1125
#24 0x00007ffff58cffc2 in QApplication::exec () at kernel/qapplication.cpp:3756
#25 0x00000000004053a3 in main (argc=1, argv=0x7fffffffe3c8) at main.cpp:143
```

--

Stack traces for the bad version (6d09a6..). readData is called twice.

First call:
```
Breakpoint 1, NetworkReply::readData (this=0x4b33b0, data=0x4a0628 "\240\257q", maxSize=512) at main.cpp:65
65              qDebug("NetworkReply.readData: %p %lli", data, maxSize);
(gdb) bt
#0  NetworkReply::readData (this=0x4b33b0, data=0x4a0628 "\240\257q", maxSize=512) at main.cpp:65
#1  0x00007ffff3cfa64d in QIODevice::read (this=0x4b33b0, data=0x4a0628 "\240\257q", maxSize=512) at io/qiodevice.cpp:858
#2  0x00007ffff3cfaaa4 in QIODevice::read (this=0x4b33b0, maxSize=512) at io/qiodevice.cpp:964
#3  0x00007ffff3cfbafd in QIODevicePrivate::peek (this=0x4b34c0, maxSize=512) at io/qiodevice.cpp:1467
#4  0x00007ffff3cfbc5b in QIODevice::peek (this=0x4b33b0, maxSize=512) at io/qiodevice.cpp:1533
#5  0x00007ffff6e88e3c in QtMIMETypeSniffer::sniff() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#6  0x00007ffff6e88c79 in QtMIMETypeSniffer::QtMIMETypeSniffer(QNetworkReply*, QString const&, bool) ()
   from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#7  0x00007ffff6bb31df in WebCore::QNetworkReplyWrapper::receiveMetaData() () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#8  0x00007ffff6bb69d0 in WebCore::QNetworkReplyWrapper::qt_static_metacall(QObject*, QMetaObject::Call, int, void**) ()
   from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#9  0x00007ffff3d96683 in QMetaObject::activate (sender=0x4b33b0, m=0x7ffff3f2d7e0, local_signal_index=0, argv=0x0)
    at kernel/qobject.cpp:3546
#10 0x00007ffff3df3cfb in QIODevice::readyRead (this=0x4b33b0) at .moc/debug-shared/moc_qiodevice.cpp:105
#11 0x0000000000404d54 in NetworkReply::setContent (this=0x4b33b0) at main.cpp:42
#12 0x0000000000405bc8 in NetworkReply::qt_static_metacall (_o=0x4b33b0, _c=QMetaObject::InvokeMetaMethod, _id=0, _a=0x7fffffffd4c0)
    at moc_main.cpp:49
#13 0x00007ffff3d96683 in QMetaObject::activate (sender=0x48a2e0, m=0x7ffff3f2ee40, local_signal_index=0, argv=0x0)
    at kernel/qobject.cpp:3546
#14 0x00007ffff3df6b93 in QTimer::timeout (this=0x48a2e0) at .moc/debug-shared/moc_qtimer.cpp:148
#15 0x00007ffff3d9f96f in QTimer::timerEvent (this=0x48a2e0, e=0x7fffffffddf0) at kernel/qtimer.cpp:280
#16 0x00007ffff3d9104a in QObject::event (this=0x48a2e0, e=0x7fffffffddf0) at kernel/qobject.cpp:1156
#17 0x00007ffff41abedc in QApplicationPrivate::notify_helper (this=0x40a2f0, receiver=0x48a2e0, e=0x7fffffffddf0)
    at kernel/qapplication.cpp:4495
#18 0x00007ffff41a93d8 in QApplication::notify (this=0x7fffffffe2a0, receiver=0x48a2e0, e=0x7fffffffddf0)
    at kernel/qapplication.cpp:3877
#19 0x00007ffff3d77f8e in QCoreApplication::notifyInternal (this=0x7fffffffe2a0, receiver=0x48a2e0, event=0x7fffffffddf0)
    at kernel/qcoreapplication.cpp:853
#20 0x00007ffff6476a53 in QCoreApplication::sendEvent(QObject*, QEvent*) () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#21 0x00007ffff3db58c9 in QTimerInfoList::activateTimers (this=0x40bf78) at kernel/qeventdispatcher_unix.cpp:611
#22 0x00007ffff3db6773 in QEventDispatcherUNIX::activateTimers (this=0x40b6f0) at kernel/qeventdispatcher_unix.cpp:868
#23 0x00007ffff3db6ada in QEventDispatcherUNIX::processEvents (this=0x40b6f0, flags=...) at kernel/qeventdispatcher_unix.cpp:930
#24 0x00007ffff4287458 in QEventDispatcherX11::processEvents (this=0x40b6f0, flags=...) at kernel/qeventdispatcher_x11.cpp:152
#25 0x00007ffff3d7579c in QEventLoop::processEvents (this=0x7fffffffe210, flags=...) at kernel/qeventloop.cpp:149
#26 0x00007ffff3d75930 in QEventLoop::exec (this=0x7fffffffe210, flags=...) at kernel/qeventloop.cpp:204
#27 0x00007ffff3d78624 in QCoreApplication::exec () at kernel/qcoreapplication.cpp:1125
#28 0x00007ffff41a8fc2 in QApplication::exec () at kernel/qapplication.cpp:3756
#29 0x0000000000405543 in main (argc=1, argv=0x7fffffffe3c8) at main.cpp:143
```

Second call:
```
Breakpoint 1, NetworkReply::readData (this=0x4b33b0, data=0x560298 "\221", maxSize=1024) at main.cpp:65
65              qDebug("NetworkReply.readData: %p %lli", data, maxSize);
(gdb) bt
#0  NetworkReply::readData (this=0x4b33b0, data=0x560298 "\221", maxSize=1024) at main.cpp:65
#1  0x00007ffff3cfa64d in QIODevice::read (this=0x4b33b0, data=0x560298 "\221", maxSize=1024) at io/qiodevice.cpp:858
#2  0x00007ffff3cfaaa4 in QIODevice::read (this=0x4b33b0, maxSize=1536) at io/qiodevice.cpp:964
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
#11 0x00007ffff3d96683 in QMetaObject::activate (sender=0x4b33b0, m=0x7ffff3f2d7e0, local_signal_index=0, argv=0x0)
    at kernel/qobject.cpp:3546
#12 0x00007ffff3df3cfb in QIODevice::readyRead (this=0x4b33b0) at .moc/debug-shared/moc_qiodevice.cpp:105
#13 0x0000000000404d54 in NetworkReply::setContent (this=0x4b33b0) at main.cpp:42
#14 0x0000000000405bc8 in NetworkReply::qt_static_metacall (_o=0x4b33b0, _c=QMetaObject::InvokeMetaMethod, _id=0, _a=0x7fffffffd4c0)
    at moc_main.cpp:49
#15 0x00007ffff3d96683 in QMetaObject::activate (sender=0x48a2e0, m=0x7ffff3f2ee40, local_signal_index=0, argv=0x0)
    at kernel/qobject.cpp:3546
#16 0x00007ffff3df6b93 in QTimer::timeout (this=0x48a2e0) at .moc/debug-shared/moc_qtimer.cpp:148
#17 0x00007ffff3d9f96f in QTimer::timerEvent (this=0x48a2e0, e=0x7fffffffddf0) at kernel/qtimer.cpp:280
#18 0x00007ffff3d9104a in QObject::event (this=0x48a2e0, e=0x7fffffffddf0) at kernel/qobject.cpp:1156
#19 0x00007ffff41abedc in QApplicationPrivate::notify_helper (this=0x40a2f0, receiver=0x48a2e0, e=0x7fffffffddf0)
    at kernel/qapplication.cpp:4495
#20 0x00007ffff41a93d8 in QApplication::notify (this=0x7fffffffe2a0, receiver=0x48a2e0, e=0x7fffffffddf0)
    at kernel/qapplication.cpp:3877
#21 0x00007ffff3d77f8e in QCoreApplication::notifyInternal (this=0x7fffffffe2a0, receiver=0x48a2e0, event=0x7fffffffddf0)
    at kernel/qcoreapplication.cpp:853
#22 0x00007ffff6476a53 in QCoreApplication::sendEvent(QObject*, QEvent*) () from /usr/local/Trolltech/Qt-4.8.0/lib/libQtWebKit.so.4
#23 0x00007ffff3db58c9 in QTimerInfoList::activateTimers (this=0x40bf78) at kernel/qeventdispatcher_unix.cpp:611
#24 0x00007ffff3db6773 in QEventDispatcherUNIX::activateTimers (this=0x40b6f0) at kernel/qeventdispatcher_unix.cpp:868
#25 0x00007ffff3db6ada in QEventDispatcherUNIX::processEvents (this=0x40b6f0, flags=...) at kernel/qeventdispatcher_unix.cpp:930
#26 0x00007ffff4287458 in QEventDispatcherX11::processEvents (this=0x40b6f0, flags=...) at kernel/qeventdispatcher_x11.cpp:152
#27 0x00007ffff3d7579c in QEventLoop::processEvents (this=0x7fffffffe210, flags=...) at kernel/qeventloop.cpp:149
#28 0x00007ffff3d75930 in QEventLoop::exec (this=0x7fffffffe210, flags=...) at kernel/qeventloop.cpp:204
#29 0x00007ffff3d78624 in QCoreApplication::exec () at kernel/qcoreapplication.cpp:1125
#30 0x00007ffff41a8fc2 in QApplication::exec () at kernel/qapplication.cpp:3756
#31 0x0000000000405543 in main (argc=1, argv=0x7fffffffe3c8) at main.cpp:143
```
