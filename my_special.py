#!/usr/bin/env python
# coding: utf-8

# # <h1 center> Full year report </h1>

# In this report you will find the following:
#
# 1) General financial performance
# - Total amount of money for the year
# - Year cycle: can we see trends over the months
# - Services
#
# 2) Marketting information
# - Who : what are the sources
# - What: which services have more success
# - Mix: which sources bring what
# - How: how is your conversion rate (accepted on total...)
#
# 3) More grannular information on operations: geographic
# - In which Cantons do you go most

# To achieve that we need:
# - To tranform the data & extract the new necessary df
# - To create the graphs
# - To integrate the graphs to the dashboard
# - and more later

# In[1]:


import plotly.express as px
import pandas as pd
import numpy as np
import seaborn as sns  # visualisation
import matplotlib.pyplot as plt  # visualisation
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import os
import seaborn as sns
import chart_studio.plotly as py
import plotly.graph_objects as go


# #### Getting the data

# In[2]:


xls = pd.ExcelFile('/Users/neigelinerivollat/Desktop/SEE/database_see.xlsx')
jan_juil = pd.read_excel(xls, 'Janvier - Juin')
des_juillet = pd.read_excel(xls, 'Juillet - Novembre')

df = pd.concat([jan_juil, des_juillet])
df = pd.DataFrame(df)
# df


# #### Assessing quality of the data

# i. Missing value per column

# In[3]:


# We create a table that counts the number of
# missing values per column.

nas = df.isnull().sum()
nas = pd.DataFrame(nas)

nas
nas.index.name = 'Variable'
nas.reset_index(inplace=True)

# We then create a graph using this table
nas = nas.rename(columns={0: "NA's Count"})
nas
sns.catplot(y="Variable", x="NA's Count", kind="swarm", data=nas)


# ii. Making sure the dates are in order

# In[4]:


df = df.sort_values(by='DATE_DEVIS')


# ## 1) General financial performance

# ### a. Amount for the year

# ##### i. Data transf & extraction

# Here what we need is to select the subset from the dataframe where the devis has been accepted.
#
# In an interactive dashboard the user will be able to select or deselect the additional categories: waiting, and not_accepted.

# In[5]:


# Only need to make sure that no missing value in status devis
# or it won't work.
df = df[df['STATUS_DEVIS'].notna()]

available_indicators = df['STATUS_DEVIS'].unique()

# ##### ii. Graph making

# In[6]:


fig = px.histogram(df, x="DATE_DEVIS", y='MONTANT', color="STATUS_DEVIS")
fig.update_layout(bargap=0.2)
# fig.show()


# ### b. Year cycle trends

# There what we want to see the cumulative amounts of devis signed to see the growth of the CA over the year.
#
# The interactive element would be based on the type of service (AND ideally a third dimension would be the devis status).

# ##### i. Data transf & extraction

# We need to obtain a column for cumulative values.

# In[7]:


df['SERVICE'].astype(str)


# In[8]:


df = df[df['SERVICE'].notna()]


# In[9]:


df['Cumulative_per_serv'] = df['MONTANT'].groupby(df['SERVICE']).cumsum()
df_accepted = df.loc[df['STATUS_DEVIS'] == 'ACCEPTED']
df_accepted['Accept_Cum'] = df_accepted['MONTANT'].groupby(
    df_accepted['SERVICE']).cumsum()
df_accepted

df_to_use = df

service_table = df['SERVICE'].value_counts()
df['SERVICE'] = np.where(df['SERVICE'].isin(
    service_table.index[service_table >= 5]), df['SERVICE'], 'Other_Service')
service_table2 = df['SERVICE'].value_counts()
service_table2 = pd.DataFrame(service_table2).reset_index()
service_table2

fig11 = px.pie(service_table2,
               values='SERVICE',
               names='index',
               color_discrete_map={'CCB': 'green', 'CCP': 'black', 'ING': 'red', 'PEK': 'orange', 'CAH': 'yellow', 'DSB': 'purple', 'AMO': 'brown', 'VEX': 'grey', 'GED': 'red',
                                   'PAP': 'green', 'DOS': 'green'})


fig12 = px.pie(df, values='MONTANT',
               names='SERVICE',
               color_discrete_map={'CCB': 'green', 'CCP': 'black', 'ING': 'red', 'PEK': 'orange', 'CAH': 'yellow', 'DSB': 'purple', 'AMO': 'brown', 'VEX': 'grey', 'GED': 'red',
                                   'PAP': 'green', 'DOS': 'green'})

