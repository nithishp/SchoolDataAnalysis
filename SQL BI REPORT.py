#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


get_ipython().system('pip install ipython-sql')


# In[5]:


dataset = pd.read_excel("D:\Latest TechTest-BI-Dataset 2021.xlsx")


# In[6]:


dataset.head()


# In[20]:


dataset = pd.read_excel("D:\Latest TechTest-BI-Dataset 2021.xlsx",sheet_name = "Data Dictonary")


# In[ ]:





# In[23]:


dataset.head()


# In[25]:


dataset = pd.read_excel("D:\Latest TechTest-BI-Dataset 2021.xlsx",sheet_name = "Teacher Activity")


# In[26]:


dataset.head()


# In[30]:


dataset = pd.read_excel("D:\Latest TechTest-BI-Dataset 2021.xlsx",sheet_name = "Student Activity")


# In[31]:


dataset.head()


# In[18]:


import sqlite3


# In[12]:


get_ipython().run_line_magic('load_ext', 'sql')
get_ipython().run_line_magic('sql', 'sqlite:///:memory:')


# In[40]:


get_ipython().run_cell_magic('sql', '', 'SELECT \n    school_name, \n    AVG(logged_in) * 100 AS avg_login_percentage\nFROM \n    dataset\nGROUP BY \n    is_present\nHAVING \n    AVG(logged_in) * 100 > 60\nORDER BY \n    avg_login_percentage DESC\nLIMIT 5;')


# In[32]:


#1.Top 5 schools with overall teachers’ login% > 60% 


# In[33]:


dataset = pd.read_excel("D:\Latest TechTest-BI-Dataset 2021.xlsx",sheet_name = "Teacher Activity")


# In[34]:


dataset.head()


# In[38]:


SELECT 
    school_name,
    date,
    (logged_in - LAG(logged_in) OVER(PARTITION BY school_name ORDER BY date)) / LAG(logged_in) OVER(PARTITION BY school_name ORDER BY date) * 100 AS login_change_percentage
FROM 
    my_table;


# In[41]:


get_ipython().run_cell_magic('sql', '', 'WITH daily_login_percentage AS (\n    SELECT\n        school_name,\n        login_date,\n        AVG(logged_in) * 100 AS login_percentage\n    FROM \n        my_table\n    GROUP BY \n        school_name, login_date\n),\ndaily_change AS (\n    SELECT\n        school_name,\n        login_date,\n     login_percentage,\n        LAG(login_percentage, 1) OVER (PARTITION BY school_name ORDER BY login_date) AS prev_login_percentage\n    FROM \n        daily_login_percentage\n)\nSELECT\n    school_name,\n    login_date,\n    login_percentage,\n    prev_login_percentage,\n    (login_percentage - prev_login_percentage) AS day_over_day_change\nFROM \n    daily_change\nWHERE \n    prev_login_percentage IS NOT NULL\nORDER BY \n    school_name, login_date;')


# In[42]:


# SQL query to calculate the revenue generated per school
revenue_query = f"""
SELECT 
    school_name, 
    SUM(billable_students * {payment_per_student_per_month}) AS monthly_revenue
FROM 
    my_table
GROUP BY 
    school_name
"""


# In[43]:


# Define the payment per student per month
payment_per_student_per_month = 500
SELECT 
    school_name 
    SUM(billable_students * 500) AS monthly_revenue
FROM 
    my_table
GROUP BY 
    school_name;


# In[44]:


get_ipython().run_cell_magic('sql', '', 'WITH consecutive_logins AS (\n    SELECT\n        school_name,\n        teacher_id,\n        login_date,\n        LAG(login_date, 1) OVER (PARTITION BY school_name, teacher_id ORDER BY login_date) AS prev_day,\n        LAG(login_date, 2) OVER (PARTITION BY school_name, teacher_id ORDER BY login_date) AS prev_prev_day\n    FROM \n        my_table\n    WHERE \n        logged_in = 1\n),\nconsecutive_days AS (\n    SELECT\n        school_name,\n        teacher_id\n    FROM \n        consecutive_logins\n    WHERE \n        julianday(login_date) - julianday(prev_day) = 1\n        AND julianday(prev_day) - julianday(prev_prev_day) = 1\n    GROUP BY \n        school_name, teacher_id\n)\nSELECT \n    school_name, \n    COUNT(teacher_id) AS num_teachers_logged_in_3_days\nFROM \n    consecutive_days\nGROUP BY \n    school_name;')


# In[45]:


WITH WeeklyLogins AS (
    SELECT
        school_id,
        YEARWEEK(login_date) AS week,
        COUNT(DISTINCT student_id) AS weekly_logins
    FROM
        Student_Activity
    WHERE
        login_status = 'Logged In'
    GROUP BY
        school_id, YEARWEEK(login_date)
)


# In[ ]:




