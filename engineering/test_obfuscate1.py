#!/usr/bin/python
# encoding: utf-8
M=float
t=str
X=list
g=False
b=dict
mV=True
mE=print
mF=any
import os
G=os.path
import sys
u=sys.path
u.append('/Users/luoyonggui/PycharmProjects/mayiutils_n1/mayiutils/db')
from pymongo_wrapper import PyMongoWrapper
import pandas as pd
N=pd.date_range
R=pd.to_datetime
L=pd.read_pickle
r=pd.concat
w=pd.DataFrame
U=pd.read_excel
import numpy as np
l=np.where
class Publisher:
 def __init__(x):
  pass
 def register(x):
  pass
 def unregister(x):
  pass
 def notify_all(x):
  pass
class Subscriber:
 def __init__(x):
  pass
 def notify(x):
  pass
from attr import attrs,attrib,fields
from cattr import unstructure,structure
from datetime import datetime,date
c=datetime.strptime
e=datetime.now
@attrs
class Transaction:
 m=attrib(type=M,default=0)
 V=attrib(type=M,default=0)
 E=attrib(type=M,default=0)
 F=attrib(type=datetime,default=e())
 T=attrib(type=t,default='cash')
 k=attrib(type=t,default='pingan')
@attrs
class Trade(Publisher):
 p=attrib(factory=X,repr=g)
 a=attrib(factory=X)
 def register(x,k):
  if k not in x._accounts:
   x._accounts.append(k)
 def unregister(x,k):
  if k not in x._accounts:
   x._accounts.remove(k)
 def notify_all(x):
  for a in x._accounts:
   a.notify(x._transaction_list)
@attrs
class Account(Subscriber):
 d=attrib(type=t)
 S=attrib(factory=X,repr=g)
 W=attrib(factory=b)
 q=attrib(type=M,default=0)
 def notify(x,f):
  for t in f:
   if t.account==x._name:
    x._trade_list.append(t)
    if t.target=='cash':
     x._cash+=t.num
    else:
     m=t.num
     o=t.num*t.price
     h=5 if o*0.00025<5 else o*0.00025
     if t.target in x._positions:
      m+=x._positions[t.target][0]
      o+=x._positions[t.target][1]*x._positions[t.target][0]
     z=(o+h)/m
     x._positions[t.target]=(m,z)
def add_transactions():
 df=U('data/transactions.xlsx')
 r=[]
 for I in df.itertuples():
  if I.target!='cash':
   r.append([I.trade_date,I.account,'cash',1,-1*(I.price*I.num*1+I.fee_rate),0])
 A=w(r,columns=df.columns)
 df=r([df,A],ignore_index=mV)
 mE(df)
 if not df.empty:
  K=PyMongoWrapper()
  K.insertDataframe(df,'finance','transactions')
 else:
  mE('no transactions!')
H=G.dirname(G.abspath(__file__))
j=L(G.join(H,'data/stock_dict.pkl'))
y=L(G.join(H,'data/fund_otc_series.pkl'))
i=j.append(y)
def get_last_day_market_val(T,D):
 if T=='cash':
  return e().date(),1
 if mF([T.endswith('.SZ'),T.endswith('.SH')]):
  s=T
 else:
  s=i.loc[T]
 K=PyMongoWrapper()
 v=K.getCollection('finance',s)
 r=X(K.findAll(v,{'trade_date':{'$lte':c(D,'%Y%m%d')}},fieldlist=['trade_date','close','pct_chg'],sort=[('trade_date',-1)],limit=1))[0]
 return r['trade_date'].date(),r['close']
def get_account_val(J,D):
 J=J[:D]
 Q=J.groupby(['account','target'])['num','cost'].sum()
 Q.reset_index(inplace=mV)
 Q['price']=0
 Q['tdate']=0
 for i in J['target'].unique():
  Q.loc[Q.target==i,['tdate','price']]=get_last_day_market_val(i,D)
 Q['type']=l((Q.account=='PA')&(Q.target!='cash'),'STOCK',l((Q.account=='ZLT')&(Q.target!='cash'),'FUND',l((Q.account.isin(['TTJ','TTA']))&(Q.target!='cash'),'OTC_FUND','cash')))
 Q['market_val']=Q.num*Q.price
 Q['profit']=Q['market_val']-Q['cost']
 s=Q.groupby('account')['market_val'].sum()
 s.loc['TOTAL']=s.sum()
 B=w(s).T
 B.index.name='date'
 B.index=R([D])
 return B
if __name__=='__main__':
 f=[]
 K=PyMongoWrapper()
 v=K.getCollection('finance','transactions')
 n='trade_date account target price num fee_rate'.split()
 rs=K.findAll(v,fieldlist=n,sort=[('trade_date',1)])
 J=w(rs)
 J.set_index('trade_date',inplace=mV)
 J['cost']=J['price']*J['num']*(1+J.fee_rate)
 C=w()
 P=N('20190921','20190926',freq='B')
 for d in P:
  d=d.strftime('%Y%m%d')
  if C.empty:
   C=get_account_val(J,d)
  else:
   C=r([C,get_account_val(J,d)])
 mE(C)
 C.plot(subplots=mV,figsize=(8,14))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

