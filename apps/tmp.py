
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


def main():
    data_files = [
        "kripke_20181212-202440.csv",
        "kripke_20181212-202631.csv",
        "kripke_20181212-203912.csv",
        "kripke_20181212-204155.csv",
        "kripke_20181212-204410.csv"
    ]

    def get_time_col_from_file(filepath):
        df = pd.read_csv(filepath)
        return df["time"].values

    time = []
    for filepath in data_files:
        time.append(get_time_col_from_file(filepath))
    time = np.array(time)
    print(time.shape)

    plt.figure()
    plt.plot(np.var(time[:3], axis=0))
    # plt.show()

    plt.figure()
    plt.plot(np.var(time, axis=0))
    plt.show()

def convert_kripke_csv():
    df = pd.read_csv("kripke.csv")
    df["layout"] = df["layout"].astype("category")
    df["pmethod"] = df["pmethod"].astype("category")
    cat_columns = df.select_dtypes(['category']).columns
    df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

    df.to_csv("kripke_cleaned.csv", index=False)

def plot_kripke_hist():
    df = pd.read_csv("kripke.csv")
    y = df["time"]
    plt.hist(y, bins=500)
    plt.show()


if __name__ == '__main__':
    # main()
    # convert_kripke_csv()
    plot_kripke_hist()
    