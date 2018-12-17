#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import socket
 
import time
 
import threading
BUFSIZE=1024
 
 
class Access_to_Host(object):
         
    def handler(self,conn,addr):
        self.conn=conn
        self.addr=addr
        all_src_data,hostname,port,ssl_flag=self.get_dst_host_from_header(self.conn,self.addr)
        all_dst_data=self.get_data_from_host(hostname,port,all_src_data,ssl_flag)
 
 
        if  all_dst_data and not ssl_flag:
            #self.send_data_to_client(self.conn,all_dst_data)
            self.ssl_client_server_client(self.conn,self.conn_dst,all_dst_data)
        elif ssl_flag:
            sample_data_to_client=b"HTTP/1.0 200 Connection Established\r\n\r\n"
           # print("\nSSL_Flag-1")
            #self.send_data_to_client(self.conn,all_dst_data)
            #print("SSL_Flag-2")
            self.ssl_client_server_client(self.conn,self.conn_dst,sample_data_to_client)
            #print("\nSSL_Flag-3")
        else:
            print('pls check network. cannot get hostname:'+hostname)
        #self.conn.close()
    def ssl_client_server(self,src_conn,dst_conn):
        self.src_conn=src_conn
        self.dst_conn=dst_conn        
        while True:
            ###get data from client
            try:
                ssl_client_data=self.src_conn.recv(BUFSIZE)
            except Exception as e:
                print("client disconnct ")
                print(e)
                self.src_conn.close()
                #self.dst_conn.close()
                return False
            
            if ssl_client_data:
                #####send data to server
                try:
                    self.dst_conn.sendall(ssl_client_data)
                except Exception as e:
                    print("server disconnct Err")
                    self.dst_conn.close()
                    return False
            else:
                self.src_conn.close()
                return False
            
    def ssl_server_client(self,src_conn,dst_conn):
        self.src_conn=src_conn
        self.dst_conn=dst_conn
        
        while True:
            ###get data from server
            try:
                ssl_server_data=self.dst_conn.recv(BUFSIZE)
            except Exception as e:
                print("server disconnct ")
                self.dst_conn.close()
                return False
                            
            if ssl_server_data:
                #####send data to client
                try:
                    self.src_conn.sendall(ssl_server_data)
                except Exception as e:
                    print("Client disconnct Err")
                    self.src_conn.close()
                    return False
            else:
                self.dst_conn.close()
                return False
                                    
        
    def ssl_client_server_client(self,src_conn,dst_conn,all_dst_data):
        self.src_conn=src_conn
        self.dst_conn=dst_conn
        try:
            #print(all_dst_data)
            self.src_conn.sendall(all_dst_data)
        except Exception as e:
            print(e)
            print("cannot sent data(HTTP/1.0 200) to SSL client")
            return False
        threadlist=[]
 
 
        t1=threading.Thread(target=self.ssl_client_server,args=(self.src_conn,self.dst_conn))
        t2=threading.Thread(target=self.ssl_server_client,args=(self.src_conn,self.dst_conn))
        threadlist.append(t1)
        threadlist.append(t2)
        for t in threadlist:
            t.start()
            #t.join()
        #self.dst_conn.close()
        #self.src_conn.close()
 
 
        
    def get_src_client(self):
        self.src_ip=self.s_src.getpeername()
        return  self.src_ip
        
    def send_data_to_client(self,conn_src,data):
        self.conn_src=conn_src
        try:
            self.conn_src.sendall(data)
        except Exception as e:
            print(e)
            print("cannot sent data to client")
            return False
        #self.conn_dst.close()
            
    def get_dst_host_from_header(self,conn_sock,addr):
        
        self.s_src=conn_sock
        self.addr=addr
        header=""
        ssl_flag=False
        while True:
            #print("Loop Loop Loop")
            header=self.s_src.recv(BUFSIZE)
            if header :
                indexssl=header.split(b"\n")[0].find(b"CONNECT")
               # print("indexsll:"+str(indexssl))
                if indexssl>-1:
                    #####CONNECT===7  +8 
                    hostname=str(header.split(b"\n")[0].split(b":")[0].decode())
                    hostname=hostname[indexssl+8:]
                    port=443
                    ssl_flag=True
                    return header,hostname,port,ssl_flag
                index1=header.find(b"Host:")
                index2=header.find(b"GET http")
                index3=header.find(b"POST http")
                if index1>-1:
                    indexofn=header.find(b"\n",index1)
                    ##host:===5
                    host=header[index1+5:indexofn]
                elif index2>-1 or index3>-1:
                    ###no host sample :'GET http://saxn.sina.com.cn/mfp/view?......
                    host=header.split(b"/")[2]
                else:                        
                    print("src socket host:")
                    print(self.s_src.getpeername())
                    print("cannot find out host!!:"+repr(header))
                    return 
                break
        host=str(host.decode().strip("\r").lstrip())
        if len(host.split(":"))==2:
            port=host.split(":")[1]
            hostname=host.split(":")[0].strip("")
        else:
            port=80
            hostname=host.split(":")[0].strip("")
        ssl_flag=False
        return header,hostname,int(port),ssl_flag
 
 
    def get_data_from_host(self,host,port,sdata,ssl_flag):
        self.conn_dst=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        all_dst_data=""
        try:
            self.conn_dst.connect((str(host),port))
        except Exception as e:
            print(e)
            print("get_data_from_host: cannot get host:"+host)
            self.conn_dst.close()
            return False
        #con_string="("+server+","+port+")"
        ############https
        try:
            if ssl_flag:
                return all_dst_data
            else:
                self.conn_dst.sendall(sdata)
        except Exception as e:
            print(e)
            print("cannot send data to host:"+host)
            self.conn_dst.close()
            return False
       # buffer=[]
        rc_data=self.conn_dst.recv(BUFSIZE)
        #####data
        return rc_data
 
 
         
