#导入作者
LOAD CSV WITH HEADERS FROM 'file:///author.csv' AS line
create (:author {id:line.id,name:line.作者})

#导入诗词题目
LOAD CSV WITH HEADERS FROM 'file:///title.csv' AS line
create (:poem {id:line.id,name:line.诗词})

#导入作者与诗词对应关系
LOAD CSV WITH HEADERS FROM "file:///author_title_relation.csv" AS line
match (from:author{id:作者id}),(to:title{id:诗词id})
merge (from)-[r:作者]->(to)

#创建新的节点
create (:tag{name:'咏物'})

#把所有作者指向 咏物 节点
match (from:author),(to:tag)
merge (from)-[r:属于]->(to)

#把所有诗词指向 咏物 节点
#注意这里的关系和上面的不能一样，不然会无法生成
match (from:poem),(to:tag)
merge (from)-[r:题材是]->(to)

#将相同的作者节点合并
#其中需要用到apoc.refactor.mergeNodes，安装和使用参考
#https://blog.csdn.net/likeyou1314918273/article/details/105946179
#https://zhuanlan.zhihu.com/p/61326763
MATCH (n:author)
with n.name as name,collect(n) as nodelist,count(n) as nodecount
where nodecount > 1
call apoc.refactor.mergeNodes(nodelist) YIELD node
RETURN count(node)

#关系查询
MATCH (a:author)-[:作者]->(b:poem {name:'草'}) RETURN a,b
MATCH (a:author {name:'苏轼'})-[:作者]->(b:poem ) RETURN a,b


#查询库中的数据，貌似最大容量是300
MATCH (n) RETURN n (LIMIT 25) #limit可加可不加

#将库中的所有数据删除
match(n) detach delete n
