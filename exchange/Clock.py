
import pandas as pd
import numpy as np

class Clock:

    def __init__(self,start_date:str,end_date:str,unit_time:str):
        """
        :param start_date: The start of the time.
        :param end_date: The end of the time.
        :param unit_time: The unit of the time.
        """
        self.start_date=start_date
        self.end_date=end_date
        self.unit_time=unit_time

    def clock(self):
        date_list=pd.date_range(self.start_date,self.end_date,freq=self.unit_time)
        for time in date_list:
            print(time)

def main():
    c=Clock('20190405','20190406','min')
    c.clock()

if __name__=="__main__":
    main()
