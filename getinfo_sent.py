#from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from time import gmtime, strftime
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr



my_sender = 'xxxxxx@qq.com'  # 发件人邮箱账号
my_pass = 'xxxxxx'  # 发件人邮箱密码
my_user = 'xxxxxxx@qq.com'  # 收件人邮箱账号，我这边发送给自己
keyword = 'xxxx'


def get_products():
    """
    提取商品数据
    """
    base_url = "https://search.smzdm.com/?c=faxian&s="
    url = base_url + keyword
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'
    header = {'User-Agent': user_agent}
    r = requests.get(url=url, headers=header)
    r.raise_for_status()
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup.find_all("li",{"class":"feed-row-wide "}))

    data = soup.find("li", {"class": "feed-row-wide "})

    title = data.a['title']
    value = data.find("div", {"class": "z-highlight"}).string
    tag   = data.find("div", {"class": "feed-block-descripe"}).text.replace("\n", "").replace(' ', '') #去掉换行和空格
    date  = data.find("span", {"class": "feed-block-extras"}).text.replace("\n", "").replace(' ', '')
    html  = data.a['href']
    with open ('log/'+ keyword +'.txt', 'w') as file:
        file.write(title  + value +'\n' + tag +'\n'+ date +'\n'+ html)



def mkdir(path):

    # 判断路径是否存在
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print (path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path + ' 目录已存在')
        return False


def diff_file(content1, content2):
    i=1
    if content1 == content2:
       i=0
    return i

# 读取文件内容，注意，文件不能过大，内存溢出
def get_file(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    # 如果不存在此文件，创建一个空白文件
    else:
        f = open(file, 'w')
        f.close()


# 复制文件,文件1复制给文件2
def copy_file(file1, file2):
    file_content1 = get_file(file1)
    with open(file2, 'w') as f:
        f.write(file_content1)

def log(url1, url2):
    try:
        # 读取两个文件的内容,第二个文件才是增加内容的文件
        file_content1 = get_file(url1)
        file_content2 = get_file(url2)
        # 比较两个文件的差异
        diff = diff_file(file_content1, file_content2)
        # 差异发送到邮件
        if diff == 1 :
            hit_email = mail(file_content1)
            # 发邮件成功的话，要覆盖后面的文件，用于下次对比
            if hit_email == 1:
                copy_file(url1, url2)
                print('发送成功')
            elif hit_email == 0:
                print('发送失败')
        else:
            print("没有更新")
    except Exception as e:
        print('Error:', e)




def mail(diff):
    ret = 1
    try:
        msg = MIMEText(diff, 'plain', 'utf-8')
        msg['From'] = formataddr(["FromJoyce", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "发送邮件测试"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = 0
    return ret


if __name__ == '__main__':
    a = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(a)
    mkdir('log')
    get_products()
    url1 = 'log/'+keyword+'.txt'
    url2 = 'log/'+keyword+'tmp.txt'
    log(url1, url2)
    print("运行结束")


