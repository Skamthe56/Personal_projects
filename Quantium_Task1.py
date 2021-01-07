#!/usr/bin/env python
# coding: utf-8

# In[136]:


import pandas as pd 
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import calendar
import matplotlib as mlp
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:





# In[2]:


transaction_data = pd.read_csv("QVI_transaction_data_1.csv")
monthly_sales = pd.read_csv('monthly_sales.csv',index_col="DATE")
transaction_data.info()
monthly_sales.info()


# In[3]:


transaction_data["DATE"] = pd.to_datetime(transaction_data["DATE"])
transaction_data.info()

plt.figure(figsize=(30,10))

# Add title
plt.title("Monthly sales")

# Bar chart showing average arrival delay for Spirit Airlines flights by month
sb.barplot(x=transaction_data['DATE'], y=transaction_data['TOT_SALES'])

# Add label for vertical axis
plt.ylabel("TOTAL SALES")


# In[7]:


transaction_data["DATE"] = pd.to_datetime(transaction_data["DATE"])


# In[ ]:





# In[6]:


transaction_data.head()


# In[8]:


transaction_data.max()


# In[9]:


#finding highest sales value and store
transaction_data.max()["TOT_SALES"]


# In[10]:


#finding any missing value in dataframe
transaction_data.isna().sum()


# In[11]:


monthly=transaction_data.groupby(transaction_data['DATE'].dt.strftime('%B'))['TOT_SALES'].sum().sort_values()
print(monthly)


# In[12]:


vi=monthly.index
type(vi)
monthly_reset=monthly.reset_index()
print (monthly_reset)


# In[13]:


monthly_reset.info()


# In[14]:


monthly_reset.sort_values(by="TOT_SALES")


# In[15]:


monthly_reset['DATE'] = pd.to_datetime(monthly_reset['DATE'], format='%B').dt.month_name().str.slice(stop=3)
print(monthly_reset)


# In[16]:


monthly_reset.info()


# In[17]:


monthly_reset.describe()


# In[ ]:





# In[18]:


# plt.figure(figsize=(20,5))

# # Add title
# plt.title("Monthly sales new")

# # Linechart showing total sales by months for 2018 and 2019 data
# sb.lineplot(x=monthly_reset["DATE"], y= monthly_reset['TOT_SALES'],data=monthly_reset)


# # Monthly sales trend

# In[322]:


plt.figure(figsize=(20,5))

# Add title
plt.title("Monthly sales")

# Linechart showing total sales by months for 2018 and 2019 data
sb.lineplot(data= monthly_sales['TOT_SALES'],label="TOTAL SALES")
plt.savefig('Monthly_sales_trend.jpg')


# In[275]:


## Above graph shows December and Jan had high sales value but a considerable drop in sales in Feb and again pickup in sales value in March
## Overall sales value seems to be arround 160000 value throughout the year.


# In[20]:


plt.figure(figsize=(20,5))

# Add title
plt.title("Monthly sales")

# Linechart showing total sales by months for 2018 and 2019 data
sb.barplot(x= monthly_sales.index,y=monthly_sales['TOT_SALES'] ,label="TOTAL SALES")


# In[ ]:





# In[ ]:





# In[21]:


#grouping data store number wise to get total sales per store
transaction_data.groupby(transaction_data['STORE_NBR'])['TOT_SALES'].sum()


# In[22]:


df=transaction_data.groupby(['STORE_NBR']).TOT_SALES.agg([sum])
print (df)


#store_data = pd.DataFrame(transaction_data.groupby(transaction_data['STORE_NBR'])['TOT_SALES'].sum())
#print (store_data)

#store_data = transaction_data.groupby(transaction_data['STORE_NBR'])['TOT_SALES'].sum()
#print(store_data)

#store_data.info()


# In[23]:


mi = df.index
type(mi)


# In[24]:


df1=df.reset_index()
print(df1)

sorted_TOT_sales=df1.sort_values(by='sum')
print(sorted_TOT_sales)


# In[25]:


df.describe()


# In[ ]:





# In[26]:


bottom10_stores=sorted_TOT_sales.head(10)
print (bottom10_stores)


# In[27]:


top10_stores=sorted_TOT_sales.tail(10)
print(top10_stores)


# In[315]:


df.max()


# In[314]:


df.min()


# In[312]:





# In[313]:



plt.figure(figsize=(50,10))

# Add title
plt.title("Monthly sales store wise")

# barchart showing total sales for each store
sb.barplot(x= df1.index,y=df1['sum'] ,label="TOTAL SALES per store")
plt.xlabel=("store number")
plt.xticks(rotation=90)
plt.savefig('Storewise_sales.jpg')


# In[31]:


df1.info()  


# In[32]:


