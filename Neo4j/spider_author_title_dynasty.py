import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.parse
from lxml import etree

#先爬取每首诗对应的超链接
html = urlopen('https://so.gushiwen.cn/gushi/yongwu.aspx')  # 获取网页
bs = BeautifulSoup(html, 'html.parser')  # 解析网页
hyperlink = bs.find_all('a')  # 获取所有超链接
file = open('D:/伴鱼/KnowledgeGraph/poem/poem_url.txt', 'w')
for h in hyperlink:
    hh = h.get('href')
    if hh and '/shiwenv' in hh:  # 筛选博客链接
        #print(hh)
        file.write(hh)  # 写入到“blog.txt”文件中
        file.write('\n')
file.close()

# 接下来爬取对应超链接中的内容
# 请求地址
# 咏物诗网址
f=open('D:/伴鱼/KnowledgeGraph/poem/poem_url.txt', 'r')
for line in f:
    #print(line)
    url = 'https://so.gushiwen.cn'+line
    # 请求头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    # 发送请求，获得响应
    response = urllib.request.urlopen(req)
    # 读取响应，获得文本
    text = response.read().decode('utf-8')
    # 构造 _Element 对象
    html = etree.HTML(text)
    # 使用 xpath 匹配数据，得到匹配字符串列表，感觉还是Xpath最方便啊

    #提取诗词题目
    title=html.xpath('//h1[contains(@style,"font-size")]//text()')
    title=''.join(title) #这样会导致作者后面有空格
    #print(title)

    #提取诗词作者和朝代
    author_dynasty = html.xpath('//p[1][contains(@class,"source")]//text()')
    # 过滤数据，去掉空白
    # 将字符串列表连成字符串并返回
    author_dynasty = ''.join(author_dynasty)
    author_dynasty=author_dynasty.split()
    author_dynasty = ''.join(author_dynasty)
    author_dynasty=author_dynasty.replace('〔','\t')
    author_dynasty=author_dynasty.replace('〕','\n')

    #print(dynasty)
    f = open('D:/伴鱼/KnowledgeGraph/poem/poem.txt','a',encoding='utf-8')
    f.write(title)
    f.write('\t')
    f.write(author_dynasty)
    f.close()
