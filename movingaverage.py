import pandas as pd 
import talib 
from functools import reduce
from talib import SMA 
idx = pd.IndexSlice

class MovingAverage(pd.DataFrame):
    def __init__ (self, multi_data):
        super(MovingAverage,self).__init__()
        self.multi_data = multi_data
        self.columns_l1 = list(self.multi_data.columns.levels[0])
        self.columns_l2 = list(self.multi_data.columns.levels[1]) 
        print(f"*** Warning it is a mult level columns level 1 \n{self.columns_l1}")
        print("Please pass the proper name into SMAAVE to avoid columns names problems")
        
    def Multi_SMA (self, avg_list, col_name):
        range_avg = len(avg_list)
        frames_ = [pd.DataFrame(index=self.multi_data.index) for _ in range(0,range_avg)]
        names_  = [f"SM{val}" for val in avg_list]
        
        # Multiples Moving Average
        for ticker_ in self.columns_l2:
            for avg_ , position in zip (avg_list, range(0,range_avg)):
                SMA_ = SMA(self.multi_data.loc[:,idx["Adj Close",ticker_]].values , timeperiod=int(avg_))         
                
                # Inputtin Columns 
                frames_[position].insert(0, ticker_, SMA_)
                
        # Creating Multi-columns and Concatenating 
        for position in range(0, range_avg):
            frames_[position].columns = (pd.MultiIndex.from_product([[names_[position]],
                                                                     frames_[position].columns]))
        # Merging all DataFrame
        multi_sma = reduce(lambda left, right : pd.merge(left, right, left_index=True,right_index=True),
                                                       frames_)
        return multi_sma
    
    def above_50 (self, col_name , start, td = 60):
        # td = trading dates
        
        above_50 = self.multi_data.loc[:, idx[['Adj Close', col_name],:]].T.unstack()
        trend = above_50.loc['Adj Close', idx[:,:]] - above_50.loc[col_name, idx[:,:]]
        trend = pd.DataFrame(trend.unstack()).loc[start:,:]
        trend = trend[(trend>0)].dropna(axis=1, thresh = td)
        print(f"Finding Stock above 50D SMA with {td} in positive traiding")
        
        return trend
        
