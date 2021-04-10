#爬取所有类型的诗的题目、作者、朝代以及诗词内容
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.parse
from lxml import etree


#先爬取每种类型的诗对应的超链接
poem_type=['tangshi','sanbai','songsan','xiaoxue','chuzhong','gaozhong','xiaowen','chuwen','gaowen',#9
           'songci','shijiu','shijing','chuci','yuefu','xiejing','yongwu','chuntian','xiatian',#18
           'qiutian','dongtian','yu','xue','feng','hua','meihua','hehua','juhua',#27
           'liushu','yueliang','shanshui','shan','shui','changjiang','huanghe','ertong','niao',#36
           'ma','tianyuan','biansai','diming','jieri','chunjie','yuanxiao','hanshi','qingming',#45
           'duanwu','qixi','zhongqiu','chongyang','huaigu','shuqing','aiguo','libie','songbie',#54
           'sixiang','sinian','aiqing','lizhi','zheli','guiyuan','daowang','xieren','laoshi',#63
           'muqin','youqing','zhanzheng','dushu','xishi','youguo','wanyue','haofang','minyao',#72
           'guanzhi'#73
           ]
base_url='https://so.gushiwen.cn/gushi/'
i=0
#前18个爬完了，要爬第19个qiutian时出现网络连接问题，故从第19个重新开始爬取
#i=18
#爬到第54个时又遇到了相同的问题，重新开始爬取
#i=53
#总共分三次爬完

while(i<len(poem_type)):
    url=base_url+poem_type[i]+'.aspx'
    html = urlopen(url)  # 获取网页
    bs = BeautifulSoup(html, 'html.parser')  # 解析网页
    hyperlink = bs.find_all('a')  # 获取所有超链接
    url_location='D:/伴鱼/KnowledgeGraph/poem/data/'+poem_type[i]+'_poem_url.txt'
    file = open(url_location, 'w')
    for h in hyperlink:
        hh = h.get('href')
        if hh and '/shiwenv' in hh:  # 筛选博客链接
            #print(hh)
            #有些网址爬下来前面会有https://so.gushiwen.cn，故需要去除
            if 'https://so.gushiwen.cn' in hh:
                hh=hh.replace('https://so.gushiwen.cn','')
            file.write(hh)  # 写入到文件中
            file.write('\n')
    file.close()

    # 接下来爬取对应超链接中的内容
    # 请求地址
    # 每种类型的诗网址
    f=open(url_location, 'r')
    for line in f:
        #print(line)
        url = 'https://so.gushiwen.cn'+line
        # 请求头部
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        # 利用请求地址和请求头部构造请求对象
        req = urllib.request.Request(url=url, headers=headers, method='GET')
        # 发送请求，获得响应,并设置响应延时
        response = urllib.request.urlopen(req,timeout=5)
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

        #提取诗词内容
        #遇到使用div[1]无法准确提取时，可以使用full xpath的方法
        content = html.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[2][@class="contson"]//text()')
        #print(content)
        content = ''.join(content)
        content = content.split()
        content = ''.join(content)
        #print(content_after_filter)

        #print(dynasty)
        poem_location='D:/伴鱼/KnowledgeGraph/poem/data/'+poem_type[i]+'_poem.txt'
        f = open(poem_location,'a',encoding='utf-8')
        f.write(title)
        f.write('\t')
        f.write(author_dynasty)
        f.write(content)
        f.write('\n')
        f.write('\n')
        f.close()

    print('第{}种类型：{}爬取成功'.format(i+1,poem_type[i]))
    i+=1 #计数已爬取的古诗词类型
