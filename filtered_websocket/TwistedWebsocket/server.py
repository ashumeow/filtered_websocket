from __future__ import absolute_import

import uuid
import re
import hashlib
import base64
from twisted.internet.protocol import Protocol as BaseProtocol
from .exception import FrameError, ProtocolError
from .frame import Frame


handshake = '\
HTTP/1.1 101 Web Socket Protocol Handshake\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Accept: %s\r\n\r\n\
'


#
# Server protocol
#

class Protocol(BaseProtocol, object):

    def __init__(self, users=None):
        if users is None:
            users = {}
        self.bufferIn = b""
        self.bufferOut = b""
        self.users = users
        self.id = uuid.uuid4()
        self.users[self.id] = self
        self.websocket_ready = False

    def buildHandcheck(self):
        buf = self.bufferIn
        pos_check = re.compile(b"\r\n\r\n")
        pos = pos_check.search(buf).span()[0]
        if pos == -1:
            raise ProtocolError("Incomplete Handshake")
        self.onHandshake(buf)
        cmd = buf[:pos+5]
        self.bufferIn = buf[pos+4:]
        key_check = re.compile(b"Sec-WebSocket-Key:\s*(\S+)\s*")
        key = key_check.search(cmd)
        if not key:
            raise Exception("Missing Key")
        key = key.group(1)
        self.key = key
        key = str(key) + u"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        key = base64.b64encode(hashlib.sha1(key.encode("utf-8")).digest())
        return handshake % key.decode("utf-8")

    def sendHandcheck(self):
        try:
            hc = self.buildHandcheck()
        except ProtocolError:
            pass
        except Exception as e:
            print(e)
            self.transport.abortConnection()
        else:
            _write = b"".join([chr(ord(c)) for c in hc])
            self.transport.write(_write)
            self.websocket_ready = True

    def dataReceived(self, data):
        self.bufferIn += data
        if not self.websocket_ready:
            self.sendHandcheck()
            self.onConnect()
        else:
            try:
                frame = Frame(self.bufferIn)
            except FrameError:
                pass
            else:
                f_len = frame.length()
                self.bufferIn = self.bufferIn[f_len:]
                self.onMessage(frame.message())

    def connectionLost(self, *args, **kwargs):
        if self.id in self.users:
            del self.users[self.id]
        self.onDisconnect()

    def loseConnection(self):
        if self.id in self.users:
            del self.users[self.id]
        self.onDisconnect()
        self.transport.loseConnection()

    def abortConnection(self):
        if self.id in self.users:
            del self.users[self.id]
        self.onDisconnect()
        self.transport.abortConnection()

    def sendMessage(self, msg):
        self.bufferOut += Frame.buildMessage(msg, mask=False)
        if not self.websocket_ready:
            return
        _write = b"".join([chr(ord(c)) for c in self.bufferOut])
        self.transport.write(_write)
        self.bufferOut = b""

    def onHandshake(self, header):
        pass

    def onConnect(self):
        pass

    def onDisconnect(self):
        pass

    def onMessage(self, msg):
        pass
