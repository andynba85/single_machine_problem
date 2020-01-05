# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 21:58:35 2020

@author: Andy Hsieh
"""

import heapq
from operator import itemgetter
import numpy as np
import sys
import time
import csv
import os
import pandas as pd
from pandas import Series
import itertools


class Node(object):
    def __init__(self, level = None, sequence = None, CompletionTime = None):
        self.level = level
        self.sequence = sequence
        self.CompletionTime = CompletionTime
        self.upperBound, self.upperBoundSequence = None, None
        self.lowerBound = self.getLowerBound()
        
        
    def __lt__(self, other):
        return self.lowerBound < other.lowerBound


    def getUpperBound(self):
        remainseq = seqs.copy()
        completionTime = self.CompletionTime
        
        #算已經確定的排序的CT
        for i in self.sequence:
            remainseq.remove(i)     
            
        seq = self.sequence + remainseq
        #算UB，先task再job(根據可行sequence)
        for i in (remainseq):
            if i in totaltasks:
                completionTime += completionTime + tasks.loc[i, 0]
            else:
                completionTime += completionTime + jobs.loc[i, 0]
                
        return completionTime, seq


    def getLowerBound(self):
        #算已經確定的排序的CT
        remainjobs = jobs.copy()
        remaintasks = tasks.copy()
        all = pd.concat([remainjobs, remaintasks])
        completionTime = self.CompletionTime
        
        #算已經確定的排序的CT
        for i in self.sequence:
            all = all.drop([i])
        
        #計算lowerbound 以小到大排列，spt原則
        all = all.sort_values(by=[0])
        for i in range(len(all)):
            completionTime += completionTime + all.iloc[i, 0]
            
        return completionTime
        

    def getChild(self):
        remainJobs = []
        #此node是task
        if(self.sequence[-1] in totaltasks):
            for i in range(len(totaltasks)):
                #不是最後一個task
                if(self.sequence[-1] == totaltasks[i] and i != len(totaltasks) - 1):
                    #加上加一個task
                    remainJobs.append(totaltasks[i + 1])
                    #加上此task連到的job
                    tempjob = df_ch[df_ch[self.sequence[-1]] == 1].index.tolist()
                    remainJobs.extend(tempjob)
                #如果此node是最後一個task
                else:
                    tempjob = df_ch[df_ch[self.sequence[-1]] == 1].index.tolist()
                    #remainJobs.extend(tempjob)
            
            #考慮除了最後一個node的node
            remaintempjob = []
            for i in range(len(self.sequence) - 1): 
                # if = task
                if(self.sequence[i] in totaltasks):
                    #加上task連到的job
                    tempjob = df_ch[df_ch[self.sequence[i]] == 1].index.tolist()
                    remaintempjob.extend(tempjob)
            #刪掉已存在sequence中的job
            temp = []
            #如果這些job已經在本身sequence
            for j in range(len(remaintempjob)):
                if(remaintempjob[j] in self.sequence):
                    temp.append(j)
            #假設只有一個job在本身sequence
            if(len(temp) == 1):
                for k in range(len(temp)): 
                    remaintempjob.remove(remaintempjob[temp[k]])
            #不只一個
            else:
                count = 0
                for k in range(len(temp)): 
                    remaintempjob.remove(remaintempjob[temp[k] - count])
                    count += 1
        
            remainJobs.extend(remaintempjob)
                    
            #把沒有前置task工作的job加入
            for i in range(len(totaljobs)):
                count = 0 
                for j in range(len(totaltasks)):
                    #print(i,j,df.iloc[i][j])
                    if(df_ch.iloc[i][j] == 1):
                        count += 1
                if(count == 0):
                    remainJobs.append(totaljobs[i])
                    
        #此node是job
        else:
            remaintempjob = []
            temp = []
            #掃過本身sequence
            #把有task連到的job加入
            
            #找尋確定的sequence中task所連接的job(可以用但還沒用的job)
            for i in range(len(self.sequence)):
                if(self.sequence[i] in totaltasks):
                    tempjob = df_ch[df_ch[self.sequence[i]] == 1].index.tolist()
                    remaintempjob.extend(tempjob)           
            for j in range(len(remaintempjob)):
                if(remaintempjob[j] in self.sequence):
                    temp.append(j)
            if(len(temp) == 1):
                for k in range(len(temp)): 
                    remaintempjob.remove(remaintempjob[temp[k]])
            else:
                count = 0
                for k in range(len(temp)): 
                    remaintempjob.remove(remaintempjob[temp[k] - count])
                    count += 1
            
            #如果所有的可做的job都在本身sequence了
            #加上下一個task
            counttask = 0
            if (remaintempjob == []):
                for i in range(len(self.sequence)):
                    if(self.sequence[i] in totaltasks):
                       counttask += 1
                if(counttask != len(totaltasks)):
                    remaintempjob.append(totaltasks[counttask])
            remainJobs.extend(remaintempjob)
            
            #把沒有前置task工作的job加入
            for i in range(len(totaljobs)):
                count = 0 
                for j in range(len(totaltasks)):
                    #print(i,j,df.iloc[i][j])
                    if(df_ch.iloc[i][j] == 1):
                        count += 1
                if(count == 0):
                    remainJobs.append(totaljobs[i])   
             
        return remainJobs
    
    
    def getRootChild(self):
        
        #第一個必做的task
        remainWorks = []
        remainWorks.append(totaltasks[0])
        
        #沒有前置task的job加入
        for i in range(len(totaljobs)):
            count = 0 
            for j in range(len(totaltasks)):
                if(df_ch.iloc[i][j] == 1):
                    count += 1
            if(count == 0):
                #if(count == 0):
                    remainWorks.append(totaljobs[i]) 
        #print(remainWorks)
                    
        return remainWorks
        
     
def BnbSlover():
    upperBound = sys.maxsize
    solution = []
    # root is a empty node
    root = Node(level=0, sequence=[], CompletionTime = 0)
    heap = []
    heapq.heappush(heap, root)
    totalNode = 0
    if(root.sequence == []):
        minNode = heapq.heappop(heap)
        for i in minNode.getRootChild():
            a = minNode.sequence.copy()
            a.append(i)
            if(i in totaltasks):
                time = tasks.loc[i, 0]
            else:
                time = jobs.loc[i, 0]
            child = Node(level = minNode.level + 1, sequence = a, CompletionTime = time)
            # only if when child's lower bound is better than current bound
            # the child will be push in heap hoping to get a better solution
            if child.lowerBound < upperBound:
                heapq.heappush(heap, child)
                totalNode += 1
                
                # if child's upper bound is better than current bound
                # update current upper bound and so as the current solution
                child.upperBound, child.upperBoundSequence = child.getUpperBound()
                if child.upperBound < upperBound:
                    upperBound = child.upperBound
                    solution = child.upperBoundSequence.copy()
      
    while len(heap) != 0:
        minNode = heapq.heappop(heap)
        for i in minNode.getChild():
            a = minNode.sequence.copy()
            if(i not in a):
                a.append(i)
            if(i in totaltasks):
                time = minNode.CompletionTime + minNode.CompletionTime + tasks.loc[i, 0]
            else:
                time = minNode.CompletionTime + minNode.CompletionTime +jobs.loc[i, 0]
            child = Node(level = minNode.level + 1, sequence = a, CompletionTime = time)
            # only if when child's lower bound is better than current bound
            # the child will be push in heap hoping to get a better solution
            if child.lowerBound < upperBound:
                heapq.heappush(heap, child)
                totalNode += 1
                
                # if child's upper bound is better than current bound
                # update current upper bound and so as the current solution
                child.upperBound, child.upperBoundSequence = child.getUpperBound()
                if child.upperBound < upperBound:
                    upperBound = child.upperBound
                    solution = child.upperBoundSequence.copy()

    return solution, upperBound, totalNode


if __name__ == '__main__':
    # first for release date ,second for processing time
    
    x = 10
    y = 10
    jobs_init_df = np.loadtxt('jobs.txt',delimiter='\t').tolist()[0:x] #delimiter引數依據原始文字資料每行數字之間符號，這裡為\t
    jobNumber = len(jobs_init_df)
    tasks_init_df = np.loadtxt('tasks.txt',delimiter='\t').tolist()[0:y] #delimiter引數依據原始文字資料每行數字之間符號，這裡為\t
    taskNumber = len(tasks_init_df)
    completionTime = 0
    tasks_init_df = pd.DataFrame(tasks_init_df)
    jobs = pd.DataFrame(jobs_init_df)
    Min_completionTime = sys.maxsize
    Min_sequence = []
    Total_time = 0.0
    
    task_init = []
    job_init = []
    
    #x=3  #task數量，可手動調整
    for i in range(1,x+1):
        task_init.append("a"+str(i))
        #print(task_init)    
    #y=3  #job數量  
    for j in range(1,y+1):
        job_init.append("b"+str(j))
        #print(job_init)
    
    filepatharray="Array.txt"
    array=[]  #抓取Array.txt裡task跟job之間的關係
    with open(filepatharray) as fp:
        line = fp.readlines()[0:y]
        for i in line:
          array.append(i.split(",")[0:x]) 
    array = np.transpose(array).tolist() #將array轉置成job跟task的矩陣關係
    df = pd.DataFrame(array,index=job_init,columns=task_init).astype("int") #按照順序沒有簡化的矩陣
    #print(df)
    #根據columns去做排列組合，根據paper給定task順序 簡化順序
    for i in list(itertools.permutations(range(0,x))):
       #print(i)
       df_ch = df.take(i,axis=1) #根據columns排列組合後簡化矩陣
       #print(df_ch)
       totaltasks = df_ch.columns.tolist() #每輪task的順序
       totaljobs = df_ch.index.tolist() 
       
       tasks = tasks_init_df.take(i,axis=0)
       tasks.index = Series(totaltasks)
       #print(tasks)
      
       jobs.index = Series(totaljobs)
       #print(jobs)
      
       
       for j in range(len(job_init)):   
           t1=len(task_init)-1                   #先記錄每個job需要的最後一個前置task
           temp=0
           while t1>=0:
               if (df_ch.iloc[j][t1] == 1):
                   temp=t1
                   #print(t1)
                   break
               else:
                   t1=t1-1     
           t2=temp-1
           while t2>=0:  
               if (df_ch.iloc[j][t2] == 1):
                   df_ch.iloc[j][t2] = 0                #將前面的前置task轉為0(拎起來)
               else:
                   t2=t2-1
       
       seqs = []         
       no_task_job = []        
       for t in df_ch.columns:          #依照task順序，放入job
          #print(t)
          seqs.append(t)
          for j in job_init:
              #print(j)
              if (df_ch.loc[j,t]== 1):
                  seqs.append(j)
    
       for j in job_init:
          count = 0
          for t in df_ch.columns:
              if (df_ch.loc[j,t]== 0):
                  count = count+1
              else:
                  continue
          if count == len(i):
              no_task_job.append(j)
              
       seqs.extend(no_task_job)        
       #print(seqs)

       tStart = time.time()         
       solution, objectiveValue, totalNode = BnbSlover()
       tEnd = time.time()
       times = (tEnd - tStart)
       print('Sequence:', solution)
       print('Completion Time:', objectiveValue)
       print("It cost %f sec" % (tEnd - tStart),"\n")
       times = (tEnd - tStart)
       Total_time = Total_time + times
       if(objectiveValue < Min_completionTime):
           Min_completionTime = objectiveValue
           Min_sequence = solution
           
    print("--------------------------------------------------------------------------------------------------------------------------")
    print("前"+str(x)+"筆task跟前"+str(y)+"筆job的結果:")
    print('Min Sequence:', Min_sequence)
    print('Min Completion Time:', Min_completionTime)
    print("It total cost %f sec" % (Total_time))
               