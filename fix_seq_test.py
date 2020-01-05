# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 15:28:25 2019

@author: Andy Hsieh
"""

import pandas as pd
import numpy as np
import itertools
'''
job = ['b1','b2','b3','b4','b5']
task = ['a1','a2','a3','a4','a5']


filepatharray="Array.txt"
filepathdata="data.txt"
'''
'''
array=[[0,0,0,1,1]
      ,[1,0,0,0,0]
      ,[0,0,1,1,0]
      ,[0,1,1,0,1]
      ,[0,0,0,0,1]]
'''

'''
task_value = {"a1":36.77891084235486,"a2":90.03019860018104,
         "a3":95.29082159000146,"a4":40.24084233259347,
         "a5":63.558699567441955}
job_value = {"b1":62.49533853124859,"b2":21.048638850868418,
        "b3":84.794291327822,"b4":79.94450103559635,
        "b5":35.75937996177455}
'''
'''
array=[]
with open(filepatharray) as fp:
    line = fp.readlines()[0:5]
    for i in line:
      array.append(i.split(",")[0:5]) 

array = np.transpose(array).tolist()
df = pd.DataFrame(array,index=job,columns=task)

for j in range(len(job)):   
    t1=len(task)-1                   #先記錄每個job需要的最後一個前置task
    temp=0
    while t1>=0:
        if (df.iloc[j][t1] == "1"):
            temp=t1
            print(t1)
            break
        else:
            t1=t1-1   
       
    t2=temp-1
    while t2>=0:  
        if (df.iloc[j][t2] == "1"):
            df.iloc[j][t2] = 0                #將前面的前置task轉為0(拎起來)
        else:
            t2=t2-1
        
print(df)
seq=[]         
no_task_job = []        
       
for t in range(len(task)):          #依照task順序，放入job
    seq.append(task[t])
    for j in range(len(job)):
        
        if (df.iloc[j][t]=="1"):
            seq.append(job[j])

for j in range(len(job)):
    count = 0
    for t in range(len(task)): 
        if (df.iloc[j][t]=="0"):
            count = count+1
        else:
            continue
    if count == len(task):
        no_task_job.append(job[j])

seq.extend(no_task_job)        
print(seq)
'''


x=5
y=5
job = []
task = []
perm_result = []

for i in range(1,x+1):
    task.append("a"+str(i))
    print(task)
    
for j in range(1,y+1):
    job.append("b"+str(j))
    print(job)

filepatharray="Array.txt"
#filepathdata="data.txt"

array=[]
with open(filepatharray) as fp:
    line = fp.readlines()[0:y]
    for i in line:
      array.append(i.split(",")[0:x]) 

array = np.transpose(array).tolist()
df = pd.DataFrame(array,index=job,columns=task)

for i in list(itertools.permutations(range(0,x))):
   print(i)
   df_ch = df.take(i,axis=1)
   #print("111111111",df_ch.columns)
   #print(df_ch.iloc[0][0])
   
   for j in range(len(job)):   
       t1=len(task)-1                   #先記錄每個job需要的最後一個前置task
       temp=0
       while t1>=0:
           if (df_ch.iloc[j][t1] == "1"):
               temp=t1
               #print(t1)
               break
           else:
               t1=t1-1     
       t2=temp-1
       while t2>=0:  
           if (df_ch.iloc[j][t2] == "1"):
               df_ch.iloc[j][t2] = "0"                #將前面的前置task轉為0(拎起來)
           else:
               t2=t2-1
   seq = []         
   no_task_job = []        
   for t in df_ch.columns:          #依照task順序，放入job
      print(t)
      seq.append(t)
      for j in job:
          print(j)
          if (df_ch.loc[j,t]=="1"):
              seq.append(j)

   for j in job:
      count = 0
      for t in df_ch.columns:
          if (df_ch.loc[j,t]=="0"):
              count = count+1
          else:
              continue
      if count == len(i):
          no_task_job.append(j)
          
   seq.extend(no_task_job)        
   print(seq)
   perm_result.append(seq)

#print (list(itertools.permutations(task)))

#x task數量  y:job數量

def create(x,y):
    #x=5
    #y=5
    job = []
    task = []
    perm_result = []
    
    for i in range(1,x+1):
        task.append("a"+str(i))
        print(task)
        
    for j in range(1,y+1):
        job.append("b"+str(j))
        print(job)
    
    filepatharray="Array.txt"
    #filepathdata="data.txt"
    
    array=[]
    with open(filepatharray) as fp:
        line = fp.readlines()[0:y]
        for i in line:
          array.append(i.split(",")[0:x]) 
    
    array = np.transpose(array).tolist()
    df = pd.DataFrame(array,index=job,columns=task)
    
    for i in list(itertools.permutations(range(0,x))):
       print(i)
       df_ch = df.take(i,axis=1)
       #print("111111111",df_ch.columns)
       #print(df_ch.iloc[0][0])
       
       for j in range(len(job)):   
           t1=len(task)-1                   #先記錄每個job需要的最後一個前置task
           temp=0
           while t1>=0:
               if (df_ch.iloc[j][t1] == "1"):
                   temp=t1
                   #print(t1)
                   break
               else:
                   t1=t1-1     
           t2=temp-1
           while t2>=0:  
               if (df_ch.iloc[j][t2] == "1"):
                   df_ch.iloc[j][t2] = "0"                #將前面的前置task轉為0(拎起來)
               else:
                   t2=t2-1
       seq = []         
       no_task_job = []        
       for t in df_ch.columns:          #依照task順序，放入job
          print(t)
          seq.append(t)
          for j in job:
              print(j)
              if (df_ch.loc[j,t]=="1"):
                  seq.append(j)
    
       for j in job:
          count = 0
          for t in df_ch.columns:
              if (df_ch.loc[j,t]=="0"):
                  count = count+1
              else:
                  continue
          if count == len(i):
              no_task_job.append(j)
              
       seq.extend(no_task_job)        
       print(seq)
       perm_result.append(seq)
       
       
    return perm_result

        
        
        
    

        
        
        
        
    
    