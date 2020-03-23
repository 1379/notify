## 介绍

notify 是一个基于Python的小说更新提示爬虫，专用与《逆天邪神》小说的更新提示，信息来源为http://nitianxieshen.com。当小说更新时该爬虫会自动发送更新提示到你指定的邮箱，提醒你阅读。

##  快速使用

1. 运行环境：
   - Linux服务器
   - Python3
   - lxml

1. 下载notify.py文件到服务器

2. 安装lxml

   ```shell
   pip3 install lxml
   ```

3. 运行notify.py: 

   ```shell
   python3 notify.py 123@qq.com 123@qq.com my_password
   ```

   第一个参数123@qq.com是发件人的邮箱地址(目前只支持QQ邮箱)

   第二个参数123@qq.com是收件人的邮箱地址

   第三个参数my_password则是发件人的QQ邮箱授权码，获取授权码需要到QQ邮箱网页版开通SMTP服务

   所以，上面命令是通过123@qq.com和授权码发送更新提示邮件给123@qq.com（此时相当于给自己发邮件）

   执行以上命令即可运行脚本，同时当前目录会生成两个文件：chapter_config用于保存上一次的最新章节编号（以便与判断最新章节）nitianxieshen.log用于记录程序运行日志

   notify.py脚本会访问http://nitianxieshen.com网址获取最新章节，并与chapter_config文件中的章节序号比较，如果大于则发送邮件提醒，并保存最新的章节序号到chapter_config文件，程序退出。

3. 配置Linux crontab定时任务

   在步骤2中，成功运行了脚本，但只是一次性的，程序运行完毕便退出了，如果想要脚本全天候监视小说更新，则需要让脚本定时执行。

   Linux用户可以执行以下命令来配置定时任务

   ```shell
   crontab -e
   ```

   执行以上命令后，会给出一个编辑器，我们需要将我们的要执行的任务写入

   ```
   */30 * * * * python3 /root/notify.py 123@qq.com 123@qq.com my_password
   ```

   此语句的含义是 每搁30分钟执行一次 /root/notify.py 这个脚本（/root/notify.py是作者的服务器上的路径，使用者需要替换成自己的路径），可以随意更改30为任何值，如更改为10，则是每10分钟执行一次脚本，检测一下小说是否更新。

   编辑完成后保存退出即可。如下图：

   ![crotab](img\crontab.png)