# p2pHttpPorxy
##说明：
在公司里通常有这种情况，工作机是windows能访问外网，查阅资料。 而开发环境，由于网络原因不能访问外网，下载安装包（yum install/ apt-get install）

运行着几个文件，能让你使工作机作为HTTP代理服务器，使开发环境通过HTTP代理访问外网

##原理：

使用p2p TCP打洞的原理（需要路由器硬件支持，不过一般都支持，至少我在的公司是这样的）

###使用步骤
1.在开发环境和工作机都能访问的机器上运行 p2p_seed_server.py（推荐 工作环境上运行这个脚本）
2.在工作机上运行 demo_p2p_client_server.py（需要修改代码，使它能指向 p2p_seed_server.py 的地址和端口）
3.在开发环境运行demo_client.py（配置同样和demo_p2p_client_server.py 一样），终端提示连接成功，打印出HTTP代理的地址和端口
