# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 13:03:21 2021

@author: lenovo
"""

from WindPy import w
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
w.start()

#Fetch historical data from WindPy
date = datetime.date.today()
wdata = w.wsd("000905.SH,000300.SH,000016.SH,IH00.CFE,IH01.CFE,IH02.CFE,IH03.CFE,IF00.CFE,IF01.CFE,IF02.CFE,IF03.CFE,IC00.CFE,IC01.CFE,IC02.CFE,IC03.CFE", "close",'2017-01-01',date,'')
expiry = w.wsd("IF00.CFE,IF01.CFE,IF02.CFE,IF03.CFE", "ltdate_new", "2017-01-01", date, "")

#Transfer Wind data to DataFrame
data = pd.DataFrame(wdata.Data, index=wdata.Codes, columns=wdata.Times).T
ex_date = pd.DataFrame(expiry.Data, index=expiry.Codes, columns=expiry.Times).T

#Calculate basis for IF
data['IF00_basis'] = data['IF00.CFE'] - data['000300.SH']
data['IF01_basis'] = data['IF01.CFE'] - data['000300.SH']
data['IF02_basis'] = data['IF02.CFE'] - data['000300.SH']
data['IF03_basis'] = data['IF03.CFE'] - data['000300.SH']

#Calculate basis for IH
data['IH00_basis'] = data['IH00.CFE'] - data['000016.SH']
data['IH01_basis'] = data['IH01.CFE'] - data['000016.SH']
data['IH02_basis'] = data['IH02.CFE'] - data['000016.SH']
data['IH03_basis'] = data['IH03.CFE'] - data['000016.SH']

#Calculate basis for IC
data['IC00_basis'] = data['IC00.CFE'] - data['000905.SH']
data['IC01_basis'] = data['IC01.CFE'] - data['000905.SH']
data['IC02_basis'] = data['IC02.CFE'] - data['000905.SH']
data['IC03_basis'] = data['IC03.CFE'] - data['000905.SH']

#Calculate the log return of indices & basis
data['ret_300'] = (data['000300.SH']-data['000300.SH'].shift(1))/data['000300.SH'].shift(1)
data['ret_50'] = (data['000016.SH']-data['000016.SH'].shift(1))/data['000016.SH'].shift(1)
data['ret_500'] = (data['000905.SH']-data['000905.SH'].shift(1))/data['000905.SH'].shift(1)

'''Correlation analysis for index return & basis return'''
'''
data['ret_IF00_basis'] = (data['IF00_basis']-data['IF00_basis'].shift(1))/data['000300.SH'].shift(1)
data['ret_IF01_basis'] = (data['IF01_basis']-data['IF01_basis'].shift(1))/data['000300.SH'].shift(1)
data['ret_IF02_basis'] = (data['IF02_basis']-data['IF02_basis'].shift(1))/data['000300.SH'].shift(1)
data['ret_IF03_basis'] = (data['IF03_basis']-data['IF03_basis'].shift(1))/data['000300.SH'].shift(1)

data['ret_IH00_basis'] = (data['IH00_basis']-data['IH00_basis'].shift(1))/data['000016.SH'].shift(1)
data['ret_IH01_basis'] = (data['IH01_basis']-data['IH01_basis'].shift(1))/data['000016.SH'].shift(1)
data['ret_IH02_basis'] = (data['IH02_basis']-data['IH02_basis'].shift(1))/data['000016.SH'].shift(1)
data['ret_IH03_basis'] = (data['IH03_basis']-data['IH03_basis'].shift(1))/data['000016.SH'].shift(1)

data['ret_IC00_basis'] = (data['IC00_basis']-data['IC00_basis'].shift(1))/data['000905.SH'].shift(1)
data['ret_IC01_basis'] = (data['IC01_basis']-data['IC01_basis'].shift(1))/data['000905.SH'].shift(1)
data['ret_IC02_basis'] = (data['IC02_basis']-data['IC02_basis'].shift(1))/data['000905.SH'].shift(1)
data['ret_IC03_basis'] = (data['IC03_basis']-data['IC03_basis'].shift(1))/data['000905.SH'].shift(1)

#Build a dataframe only contains returns of indices & basis
IF_mat = data.loc[wdata.Times[1]:date,['ret_300','ret_IF00_basis','ret_IF01_basis','ret_IF02_basis','ret_IF03_basis']]
IH_mat = data.loc[wdata.Times[1]:date,['ret_50','ret_IH00_basis','ret_IH01_basis','ret_IH02_basis','ret_IH03_basis']]
IC_mat = data.loc[wdata.Times[1]:date,['ret_500','ret_IC00_basis','ret_IC01_basis','ret_IC02_basis','ret_IC03_basis']]

#Correlation matrix for three indices & basis
IF_corr_mat = IF_mat.corr()
IH_corr_mat = IH_mat.corr()
IC_corr_mat = IC_mat.corr()

#Correlation matrix in the last 200 trading days
IF_corr_mat_200 = IF_mat.iloc[-200:].corr()
IH_corr_mat_200 = IH_mat.iloc[-200:].corr()
IC_corr_mat_200 = IC_mat.iloc[-200:].corr()

#Plot the heatmap of correlation matrix
sns.heatmap(IC_corr_mat, cmap='Reds', annot=True)
sns.heatmap(IC_corr_mat_200, cmap='Reds', annot=True)
'''

#Calculate the time to maturity for existing contracts
ex_date['Cur_date'] = ex_date.index
ex_date['Time_to_maturity_00'] = 0
ex_date['Time_to_maturity_01'] = 0
ex_date['Time_to_maturity_02'] = 0
ex_date['Time_to_maturity_03'] = 0

for i in range(len(ex_date['Cur_date'])):
    diff00 = ex_date['IF00.CFE'].dt.to_pydatetime()[i].date() - ex_date['Cur_date'][i]
    ex_date['Time_to_maturity_00'][i] = diff00.days
    diff01 = ex_date['IF01.CFE'].dt.to_pydatetime()[i].date() - ex_date['Cur_date'][i]
    ex_date['Time_to_maturity_01'][i] = diff01.days
    diff02 = ex_date['IF02.CFE'].dt.to_pydatetime()[i].date() - ex_date['Cur_date'][i]
    ex_date['Time_to_maturity_02'][i] = diff02.days
    diff03 = ex_date['IF03.CFE'].dt.to_pydatetime()[i].date() - ex_date['Cur_date'][i]
    ex_date['Time_to_maturity_03'][i] = diff03.days

#Calculate the annualized basis
data['Annualized_basis_IF00'] = data['IF00_basis']/data['000300.SH']*365/ex_date['Time_to_maturity_00']
data['Annualized_basis_IF01'] = data['IF01_basis']/data['000300.SH']*365/ex_date['Time_to_maturity_01']
data['Annualized_basis_IF02'] = data['IF02_basis']/data['000300.SH']*365/ex_date['Time_to_maturity_02']
data['Annualized_basis_IF03'] = data['IF03_basis']/data['000300.SH']*365/ex_date['Time_to_maturity_03']

data['Annualized_basis_IH00'] = data['IH00_basis']/data['000016.SH']*365/ex_date['Time_to_maturity_00']
data['Annualized_basis_IH01'] = data['IH01_basis']/data['000016.SH']*365/ex_date['Time_to_maturity_01']
data['Annualized_basis_IH02'] = data['IH02_basis']/data['000016.SH']*365/ex_date['Time_to_maturity_02']
data['Annualized_basis_IH03'] = data['IH03_basis']/data['000016.SH']*365/ex_date['Time_to_maturity_03']

data['Annualized_basis_IC00'] = data['IC00_basis']/data['000905.SH']*365/ex_date['Time_to_maturity_00']
data['Annualized_basis_IC01'] = data['IC01_basis']/data['000905.SH']*365/ex_date['Time_to_maturity_01']
data['Annualized_basis_IC02'] = data['IC02_basis']/data['000905.SH']*365/ex_date['Time_to_maturity_02']
data['Annualized_basis_IC03'] = data['IC03_basis']/data['000905.SH']*365/ex_date['Time_to_maturity_03']

#Extract the annualized basis for 3 indices
IF_annualized_basis = data.loc[wdata.Times[0]:date,['Annualized_basis_IF00','Annualized_basis_IF01','Annualized_basis_IF02','Annualized_basis_IF03']]
IH_annualized_basis = data.loc[wdata.Times[0]:date,['Annualized_basis_IH00','Annualized_basis_IH01','Annualized_basis_IH02','Annualized_basis_IH03']]
IC_annualized_basis = data.loc[wdata.Times[0]:date,['Annualized_basis_IC00','Annualized_basis_IC01','Annualized_basis_IC02','Annualized_basis_IC03']]

#Replace inf on the delivery date with 0
IF_annualized_basis.replace([np.inf, -np.inf],0,inplace=True)
IH_annualized_basis.replace([np.inf, -np.inf],0,inplace=True)
IC_annualized_basis.replace([np.inf, -np.inf],0,inplace=True)

#Calculate the moving average of annualized basis
IF_annualized_basis['MA20_IF00'] = IF_annualized_basis.Annualized_basis_IF00.rolling(20).mean()
IF_annualized_basis['MA20_IF01'] = IF_annualized_basis.Annualized_basis_IF01.rolling(20).mean()
IF_annualized_basis['MA20_IF02'] = IF_annualized_basis.Annualized_basis_IF02.rolling(20).mean()
IF_annualized_basis['MA20_IF03'] = IF_annualized_basis.Annualized_basis_IF03.rolling(20).mean()

IH_annualized_basis['MA20_IH00'] = IH_annualized_basis.Annualized_basis_IH00.rolling(20).mean()
IH_annualized_basis['MA20_IH01'] = IH_annualized_basis.Annualized_basis_IH01.rolling(20).mean()
IH_annualized_basis['MA20_IH02'] = IH_annualized_basis.Annualized_basis_IH02.rolling(20).mean()
IH_annualized_basis['MA20_IH03'] = IH_annualized_basis.Annualized_basis_IH03.rolling(20).mean()

IC_annualized_basis['MA20_IC00'] = IC_annualized_basis.Annualized_basis_IC00.rolling(20).mean()
IC_annualized_basis['MA20_IC01'] = IC_annualized_basis.Annualized_basis_IC01.rolling(20).mean()
IC_annualized_basis['MA20_IC02'] = IC_annualized_basis.Annualized_basis_IC02.rolling(20).mean()
IC_annualized_basis['MA20_IC03'] = IC_annualized_basis.Annualized_basis_IC03.rolling(20).mean()

#Drop nan
IF_annualized_basis = IF_annualized_basis.dropna(axis=0, how='any')
IH_annualized_basis = IH_annualized_basis.dropna(axis=0, how='any')
IC_annualized_basis = IC_annualized_basis.dropna(axis=0, how='any')

#Plot the graphs for annualized basis
fig = plt.figure(figsize=(14,21))
sns.set_style('darkgrid')
fig.add_subplot(3,1,1)
sns.lineplot(data=IF_annualized_basis.loc[:,['MA20_IF00','MA20_IF01','MA20_IF02','MA20_IF03']][-11:-1])
fig.add_subplot(3,1,2)
sns.lineplot(data=IH_annualized_basis.loc[:,['MA20_IH00','MA20_IH01','MA20_IH02','MA20_IH03']][-11:-1])
fig.add_subplot(3,1,3)
sns.lineplot(data=IC_annualized_basis.loc[:,['MA20_IC00','MA20_IC01','MA20_IC02','MA20_IC03']][-11:-1])

#Take out the current month basis as it is too volatile
fig = plt.figure(figsize=(14,21))
sns.set_style('darkgrid')
fig.add_subplot(3,1,1)
sns.lineplot(data=IF_annualized_basis.loc[:,['MA20_IF01','MA20_IF02','MA20_IF03']][-11:-1])
fig.add_subplot(3,1,2)
sns.lineplot(data=IH_annualized_basis.loc[:,['MA20_IH01','MA20_IH02','MA20_IH03']][-11:-1])
fig.add_subplot(3,1,3)
sns.lineplot(data=IC_annualized_basis.loc[:,['MA20_IC01','MA20_IC02','MA20_IC03']][-11:-1])

#Calculate the short roll cost
ex_date['00_to_01'] = ex_date['Time_to_maturity_01'] - ex_date['Time_to_maturity_00']
ex_date['00_to_02'] = ex_date['Time_to_maturity_02'] - ex_date['Time_to_maturity_00']
ex_date['00_to_03'] = ex_date['Time_to_maturity_03'] - ex_date['Time_to_maturity_00']

data['roll_cost_IF01'] = -(data['IF01.CFE']-data['IF00.CFE'])/data['IF00.CFE']*365/ex_date['00_to_01']
data['roll_cost_IF02'] = -(data['IF02.CFE']-data['IF00.CFE'])/data['IF00.CFE']*365/ex_date['00_to_02']
data['roll_cost_IF03'] = -(data['IF03.CFE']-data['IF00.CFE'])/data['IF00.CFE']*365/ex_date['00_to_03']

data['roll_cost_IH01'] = -(data['IH01.CFE']-data['IH00.CFE'])/data['IH00.CFE']*365/ex_date['00_to_01']
data['roll_cost_IH02'] = -(data['IH02.CFE']-data['IH00.CFE'])/data['IH00.CFE']*365/ex_date['00_to_02']
data['roll_cost_IH03'] = -(data['IH03.CFE']-data['IH00.CFE'])/data['IH00.CFE']*365/ex_date['00_to_03']

data['roll_cost_IC01'] = -(data['IC01.CFE']-data['IC00.CFE'])/data['IC00.CFE']*365/ex_date['00_to_01']
data['roll_cost_IC02'] = -(data['IC02.CFE']-data['IC00.CFE'])/data['IC00.CFE']*365/ex_date['00_to_02']
data['roll_cost_IC03'] = -(data['IC03.CFE']-data['IC00.CFE'])/data['IC00.CFE']*365/ex_date['00_to_03']

#Extract the short roll cost for 3 indices
IF_roll_cost = data.loc[:,['roll_cost_IF01','roll_cost_IF02','roll_cost_IF03']]
IH_roll_cost = data.loc[:,['roll_cost_IH01','roll_cost_IH02','roll_cost_IH03']]
IC_roll_cost = data.loc[:,['roll_cost_IC01','roll_cost_IC02','roll_cost_IC03']]

#Plot the short roll cost
fig = plt.figure(figsize=(14,21))
sns.set_style('darkgrid')
fig.add_subplot(3,1,1)
sns.lineplot(data=IF_roll_cost[-11:-1])
fig.add_subplot(3,1,2)
sns.lineplot(data=IH_roll_cost[-11:-1])
fig.add_subplot(3,1,3)
sns.lineplot(data=IC_roll_cost[-11:-1])