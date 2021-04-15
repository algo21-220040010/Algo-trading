
import pandas as pd
import numpy as np
from exchange.Exchange import Exchange

class Exchange_API:
    """Exchange_API
    The API of the exchange.

    """
    def setAccountId(self,account_id:float):
        """
        :param account_id: The account id of the trader in the exchange.
        """
        self.account_id=account_id

    def setStartDate(self,startDate:str='20100416'):
        """
        :param startDate: The start date of the backtest.
        """
        self.startDate = startDate

    def setInitCash(self,init_cash:float=10000):
        """
        :param init_cash: The initial cash.
        """
        self.init_cash=init_cash

    def setSlippage(self,slippage_rate:float)
        """
        :param slippage_rate: The slippage rate of the trade.
        """
        self.slippage_rate=slippage_rate

    def setCommision(self,commision:float=0.0003):
        """
        :param commision: The commision of the trade
        """
        self.commision=commision

    def setEndDate(self,end_date:str):
        """
        :param end_date: The end date of the backtest.
        """
        self.end_date=end_date

    def setUnitTime(self,unit_time:str):
        """
        :param unit_time: The unit of the time.
        """
        self.unit_time=unit_time





