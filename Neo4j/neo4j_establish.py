#需要在http://localhost:7474/browser/中操作，这里仅做记录
#操作可以整体参考https://www.geek-share.com/detail/2808020859.html

#导入国家
LOAD CSV WITH HEADERS FROM 'file:///country.csv' AS line
create (:country {id:line.id,district:line.district,country_name:line.country})

#导入首都
LOAD CSV WITH HEADERS FROM 'file:///capital.csv' AS line
create (:capital {id:line.id,district:line.district,capital_name:line.capital})

#导入国家与首都对应关系
LOAD CSV WITH HEADERS FROM "file:///country_capital_relation.csv" AS line
match (from:country{id:line.country_id}),(to:capital{id:line.capital_id})
merge (from)-[r:首都]->(to)

#关系查询
MATCH (a:country)-[:首都]->(b:capital {capital_name:'北京'}) RETURN a,b

#查询库中的数据，貌似最大容量是300
MATCH (n) RETURN n (LIMIT 25) #limit可加可不加

#将库中的所有数据删除
match(n) detach delete n
