import matplotlib.pyplot as plt
import numpy as np


def draw_date_profit_plot(trading_date_list: list, current_profit_list: list, pic_name: str):
    xp = np.array(trading_date_list)
    yp = np.array(current_profit_list)

    plt.xlabel("Trading date")
    plt.ylabel("Profit & lost")
    plt.title("Profit and lost chart")

    plt.xticks(rotation=45, size=5)
    plt.plot(xp, yp)

    plt.savefig(pic_name)
    plt.close()

    # plt.show()

