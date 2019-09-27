#!/usr/bin/python
# encoding: utf-8
CP=float
Ct=str
Cw=list
CG=False
Cv=dict
Cy=True
CT=print
Cu=any
import os
D=os.path
import sys
z=sys.path
z.append('/Users/luoyonggui/PycharmProjects/mayiutils_n1/mayiutils/db')
from pymongo_wrapper import PyMongoWrapper
import pandas as pd
Co=pd.date_range
CI=pd.to_datetime
Ch=pd.read_pickle
CS=pd.concat
B=pd.DataFrame
X=pd.read_excel
import numpy as np
CR=np.where
class i:
 def __init__(P):
  pass
 def k(P):
  pass
 def Q(P):
  pass
 def f(P):
  pass
class O:
 def __init__(P):
  pass
 def x(P):
  pass
from attr import attrs,attrib,fields
from cattr import unstructure,structure
from datetime import datetime,date
Cn=datetime.strptime
CE=datetime.now
@attrs
class U:
 C=attrib(type=CP,default=0)
 S=attrib(type=CP,default=0)
 h=attrib(type=CP,default=0)
 I=attrib(type=datetime,default=CE())
 o=attrib(type=Ct,default='cash')
 R=attrib(type=Ct,default='pingan')
@attrs
class F(i):
 E=attrib(factory=Cw,repr=CG)
 n=attrib(factory=Cw)
 def k(P,R):
  if R not in P._accounts:
   P._accounts.append(R)
 def Q(P,R):
  if R not in P._accounts:
   P._accounts.remove(R)
 def f(P):
  for a in P._accounts:
   a.notify(P._transaction_list)
@attrs
class g(O):
 t=attrib(type=Ct)
 w=attrib(factory=Cw,repr=CG)
 G=attrib(factory=Cv)
 v=attrib(type=CP,default=0)
 def x(P,q):
  for t in q:
   if t.account==P._name:
    P._trade_list.append(t)
    if t.target=='cash':
     P._cash+=t.num
    else:
     C=t.num
     y=t.num*t.price
     T=5 if y*0.00025<5 else y*0.00025
     if t.target in P._positions:
      C+=P._positions[t.target][0]
      y+=P._positions[t.target][1]*P._positions[t.target][0]
     u=(y+T)/C
     P._positions[t.target]=(C,u)
def c():
 df=X('data/transactions.xlsx')
 r=[]
 for j in df.itertuples():
  if j.target!='cash':
   r.append([j.trade_date,j.account,'cash',1,-1*(j.price*j.num*1+j.fee_rate),0])
 d=B(r,columns=df.columns)
 df=CS([df,d],ignore_index=Cy)
 CT(df)
 if not df.empty:
  W=PyMongoWrapper()
  W.insertDataframe(df,'finance','transactions')
 else:
  CT('no transactions!')
L=D.dirname(D.abspath(__file__))
K=Ch(D.join(L,'data/stock_dict.pkl'))
p=Ch(D.join(L,'data/fund_otc_series.pkl'))
M=K.append(p)
def r(o,s):
 if o=='cash':
  return CE().date(),1
 if Cu([o.endswith('.SZ'),o.endswith('.SH')]):
  b=o
 else:
  b=M.loc[o]
 W=PyMongoWrapper()
 m=W.getCollection('finance',b)
 r=Cw(W.findAll(m,{'trade_date':{'$lte':Cn(s,'%Y%m%d')}},fieldlist=['trade_date','close','pct_chg'],sort=[('trade_date',-1)],limit=1))[0]
 return r['trade_date'].date(),r['close']
def H(J,s):
 J=J[:s]
 Y=J.groupby(['account','target'])['num','cost'].sum()
 Y.reset_index(inplace=Cy)
 Y['price']=0
 Y['tdate']=0
 for i in J['target'].unique():
  Y.loc[Y.target==i,['tdate','price']]=r(i,s)
 Y['type']=CR((Y.account=='PA')&(Y.target!='cash'),'STOCK',CR((Y.account=='ZLT')&(Y.target!='cash'),'FUND',CR((Y.account.isin(['TTJ','TTA']))&(Y.target!='cash'),'OTC_FUND','cash')))
 Y['market_val']=Y.num*Y.price
 Y['profit']=Y['market_val']-Y['cost']
 s=Y.groupby('account')['market_val'].sum()
 s.loc['TOTAL']=s.sum()
 l=B(s).T
 l.index.name='date'
 l.index=CI([s])
 return l
if __name__=='__main__':
 q=[]
 W=PyMongoWrapper()
 m=W.getCollection('finance','transactions')
 A='trade_date account target price num fee_rate'.split()
 rs=W.findAll(m,fieldlist=A,sort=[('trade_date',1)])
 J=B(rs)
 J.set_index('trade_date',inplace=Cy)
 J['cost']=J['price']*J['num']*(1+J.fee_rate)
 e=B()
 N=Co('20190921','20190926',freq='B')
 for d in N:
  d=d.strftime('%Y%m%d')
  if e.empty:
   e=H(J,d)
  else:
   e=CS([e,H(J,d)])
 CT(e)
 e.plot(subplots=Cy,figsize=(8,14))
# Created by pyminifier (https://github.com/liftoff/pyminifier)