customer= pd.read_csv("QVI_purchase_behaviour.csv")
customer.head(10)


# In[33]:


customer.info()


# In[34]:


pr_customer=customer.groupby(['PREMIUM_CUSTOMER']).LIFESTAGE.agg([len])
print (pr_customer)


# In[35]:


#premium customer count details based on life stage
pr_customer=customer.groupby(['PREMIUM_CUSTOMER','LIFESTAGE']).LIFESTAGE.agg([len])
print (pr_customer)


# In[36]:


ci= pr_customer.index
type(ci)
pr_customer.reset_index()


# In[317]:


group_data=pr_customer.reset_index()
print(group_data)
group_data.to_csv('Premium_customer_wise.csv')


# # Customer membership count based on lifestage

# In[318]:


plt.figure(figsize=(20, 7))
plt.title("Customer membership count based on lifestage")
sb.barplot(x=group_data.LIFESTAGE, y=group_data.len,hue=group_data.PREMIUM_CUSTOMER)
plt.savefig('Lifestage_wise_sales.jpg')


# In[ ]:





# # Merging Customer data and transaction data based on LYLTY_CARD_NBR column

# In[45]:


merge_all = pd.merge(transaction_data,customer)
merge_all.head()


# In[ ]:





# # Spliting product description into product name and weight in gms colum

# In[181]:


result = merge_all['PROD_NAME'].str.split('(\d+)', expand=True)
#result = result.loc[:,[1,2]]
#result.rename(columns={1:'PROD_NAME1', 2:'Weight_gm'}, inplace=True)
merge_all['PROD_NAME_new'] = result[0]
merge_all['Weight_gms'] = result[1]
print(merge_all)


# In[199]:


#grouping based on package weight in gms
Packweight_wise =merge_all.groupby(['Weight_gms','PROD_NAME_new']).TOT_SALES.agg([sum])
print(Packweight_wise.head)


# In[266]:


pi=Packweight_wise.index
type(pi)
Packweight_wise.reset_index()
new_Packweight_wise= Packweight_wise.reset_index()
print(new_Packweight_wise)
new_Packweight_wise.info()


# In[267]:


new_Packweight_wise.rename(columns = {'sum':'TOTAL_sales'}, inplace = True)
new_Packweight_wise.info()


# # Ploting weight wise Total sale value
# 

# In[204]:


plt.figure(figsize=(200, 15))
plt.title("total sales package weight wise")
sb.barplot(x=new_Packweight_wise.PROD_NAME_new, y= new_Packweight_wise.TOTAL_sales, hue= new_Packweight_wise.Weight_gms )
plt.xticks(rotation=90)
plt.savefig('Packweight_wise_sales.jpg')


# In[268]:


new_Packweight_wise['Weight_gms']= new_Packweight_wise['Weight_gms'].astype(str).astype(int)
new_Packweight_wise.info()


# In[273]:


new_Packweight_wise22 = new_Packweight_wise.sort_values (by='Weight_gms', ascending=False)
print(new_Packweight_wise22)
new_Packweight_wise22.info()
plt.figure(figsize=(20, 10))
plt.title("total sales package weight wise")
sb.barplot(x=new_Packweight_wise.Weight_gms, y= new_Packweight_wise.TOTAL_sales)
plt.xticks(rotation=90)
plt.savefig('Packweight_wise_sales1.jpg')


# # 1) The Above graph clearly indicates customer are more inclinded toward higher weight packagaes mostly above 200gms

# # 2) 70gm to 135gms are least prefered package sizes. 

# In[102]:


