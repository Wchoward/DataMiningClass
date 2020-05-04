import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import datetime

root = 'data/oakland-crime-statistics-2011-to-2016/'
file_lst = ['records-for-' + str(x) + '.csv' for x in range(2011,2017)]

def load_data(path,filename):
    return pd.read_csv(path + '/' + filename, keep_default_na = False, low_memory = False)

def str_to_datetime(s):
    date,time = s.split('T')
    date = date.split('-')
    time = time[:-4].split(':')
    date = [int(x) for x in date]
    time = [int(x) for x in time]
    return datetime.datetime(date[0],date[1],date[2],time[0],time[1],time[2])

# 计算时间间隔
def time_interval(col1,col2):
    start = col1.values;
    end = col2.values;
    ans = []
    for s,e in zip(start,end):
        if e == '':
            continue
        else:
            ans.append(int((str_to_datetime(e)-str_to_datetime(s)).seconds/60))
    return ans

class crime_data():
    def __init__(self, root, file_lst):
        self.data = []
        for i in file_lst:
        	self.data.append(load_data(root, i))
        self.column = ''

    def select_col(self, col):
        self.column = col

    def get_row_index(self, file_index, value):
        lst = []
        entity = []
        for i in range(self.data[file_index].shape[0]):
            if self.data[file_index].loc[i, self.column] == value:
                lst.append(i)
                entity.append(self.data[file_index].loc[i].values)
        return lst, entity

    def delete_row(self, file_index, index_lst):
        self.data[file_index] = self.data[file_index].drop(index=index_lst)
        self.data[file_index].reset_index(drop = True, inplace = True)

    def generate_new_col(self,col1,col2,f):
        for i in self.data:
            res = f(i[col1],i[col2])
            i['duration'] = res

    def five_number(self):
        year = 2011
        for i in self.data:
            col = np.array(i[self.column].values)
            print('Year',str(year))

            print('Min:', np.min(col),end=',')
            print('Q1:', np.percentile(col, 25),end=',')
            print('Q2:', np.percentile(col, 50),end=',')
            print('Q3:', np.percentile(col, 75),end=',')
            print('Max:', np.max(col))
            year += 1

    def box(self,index,w,h,xlabel):
        col = np.array(self.data[index][self.column])
        fig = plt.figure(figsize=(w, h))
        plt.boxplot(col, notch=False, vert=False)
        plt.xlabel(xlabel)
        plt.show()
        outlier = np.percentile(col, 75) + (np.percentile(col, 75) - np.percentile(col, 25)) * 1.5
        print(outlier)

    def seg_hist(self,index,s1,s2,w,h,xlabel,ylabel):
        col = np.array(self.data[index][self.column])
        col.sort()
        p1 = np.searchsorted(col, s1)
        p2 = np.searchsorted(col, s2)
        c1 = col[:p1]
        c2 = col[p1:p2]
        c3 = col[p2:]
        fig1 = plt.figure(figsize=(w, h))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.subplot(131)
        plt.hist(c1, bins=40, alpha=0.7)
        plt.subplot(132)
        plt.hist(c2, bins=40, alpha=0.7)
        plt.subplot(133)
        plt.hist(c3, bins=40, alpha=0.7)
        plt.show()

    def normal_hist(self,index,w,h,xlabel,ylabel):
        col = np.array(self.data[index][self.column])
        fig1 = plt.figure(figsize=(w, h))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.hist(col, bins=40, alpha=0.7)

    def get_fre(self, index):
        col = self.data[index][self.column]
        return col.value_counts()
    
    def normal_bar(self, index, w, h, n_before, n_after, xticks):
        fig = plt.figure(figsize=(w, h))
        plt.subplot(121)
        plt.title('Before')
        yticks = [self.data[index].shape[0] - n_before, n_before]
        plt.bar(xticks, [self.data[index].shape[0] - n_before, n_before])
        for x, y in zip(xticks, yticks):
            plt.text(x, y, '%d' % y, ha='center', va='bottom')
        plt.subplot(122)
        plt.title('After')
        yticks = [self.data[index].shape[0] - n_after, n_after]
        plt.bar(xticks, [self.data[index].shape[0] - n_after, n_after])
        for x, y in zip(xticks, yticks):
            plt.text(x, y, '%d' % y, ha='center', va='bottom')
        plt.show()

    def count_none(self, none_token=''):
        res = []
        y = 2011
        for year in self.data:
            cnt = 0
            year_column = np.array(year[self.column].values)
            for i in year_column:
                if i == none_token:
                    cnt += 1
            res.append(cnt)
            print(y, ':', cnt)
            y += 1
        return res