fig13 = px.pie(df_accepted, values='MONTANT',
               names='SERVICE',
               color_discrete_map={'CCB': 'green', 'CCP': 'black', 'ING': 'red', 'PEK': 'orange', 'CAH': 'yellow', 'DSB': 'purple', 'AMO': 'brown', 'VEX': 'grey', 'GED': 'red',
                                   'PAP': 'green', 'DOS': 'green'})


fig14 = px.histogram(df, x="DATE_DEVIS",
                     y='MONTANT',
                     color="STATUS_DEVIS")
fig14.update_layout(bargap=0.2)


df_accepted['Cumulative_per_serv'] = df_accepted['MONTANT'].groupby(
    df_accepted['SERVICE']).cumsum()

df_accepted['Cumulative'] = df_accepted['MONTANT'].cumsum()

df = df.loc[df['SERVICE'].notna()]
df = df.loc[df['MONTANT'].notna()]


fig15 = px.area(df_accepted, x=df_accepted["DATE_DEVIS"],
                y=df_accepted["Cumulative"])


fig16 = go.Figure()
fig16.add_trace(go.Scatter(
    x=df_accepted['DATE_DEVIS'], y=df_accepted.loc[df_accepted['SERVICE']
                                                   == 'CCB']['Cumulative_per_serv'],
    name='CCB',
    mode='lines',
    line=dict(width=0.5, color='orange'),
    stackgroup='one'))

fig16.add_trace(go.Scatter(
    x=df_accepted['DATE_DEVIS'], y=df_accepted.loc[df_accepted['SERVICE']
                                                   == 'CCP']['Cumulative_per_serv'],
    name='CCP',
    mode='lines',
    line=dict(width=0.5, color='lightgreen'),
    stackgroup='one'))

fig16.add_trace(go.Scatter(
    x=df_accepted['DATE_DEVIS'], y=df_accepted.loc[df_accepted['SERVICE']
                                                   == 'AMO']['Cumulative_per_serv'],
    name='AMO',
    mode='lines',
    line=dict(width=0.5, color='darkred'),
    stackgroup='one'))

fig16.add_trace(go.Scatter(
    x=df_accepted['DATE_DEVIS'], y=df_accepted.loc[df_accepted['SERVICE']
                                                   == 'GED']['Cumulative_per_serv'],
    name='GED',
    mode='lines',
    line=dict(width=0.5, color='blue'),
    stackgroup='one'))

fig16.add_trace(go.Scatter(
    x=df_accepted['DATE_DEVIS'], y=df_accepted.loc[df_accepted['SERVICE']
                                                   == 'DOS']['Cumulative_per_serv'],
    name='DOS',
    mode='lines',
    line=dict(width=0.5, color='red'),
    stackgroup='one'))

fig16.add_trace(go.Scatter(
    x=df_accepted['DATE_DEVIS'], y=df_accepted.loc[df_accepted['SERVICE']
                                                   == 'ING']['Cumulative_per_serv'],
    name='ING',
    mode='lines',
    line=dict(width=0.5, color='purple'),
    stackgroup='one'))

fig16.add_trace(go.Scatter(
    x=df_accepted['DATE_DEVIS'], y=df_accepted.loc[df_accepted['SERVICE']
                                                   == 'DSB']['Cumulative_per_serv'],
    name='DSB',
    mode='lines',
    line=dict(width=0.5, color='brown'),
    stackgroup='one'))

fig16.add_trace(go.Scatter(
    x=df_accepted['DATE_DEVIS'], y=df_accepted.loc[df_accepted['SERVICE']
                                                   == 'AMO']['Cumulative_per_serv'],
    name='AMO',
    mode='lines',
    line=dict(width=0.5, color='grey'),
    stackgroup='one'))

fig16.add_trace(go.Scatter(
    x=df_accepted['DATE_DEVIS'], y=df_accepted.loc[df_accepted['SERVICE']
                                                   == 'VEX']['Cumulative_per_serv'],
    name='VEX',
    mode='lines',
    line=dict(width=0.5, color='grey'),
    stackgroup='one'))

fig16.add_trace(go.Scatter(
    x=df_accepted['DATE_DEVIS'], y=df_accepted.loc[df_accepted['SERVICE']
                                                   == 'PAP']['Cumulative_per_serv'],
    name='PAP',
    mode='lines',
    line=dict(width=0.5, color='mediumorchid'),
    stackgroup='one'))