class Server(object):
    p2p_addr_self = ""
    p2p_port_self = -1
    #p2p_socket_self = socket()
    def get_p2p_server(self, addr, port):
        ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ss.connect((addr, port))
        ss.sendall("Server_reg")
        print("=================1=====================")
            # reg
        data = ss.recv(1024)
        if not data:
            print("no data1")
            ss.close()
            return
        print(data[:18])
        if data[:18] != "Server_reg success":
             print("reg fail")
             ss.close()
             return
            #############有客户端注册
        while True:
            data = ss.recv(1024)
            print data
            if not data:
                print("no data2")
                ss.close()
                return
            
            data_dict = {}
            if "server_dict" == data[:11]:
                data_dict = json.loads(data[12:])
            else:
                print("data error")
                ss.close()
                return
            if len(data_dict["client"]) > 1:
                break
        ss.sendall("Server_res " + json.dumps(data_dict["client"]))
        ss.close()
        del ss
        time.sleep(6)
        #######p2p认证客户端
        print("======================================")
        ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("server data: " ,tuple(data_dict["self"]))
        ss.bind(tuple(data_dict["self"]))
        for addr_client in data_dict["client"]:
            if "test" == addr_client:
                continue
            print tuple((addr_client, data_dict["client"][addr_client]))
            try: 
                ss.connect((addr_client, data_dict["client"][addr_client]))
            except Exception as e:
                print("client auth::  ", addr_client, data_dict["client"][addr_client])
        ss.listen(socket.SOMAXCONN)
        ss.setblocking(True)
        #connection, address = ss.accept() 
        self.p2p_addr_self = data_dict["self"][0]
        self.p2p_port_self = data_dict["self"][1]
        self.p2p_socket_self = ss
        print("p2p client_server OK")
 
    def p2p_handle(self):
        if not self.p2p_socket_self:
            return
        while True:
           connection, address = self.p2p_socket_self.accept()
           print(address)
           buf = connection.recv(1024)
           
           if buf and  buf[0] == "p":
               print(buf)
               break
           connection.close()
        self.s_s = self.p2p_socket_self

    def Handle_Rec(conn_socket,addr):
        print("This is Handler Fun")
        pass
    
    def __init__(self,host = "123",port = 0, mothed="test"):
        if mothed == "p2p_client_server":
            pass
            #1.连接p2p服务器
            #2.从服务器获得需要通信的客户端地址和本机地址
            #3.主动连接目标客户端(让目标客户端能够连接自己)
            #4.监听本机端口,等待客户端连接
        return
        print("Server starting......")
        self.host=host
        self.port=port
        self.s_s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s_s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.s_s.bind((host,port))
        self.s_s.listen(20)
 
 
    def start(self):
        print("Server starting......")
        while True:
            try:
                print(self.s_s)
                conn,addr=self.s_s.accept()
                print("new connect", self.s_s)
                threading.Thread(target=Access_to_Host().handler,args=(conn,addr)).start()
            except Exception  as e:
                print(str(e))
                print("\nExcept happend")
          
if  __name__=="__main__":
    svr=Server()
    svr.get_p2p_server("192.168.85.130", 2080)
    svr.p2p_handle()
    svr.start()
