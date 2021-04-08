# Banyu_3_KnowledgeGraph

一.使用Neo4j构建各国对应首都的图数据库<br>
-------

主要参考了：<br>
https://www.cnblogs.com/ljhdo/p/5521577.html<br>
https://zhuanlan.zhihu.com/p/313553691<br>
https://zhuanlan.zhihu.com/p/88745411<br>
https://www.cnblogs.com/yibeimingyue/p/14577543.html<br>
https://www.geek-share.com/detail/2808020859.html<br>

二.使用Neo4j构建古诗词数据库<br>
-------

觉得使用表格太多，想只通过一个csv表格来实现节点以及相互关系的构建，故重新爬取古诗词、对应作者、对应朝代的关系。但是在导入完数据后，出现了只能查询古诗而不能查询作者的问题，即<br>
MATCH (a:author)-[:作者]->(b:poem {poem_name:'陋室铭'}) RETURN a,b 
可以查询，但是<br>
MATCH (a:author {author_name:'苏轼'})-[:作者]->(b:poem) RETURN a,b 
就不能查询。一下午百思不得其解，后来组长晚上用新爬取下来的csv文件进行关系建立时发现建立失败，这才发现爬取下来的作者后面带了一个“空格”，就是这个空格导致查询不匹配。去掉空格之后重新查询就一切正常了，终于把bug找到了可太舒服了。特此记录，告诉自己以后多注意空格、制表符、回车，这种小东西真是防不胜防！

参考资料：<br>
https://www.geek-share.com/detail/2808020859.html<br>
https://blog.csdn.net/likeyou1314918273/article/details/105946179<br>
https://zhuanlan.zhihu.com/p/61326763<br>

#### 1.关于Neo4j使用LOAD CSV导入失败问题：<br>
* 要千万注意csv文件一定是要以utf-8编码的，即“CSV UTF-8（逗号分隔）”格式<br>

#### 2.关于Neo4j查询时报错(no changes, no records)问题：<br>
* 首先检查语法是否有问题<br>
* 如果语法没错，那么问题就在查询的关键词上，要仔细检查查的关键词和列表中的关键词是否“完全一致”<br>
