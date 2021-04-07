'''
参考了https://blog.csdn.net/fei347795790/article/details/99693076?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522161776305816780262563072%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=161776305816780262563072&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_v2~rank_v29-2-99693076.nonecase&utm_term=%E7%99%BE%E7%A7%91
感觉xpath方法非常实用
'''
import urllib.request
import urllib.parse
from lxml import etree
def query(content):
    # 请求地址
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
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
    sen_list = html.xpath('//div[contains(@class,"lemma-summary") or contains(@class,"para")]//text()')
    # 过滤数据，去掉空白
    sen_list_after_filter = [item.strip('\n') for item in sen_list]
    # 将字符串列表连成字符串并返回
    return ''.join(sen_list_after_filter)

if __name__ == '__main__':
    while (True):
        content = input('查询词条：')
        result = query(content)
        print("查询结果：%s" % result)
        doc_location='D:/伴鱼/KnowledgeGraph/'+content+'.txt'
        f = open(doc_location,'w', encoding='utf-8')
        f.write(result)
        f.close()
