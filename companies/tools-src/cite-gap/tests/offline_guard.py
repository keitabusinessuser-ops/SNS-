"""外部通信を試みたら即失敗させるガード（テスト専用）。

install() で socket.socket.connect / socket.getaddrinfo / urllib.request.urlopen /
http.client の接続系をパッチする。呼ばれたら NetworkAttempt を投げる。
"""
import http.client
import socket
import urllib.request
from unittest import mock


class NetworkAttempt(AssertionError):
    pass


def _deny(name):
    def f(*a, **k):
        raise NetworkAttempt(f"外部通信の試行を検出: {name}")
    return f


def patches():
    return [
        mock.patch.object(socket.socket, "connect", _deny("socket.socket.connect")),
        mock.patch.object(socket.socket, "connect_ex", _deny("socket.socket.connect_ex")),
        mock.patch.object(socket, "getaddrinfo", _deny("socket.getaddrinfo")),
        mock.patch.object(socket, "create_connection", _deny("socket.create_connection")),
        mock.patch.object(urllib.request, "urlopen", _deny("urllib.request.urlopen")),
        mock.patch.object(http.client.HTTPConnection, "connect", _deny("http.client.HTTPConnection.connect")),
        mock.patch.object(http.client.HTTPSConnection, "connect", _deny("http.client.HTTPSConnection.connect")),
    ]