# In[11]:


fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=df['DATE_DEVIS'],
                          y=df['Cumulative_per_serv'],
                          mode='lines',
                          name='lines+markers'))


# In[12]:
df_accepted = df.loc[df['STATUS_DEVIS'] == 'ACCEPTED']
df_accepted


fig21 = go.Figure()
fig21 = px.line(df, x=df_accepted['DATE_DEVIS'],
                y=df_accepted['Cumulative_per_serv'],
                color=df_accepted['SERVICE'],
                # possibility to make the line more flexible
                line_shape='spline')
# fig2.show()

# In[12]:
df_all = df
fig22 = go.Figure()
fig22 = px.line(df_all, x=df_all['DATE_DEVIS'],
                y=df_all['Cumulative_per_serv'],
                color=df_all['SERVICE'],
                # possibility to make the line more flexible
                line_shape='spline')


# ### c. Services & revenue

# Actually this is kind of what is above?

# ## 2) Marketing

# ### a. What is your conversion rate

# Here we want to understand what is our success, at the global level, but also at the service & source level. This could allow us to identify patterns.
#
# We want a score for the global information & can use a graph to see the information per service and per source.

# ##### Simple scores

# In[22]:


conversion_rate = round(sum(df['STATUS_DEVIS'] == 'ACCEPTED') /
                        len(df['STATUS_DEVIS']), 2)
print("Your conversion rate (accepted devis/total of devis) is of",
      conversion_rate, "%.")


# In[23]:


potential_conversion_rate = round((sum(df['STATUS_DEVIS'] == 'ACCEPTED') + sum(df['STATUS_DEVIS'] == 'WAITING')) /
                                  len(df['STATUS_DEVIS']), 2)

print("Your conversion rate ((accepted devis+waiting devis)/total of devis) is of",
      potential_conversion_rate, "%.")
potential_conversion_rate


# ### b. Who are your sources

# Here we are interested in understanding who brings more work  to SEE in order to better understand where to carry our efforts.
#
# We are also interested in knowing what services they bring most. This could allow us to identify new opportunities for proposal...

# ii. Share of accepted leads per source

# In[43]:


# Cross-tabulate the example data frame.
# Could remove normalise index if wish only absolute information.

df_cross = pd.crosstab(df.SOURCE_LEAD, df.STATUS_DEVIS, normalize='index')

# initiate data list for figure
data = []
# use for loop on every zoo name to create bar data
for x in df_cross.columns:
    data.append(go.Bar(name=str(x), x=df_cross.index, y=df_cross[x]))

fig3 = go.Figure(data)
fig3.update_layout(barmode='stack')

# For you to take a look at the result use
# fig3.show()


# ### c. What service brings more clients

# Here we are interested in understand which service has more success.
#
# This will allow us to answer questions such as:
# - which service needs more marketting
# - what we could stop doing
# - and other...

# In[44]:


# Cross-tabulate the example data frame.
df_cross = pd.crosstab(df.SERVICE, df.STATUS_DEVIS, normalize='index')
# df_cross

# initiate data list for figure
data = []
# use for loop on every zoo name to create bar data
for x in df_cross.columns:
    data.append(go.Bar(name=str(x), x=df_cross.index, y=df_cross[x]))

fig4 = go.Figure(data)
fig4.update_layout(barmode='stack')

# For you to take a look at the result use
# fig4.show()


# ## 3) Operation strategy

# There we add all information that helps us to make global decision for yearly strategy.

# ### a. Partners

# In[77]:


df['SOURCE_LEAD'].isna().sum()
df_for_lead = df[df['SOURCE_LEAD'].notna()]

lead_table = df['SOURCE_LEAD'].value_counts()
lead_table = pd.DataFrame(lead_table)
lead_table.index.name = 'Source'
lead_table = lead_table.reset_index()
# lead_table

fig5 = px.pie(lead_table, values='SOURCE_LEAD', names='Source')
# fig5.show()


# ### b. Geography

# In[53]:


df = df[df['CANTON'].notna()]


# In[63]:


fig6 = px.histogram(df, x="CANTON",
                    color="CANTON",
                    color_discrete_sequence=["black", "green", "red", "grey", "grey"])
fig6.update_layout(bargap=0.2)
# fig6.show()


# In[ ]:
