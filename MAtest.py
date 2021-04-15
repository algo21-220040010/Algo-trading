# 导入相关模块
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# 从Wind接口导出数据，并转换为DataFrame形式输出。
from WindPy import w

w.start()
raw_data = w.wsd("002340.SZ", "close", "2020-01-01", "2021-04-15", "Fill=Previous")

if raw_data.ErrorCode == 0:
    # 数据装入Pandas的DataFrame
    fm = pd.DataFrame(raw_data.Data, index=raw_data.Fields, columns=raw_data.Times).T
    fm['LMA'] = fm.CLOSE.rolling(20, min_periods=0).mean()  # 12日均线时间序列
    fm['SMA'] = fm.CLOSE.rolling(7, min_periods=0).mean()  # 6日均线时间序列
    fm['position'] = 0  # 记录持仓
    fm['trade'] = 0  # 记录交易
    fm['time'] = raw_data.Times  # 日期序列
    print('fm:\n', fm)
else:
    print("Error Code:", raw_data.ErrorCode)
    print("Error Message:", raw_data.Data[0][0])


# 策略函数
def Strategy(df):
    for i in range(20, len(df) - 1):
        # 当前空仓、金叉，买进。
        if (df.SMA[i - 1] < df.LMA[i - 1]) & (df.SMA[i] > df.LMA[i]) & (df.position[i] == 0):
            df.iloc[i, 4] = 1
            df.iloc[i + 1, 3] = 1
            print(df.time[i], "买入")

        # 当前持仓、死叉，卖出。
        elif (df.SMA[i - 1] > df.LMA[i - 1]) & (df.SMA[i] < df.LMA[i]) & (df.position[i] == 1):
            df.iloc[i, 4] = -1
            df.iloc[i + 1, 3] = 0
            print(df.time[i], "卖出")

            # 其他情况，仓位不变。
        else:
            df.iloc[i + 1, 3] = df.iloc[i, 3]

    # 日收益率ret，累计净值nav，基准净值benchmark。
    df['ret'] = df.CLOSE.pct_change(1).fillna(0)
    df['nav'] = (1 + df.ret * df.position).cumprod()
    df['benchmark'] = df.CLOSE / df.CLOSE[0]

    return df


# 评价函数
def Performace(df):
    # 年化收益率
    rety = df.nav[df.shape[0] - 1] ** (250 / df.shape[0]) - 1
    # 夏普比率
    Sharp = ((df.ret * df.position).mean()-df.ret.mean()) / (df.ret * df.position).std() * np.sqrt(250)
    # 最大回撤率
    DrawDown = 1 - df.nav / df.nav.cummax()
    MaxDrawDown = max(DrawDown)

    print('夏普比率为:', round(Sharp, 2))
    print('年化收益率为:{}%'.format(round(rety * 100, 2)))
    print('最大回撤为：{}%'.format(round(MaxDrawDown * 100, 2)))

    # 作图
    xtick = np.round(np.linspace(0, df.shape[0] - 1, 7), 0)
    xtick = xtick.astype(np.int)
    xticklabel = df.time[xtick]

    plt.figure(figsize=(9, 4))
    ax = plt.axes()

    plt.plot(np.arange(df.shape[0]), df.benchmark, 'black', label='benchmark', linewidth=2)
    plt.plot(np.arange(df.shape[0]), df.nav, 'red', label='nav', linewidth=2)
    # RS为相对强弱指数。
    plt.plot(np.arange(df.shape[0]), df.nav / df.benchmark, 'yellow', label='RS', linewidth=2)
    plt.legend()
    plt.show()
    ax.set_xticks(xtick)
    ax.set_xticklabels(xticklabel)


    return rety, Sharp, MaxDrawDown


fm = Strategy(fm)

rety, Sharp, MaxDrawDown = Performace(fm)
