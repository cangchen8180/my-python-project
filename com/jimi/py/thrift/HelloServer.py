# coding=utf-8

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from helloService import HelloService


class HelloHandler:
    def __init__(self):
        pass

    def helloString(self, word):
        ret = "Received: " + word
        print ret
        return ret


while True:
    # handler processer类
    handler = HelloHandler()
    processor = HelloService.Processor(handler)
    transport = TSocket.TServerSocket("127.0.0.1", 8989)
    # 传输方式，使用buffer
    tfactory = TTransport.TBufferedTransportFactory()
    # 传输的数据类型：二进制
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    # server方式一：
    # 创建一个thrift simple服务
    # server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # server方式二：
    # 创建一个thrift 标准的阻塞式IO线程池服务模型服务，预先创建一组线程处理请求。
    threadPoolServer = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    # print "Starting thrift simple server in python..."
    print "Starting thrift thread pool server in python..."
    threadPoolServer.serve()
    # server.serve()
    print "done!"
