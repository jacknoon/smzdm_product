# smzdm_product
获取什么值得买搜索页面信息
zdm_product.py是爬去需要搜索的关键次写入到mongo中。可定义关键词和爬去页数。

getinfo_sent.py是写的一个监控什么值得买发现页面，有无最新爆料，如果有就发送最新爆料的信息邮件到邮箱里。需要配合定时任务crontab实现监控。里面添加发送邮箱和收件邮箱，关键词等几个。下面是我的定时任务写法。python需要绝对路径。
*/30 * * * * /home/gg/anaconda3/bin/python /home/gg/Desktop/定时/getinfo_sent.py >> /home/gg/Desktop/定时/time.log 
