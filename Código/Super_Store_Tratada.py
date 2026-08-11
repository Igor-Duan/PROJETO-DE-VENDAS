import pandas as pd


store= pd.read_csv("../Data/samplesuperstore.csv")

#ANALIZANDO MEUS DADOS  



print(store.isna().sum())

print(store.info())

print(store[store.duplicated()])

#NENHUM COM NOT A NUMBER, OU A MAIS.

#REVISAR / TRANSFORMAR MEUS DADOS


print(store["Discount"])
print(store[["Sales", "Quantity"]])

store["Total Revenue"]  = store["Quantity"] *store["Sales"] 

store["Total Liquid"] = store["Sales"] * ( 1 -  store["Discount"])

store["Order Year"] = pd.to_datetime(store["Order Date"]).dt.year

store["Order Month"] = pd.to_datetime(store["Order Date"]).dt.month

print(store["Total Revenue"])

print(store["Total Liquid"])

print(store["Total Revenue"] - store["Total Liquid"])



print(store.groupby(by="Customer Name")["Total Liquid"].sum().sort_values(ascending=False).head(5))





store["Customer Name"].count()


df_num = store.select_dtypes(include="number")

print((df_num < 0).sum().sum())

print(df_num[(df_num < 0).any(axis=1)])

print((df_num.select_dtypes(include="number") < 0).sum())


store.columns = (
    store.columns
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)


# AGORA CARREGAR PARA O SQL

import sqlite3

conexao = sqlite3.connect("superstore.db")

#CRIAR MINHAS QUERYS

querycliente = """SELECT customer_name, sum (total_liquid ) as total FROM vendas 

 GROUP BY customer_name

Order by  sum (total_liquid ) desc
LIMIT 5;"""


queryrenda = """SELECT  

sum(Profit) as Lucro_Liquido,

sum(CASE WHEN Profit > 0 THEN Profit ELSE 0 END) as Lucro,

sum(CASE WHEN Profit < 0 THEN Profit ELSE 0 END) as prejuizo,

count(*) as Total_Vendas

FROM vendas"""

querytop_product  = """SELECT sub_category , sum(Total_Liquid) as total   FROM vendas 
GROUP BY sub_category 
ORDER BY total_liquid desc
LIMIT 10;
"""

query_prejudice = """ 
SELECT sub_category , sum(profit < 0)  as prejuízo FROM vendas 
GROUP BY sub_category
ORDER BY sum(profit < 0) desc
LIMIT 5;
"""

querymonth = """SELECT order_month  , count(*) as quant_sales  FROM vendas
GROUP BY order_month ;
"""




df_top5_cl = pd.read_sql_query(querycliente, conexao)

rendatot = pd.read_sql_query(queryrenda, conexao)

top5_prod = pd.read_sql_query(querytop_product, conexao)

query_prejudice = pd.read_sql_query(query_prejudice, conexao)

quant_per_month = pd.read_sql_query(querymonth, conexao )



print("-"*30)

print(df_top5_cl)

print("-"*30)
print(rendatot)
print("-"*30)
print(top5_prod)
print("-"*30)
print(query_prejudice)
print("-"*30)
print(quant_per_month)



#Mandando para o excel:
	
with pd.ExcelWriter("Dashboarde.xlsx") as writer:
	

    df_top5_cl.to_excel(writer,sheet_name="Top5_Buyers", index=False)

    rendatot.to_excel(writer, sheet_name="Revenues", index=False)    
	






#salvando em sql e csv os dados limpos:


store.to_sql("vendas", conexao, if_exists="replace", index=False)

#---------------------------------------


store.to_csv("../limpo/Store.csv", index=False)