#grouping based on membership type ( PREMIUM_CUSTOMER)
lifestage =merge_all.groupby(['PREMIUM_CUSTOMER',LIFESTAGE']).TOT_SALES.agg([sum])
print(lifestage.head)


# In[ ]:





# In[93]:


li = lifestage.index
type(li)
lifestage.reset_index()


# In[94]:


new_lf1= lifestage.reset_index()
print(new_lf1)
new_lf1.info()


# In[97]:


new_lf1.rename(columns = {'sum':'TOTAL_sales'}, inplace = True)
print(new_lf1)


# In[320]:


plt.figure(figsize=(20, 7))
plt.title("total sales distribution Customer membership and lifestage wise")
sb.barplot(x=new_lf1.LIFESTAGE, y= new_lf1.TOTAL, hue= new_lf1.PREMIUM_CUSTOMER )
plt.savefig('tot_sales_Cust_membership_based.jpg')


# In[274]:


## From above plot we can clearly see that New Families & Midage Single/Couples contribute to the lowest overall sales value. This group needs to be targeted to increase sale value 
## OLDER SINGLES/COUPLES have the highest sales value
## Mainstream customer membership type has the most sales values in almost all lifestage types 


# # All product wise sales

# In[106]:


productwise_sales =merge_all.groupby(['LIFESTAGE','PROD_NAME']).TOT_SALES.agg([sum])
productwise_sales.rename(columns = {'sum':'TOTAL_sales'}, inplace = True)
print(productwise_sales)


# In[113]:


pi=productwise_sales.index
type(pi)
productwise_sales.reset_index()


# In[119]:


productwise_sales1= productwise_sales.reset_index()
print(productwise_sales1)
productwise_sales1.info()


# In[147]:


plt.figure(figsize=(100, 10))
plt.title("total sales distribution Customer membership and lifestage wise")
ac=sb.barplot(x=productwise_sales1.PROD_NAME, y= productwise_sales1.TOTAL_sales, hue= productwise_sales1.LIFESTAGE )
plt.xticks(rotation=90)
plt.savefig('product_sales.jpg')


# In[128]:


plt.figure(figsize=(50, 100))
plt.title("total sales distribution Customer membership and lifestage wise")
ax=sb.barplot(x=productwise_sales1.TOTAL_sales, y= productwise_sales1.PROD_NAME, hue= productwise_sales1.LIFESTAGE )
plt.xticks(rotation=90)
plt.savefig('product_sales1.jpg')


# # Premium membership wise sales per product

# In[140]:


premiumwise_sales =merge_all.groupby(['PREMIUM_CUSTOMER','PROD_NAME']).TOT_SALES.agg([sum])
premiumwise_sales.rename(columns = {'sum':'TOTAL_sales'}, inplace = True)
print(premiumwise_sales)


# In[141]:


pi1=premiumwise_sales.index
type(pi1)
premiumwise_sales.reset_index()


# In[145]:


premiumwise_sales1= premiumwise_sales.reset_index()
print(premiumwise_sales1)
premiumwise_sales1.info()


# In[321]:


plt.figure(figsize=(100, 20))
plt.title("total sales distribution Customer membership and lifestage wise")
ac=sb.barplot(x=premiumwise_sales1.PROD_NAME, y= premiumwise_sales1.TOTAL_sales, hue= premiumwise_sales1.PREMIUM_CUSTOMER)
plt.xticks(rotation=90)
plt.savefig('PREMIUM_WISE.jpg')


# In[163]:


plt.figure(figsize=(100, 100))
plt.title("total sales distribution Customer membership and lifestage wise")
ac=sb.barplot(x=premiumwise_sales1.PREMIUM_CUSTOMER, y= premiumwise_sales1.TOTAL_sales, hue= premiumwise_sales1.PROD_NAME)
plt.xticks(rotation=90)
plt.savefig('PREMIUM_WISE1.jpg')


# In[164]:



plt.figure(figsize=(100, 10))
plt.title("total sales distribution Customer membership and lifestage wise")
ac=sb.barplot(x=premiumwise_sales1.PROD_NAME, y= premiumwise_sales1.TOTAL_sales)
plt.xticks(rotation=90)
plt.savefig('PREMIUM_WISE33.jpg')


# In[269]:


#sorting total sales value 
premiumwise_sales2=premiumwise_sales1.sort_values(by='TOTAL_sales', ascending=False)
print(premiumwise_sales2)


# In[276]:


plt.figure(figsize=(100, 35))
plt.title("total sales distribution Customer membership and lifestage wise")
ac=sb.barplot(x=premiumwise_sales2.PROD_NAME, y= premiumwise_sales2.TOTAL_sales)
plt.xticks(rotation=90)
plt.savefig('new.jpg')


# In[174]:


premiumwise_sales2.describe()
premiumwise_sales2.head()


# In[175]:


premiumwise_sales2.max


# In[179]:


plt.figure(figsize=(10, 5))
plt.title("total sales distribution Customer membership wise")
ac=sb.barplot(x=premiumwise_sales2.PREMIUM_CUSTOMER, y= premiumwise_sales2.TOTAL_sales)
plt.savefig('new1.jpg')


# In[297]:


merge_all1= merge_all['TOT_SALES']/ transaction_data['PROD_QTY']
merge_all1.max()
# merge_all["cost_per_product"]= merge_all1
# print(merge_all)


# In[299]:


merge_all1.describe()


# In[291]:


merge_all.sort_values(by="cost_per_product",ascending=False)
print(merger_all)
plt.figure(figsize=(100, 15))
plt.title("Cost per product")
ac=sb.barplot(x=merge_all.PROD_NAME_new, y= merge_all.cost_per_product)
plt.xticks(rotation=90)
plt.savefig('new11.jpg')


# In[294]:


merge_all_sorted= merge_all.sort_values(by="cost_per_product",ascending=False)
print(merge_all_sorted)


# In[295]:


650/200


# In[ ]:




