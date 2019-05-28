#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import json 
import time
 
import threading
BUFSIZE=1024
GLOBAL_dict_authorization_info = {} 
 
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
    #json_info = json.dumps(dict1)
    #dict1 = json.loads(json_info)
    #{"0.0.0.0": 1234,} 
    dict_p2p_client = {"test":9999}
    dict_p2p_server = {"test":9999}
    #dict_p2p_server_socket = {"1.1.1.1:9999":socket} 
    dict_authorization_info = {} 
    def Handle_Rec(conn_socket,addr):
        print("This is Handler Fun")
        pass
    
    def __init__(self,host,port, mothod="test"):
    #    if mothed == "p2p_client_server"
            #1.连接p2p服务器
            #2.从服务器获得需要通信的服务端地址和本机地址
            #3.主动连接目标服务端(多试几次)
            #4.连接成功准备通信
      
        print("Server starting......")
        self.host=host
        self.port=port
        self.s_s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s_s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.s_s.bind((host,port))
        self.s_s.listen(20)


    def handler(self, conn, addr):
         while True:
             buf = conn.recv(1024)
             if not buf:
                 print("error no data!!!!!!")
                 conn.close()
                 return
             if buf[:10] == 'Server_reg':#p2p server
                 print("server {0} register!".format(str(addr)))
                 self.dict_p2p_server[addr[0]] = addr[1]
                 print("dict_p2p_server [{0}]".format(str(self.dict_p2p_server)))
                 conn.sendall("Server_reg success")
                 while True:
                     time.sleep(5)
                     print("server td client info {0}".format(str(self.dict_p2p_client)))
                     if len(self.dict_p2p_client) > 1:
                         data = {"self": addr, "client": self.dict_p2p_client}
                         conn.sendall("server_dict " + json.dumps(data))
                         break
                 #self.dict_p2p_server_socket[addr[0]] = (addr[0], addr[1], conn)

             if buf[:10] == "Server_res":
                 print buf
                 data_dict = json.loads(buf[11:])
                 #authorization
                 for client_addr in data_dict:
                     print("authorization addr:{0},port:{1}".format(client_addr, str(data_dict[client_addr])))
                     if client_addr not in self.dict_authorization_info:
                         self.dict_authorization_info[client_addr] = [] 

                     self.dict_authorization_info[client_addr].append(addr)     
                 print("del server ", self.dict_p2p_server.pop(addr[0], "null"))
                 conn.close()
                 return
             
             if buf[:10] == 'Client_reg':#p2p client
                 self.dict_p2p_client[addr[0]] = addr[1]
                 conn.sendall("Client_reg success")
                 print("dict_p2p_client [{0}]".format(str(self.dict_p2p_client))) 
                 while True:
                     time.sleep(5)
                     print("auth info {0}".format(str(self.dict_authorization_info)))
                 #self.dict_p2p_client.update(dict1)
                     if addr[0] in self.dict_authorization_info:
                         print("========server address=========")
                         print(self.dict_authorization_info[addr[0]])
                         conn.sendall("auth_success {0}".format(str(json.dumps(self.dict_authorization_info[addr[0]]))))
                         break

             if buf[:9] == "Client_OK":
                 data_tuple = json.loads(buf[10:])
                 #server_addr, server_port = data_tuple
                 print(self.dict_authorization_info)
                 self.dict_p2p_client.pop(addr[0], "null")
                 self.dict_authorization_info.pop(addr[0])
                 print("client connect OK {0} --> {1}"+ str(addr), str((data_tuple)))
                 conn.close()
                 return
                 #data = {"self": addr, "server": self.dict_p2p_server}
                 #conn.sendall("client_dict " + json.dumps(data))
                 #if self.server:
                     #self.server.sendall("server_dict " + json.dumps({"self": self.addr, "client": self.dict_p2p_client}))
                     #self.server.close()
                 #conn.close()
                 #return

 
    def start(self):
        while True:
            try:
                conn,addr=self.s_s.accept()
                t = threading.Thread(target=self.handler,args=(conn,addr))
                t.setDaemon(True)
                t.start()
            except Exception  as e:
                print(str(e))
                print("\nExcept happend")
 
 
  
if  __name__=="__main__":
    svr=Server("0.0.0.0",2080)
    svr.start()
