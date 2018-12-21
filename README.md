# p2pHttpPorxy
## 说明：
在公司里通常有这种情况，工作机是windows能访问外网，查阅资料。 而开发环境，由于网络原因不能访问外网，下载安装包（yum install/ apt-get install）

运行着几个文件，能让你使工作机作为HTTP代理服务器，使开发环境通过HTTP代理访问外网

网络环境如下

![图片有问题，待更新](https://github.com/luojiantao/p2pHttpPorxy/blob/master/image/2.png) 

## 原理：

使用p2p TCP打洞的原理（需要路由器硬件支持，不过一般都支持，至少我在的公司是这样的），如果路由环境是会记录端口的话，就需要自己实现代理客户端。目前暂时不支持这种环境

```sequence
   
   Client->>SeedServer:register
   Server->>SeedServer:register
   SeedServer-->Server:ser_IP,ser_port,cli_IP,cli_port
   SeedServer-->Client:ser_IP,ser_port
   Server->>Client:connect(会提示连接失败)
   Client->>Server:connect,连接成功，证明p2p打洞完成。提示HTTP代理服务地址和端口
```
![ddjdjdjj](https://github.com/luojiantao/p2pHttpPorxy/blob/master/image/1.png) 
### 使用步骤

1. 三个文件中初始化的地址都为，seed_server的地址和端口（按照自己喜好设置）
2. 在seed机器上运行seed_server.py
3. 在server上运行client_server.py
4. 在client上运行client.py，最终会在终端提示连接成功，并答应http代理服务的地址和端口

