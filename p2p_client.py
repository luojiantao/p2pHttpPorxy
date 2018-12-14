#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import socket
 
import time
 
import threading
BUFSIZE=1024
 
 
class Access_to_Host(object):
    def meaasge_forward(self, conn, conn_dst):
       self.src = conn
       self.dst = conn_dst
       
       threadlist=[]
       t1=threading.Thread(target=self.ssl_client_server,args=(self.src_conn,self.dst_conn))
       t2=threading.Thread(target=self.ssl_server_client,args=(self.src_conn,self.dst_conn))
       threadlist.append(t1)
       threadlist.append(t2)
       for t in threadlist:
           t.join()
       self.src.close()
       self.dat.close() 
         
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
         
class Server(object):
    def get_p2p_server(self, addr, port):
        ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ss.connect((addr, port))
        ss.sendall("Client_reg")
        print("Client_reg")
        data = ss.recv(1024)
        if data and (data[:18] == "Client_reg success"):
            print("Client_reg success")
            print("wait p2p server online.....")
        data_dict = {}
        data = ss.recv(1024)
        
        if data and (data[:12] == "auth_success"):
            print("auth server [{0}]".format(data))
            data_dict = json.loads(data[13:])
        else:
            ss.close()
            return

        print data_dict
        #ss.bind(tuple(data_dict["self"]))
        times = 0
        while True:
            times += 1
            ss1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            ss1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            for addr_server, port_server in data_dict:
                if addr_server != "test":
                    time.sleep(3)
                    try:
                        ss1.connect((addr_server, port_server))
                        ss1.sendall("p2p OK")
                        print("connect success: "+ addr_server +":" + str(port_server))
                        print("p2p client OK!")
                        ss.sendall("Client_OK "+ json.dumps((addr_server, port_server)))
                        ss.close()
                        return 
                    except Exception as e:
                        print("connect fail: "+ addr_server +":" + str(port_server))
                        break
            ss1.close()
            if times >= 5:
                continue
                print("device not support")
                return
            
        
    def p2p_handle(self):
        pass 
         
    def Handle_Rec(conn_socket,addr):
        print("This is Handler Fun")
        pass
    
    def __init__(self,host,port, mothed="test"):
        if mothed == "p2p_client_server":
            pass
            #1.连接p2p服务器
            #2.从服务器获得需要通信的服务端地址和本机地址
            #3.主动连接目标服务端(多试几次)
            #4.连接成功准备通信
        return 
        print("Server starting......")
        self.host=host
        self.port=port
        self.s_s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s_s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.s_s.bind((host,port))
        self.s_s.listen(20)
 
 
    def start(self):
        while True:
            try:
                conn,addr=self.s_s.accept()
                threading.Thread(target=Access_to_Host().handler,args=(conn,conn_dst)).start()
            except Exception  as e:
                print(str(e))
                print("\nExcept happend")
 
 
 
 
          
if  __name__=="__main__":
    svr=Server("0.0.0.0",2082)
    svr.get_p2p_server("192.168.85.130", 2080)
    #svr.start()
