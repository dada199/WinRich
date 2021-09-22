WinRich project

For CN A stock market. 

Stock Analysis. 
量化投资策略

简单的MA线回归测试， 可测试MA10, MA20, MA30, MA60
account 模块:
模拟股票账户， 主要由 pandas DataFrame 表示持股信息.

data 模块:
使用tushare 取得股票日线交易信息。 其中可以包括MA（10,20,30,60）
看实际情况需要，可以取得交易日线的前后和不复权历史行情。
实际对比下来，使用tushare取得的前复权和后复权价格跟股票软件实际的前后复权价格有差别。

todo-
用TA-Lib来计算取得日线的前后复权。

取得的数据存放在项目的data_files 目录中。

strategy 模块：
策略定义。 
理论上可以在类Strategy里面增加任何买卖策略。
目前只实现了MA买卖策略。
简单来说就是根据取得的股票日线信息和MA信息，实行股价在要测试的MA线以下持币，当天股价在要测试的MA线以上持仓。
当股价上穿MA线，买入。 当股价跌穿MA线，卖出。
实际的难点是如何判断买卖价格。

目前可以按照MA线价格
test 模块：
对应的回归测试。 

