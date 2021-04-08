#需要在http://localhost:7474/browser/中操作，这里仅做记录
#导入作者，并合并重复的
LOAD CSV WITH HEADERS FROM 'file:///poem_author_title_dynasty.csv' AS line
merge (:author {author_name:line.作者})

#导入诗词题目，并合并重复的
LOAD CSV WITH HEADERS FROM 'file:///poem_author_title_dynasty.csv' AS line
merge (:poem {poem_name:line.诗词})

#导入作者（诗词）的朝代，并合并重复的
LOAD CSV WITH HEADERS FROM 'file:///poem_author_title_dynasty.csv' AS line
merge (:dynasty {dynasty_name:line.朝代})

#导入作者与诗词对应关系
LOAD CSV WITH HEADERS FROM "file:///poem_author_title_dynasty.csv" AS line
match (from:author{author_name:line.作者}),(to:poem{poem_name:line.诗词})
merge (from)-[r:作者]->(to)

#导入作者与朝代对应关系
LOAD CSV WITH HEADERS FROM "file:///poem_author_title_dynasty.csv" AS line
match (from:author{author_name:line.作者}),(to:dynasty{dynasty_name:line.朝代})
merge (from)-[r:朝代]->(to)

'''
导入作者与朝代对应关系方法二
通过这种方法可以检测出意想不到的问题，比如说作者名字后面有空格
LOAD CSV WITH HEADERS FROM "file:///poem_author_title_dynasty.csv" AS line
match (from:author{author_name:line.作者}),(to:dynasty{dynasty_name:line.朝代}) 
merge (from)-[r:朝代{author_name:line.作者,dynasty:line.朝代}]->(to)
'''

#创建新的节点
create (:label{name:'咏物'})

#把所有作者指向 咏物 节点
match (from:author),(to:label)
merge (from)-[r:属性]->(to)

#把所有诗词指向 咏物 节点
#注意这里的关系和上面的不能一样，不然会无法生成
match (from:poem),(to:label)
merge (from)-[r:题材]->(to)

#关系查询
MATCH (a:author)-[:作者]->(b:poem {poem_name:'陋室铭'}) RETURN a,b
#这边单向箭头可以去掉
MATCH (a:author)-[:作者]-(b:poem {poem_name:'陋室铭'}) RETURN a,b
MATCH (a:author {author_name:'苏轼'})-[:作者]->(b:poem) RETURN a,b
#甚至还可以反向写
MATCH (b:poem)<-[:作者]-(a:author {author_name:'苏轼'}) RETURN a,b
MATCH (a:author {author_name:'苏轼'})-[:朝代]->(b:dynasty) RETURN a,b
MATCH (a:author)-[:朝代]->(b:dynasty {dynasty_name:'清代'}) RETURN a,b


#查询库中的数据，貌似最大容量是300
MATCH (n) RETURN n (LIMIT 25) #limit可加可不加

#将库中的所有数据删除
match(n) detach delete n

#前面没用merge的话要将相同的作者节点合并，但是会导致标签丢失，所以还是直接用merge比较好
#其中需要用到apoc.refactor.mergeNodes，安装和使用参考
#https://blog.csdn.net/likeyou1314918273/article/details/105946179
#https://zhuanlan.zhihu.com/p/61326763
MATCH (n:author)
with n.name as name,collect(n) as nodelist,count(n) as nodecount
where nodecount > 1
call apoc.refactor.mergeNodes(nodelist) YIELD node
RETURN count(node)

#将相同的朝代节点合并，好像会导致节点的标签值丢失
MATCH (n:dynasty)
with n.name as name,collect(n) as nodelist,count(n) as nodecount
where nodecount > 1
call apoc.refactor.mergeNodes(nodelist) YIELD node
RETURN count(node)
