import pandas as pd
import tkinter as tk
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from scripts.GUI import RecommendApp


def stock_recommend(app, df):
    sort_by = ["Performance"]
    if app.year_filter:
        df = df[(df["FoundationYear"] >= app.year_input)]

    if app.industry_filter and not app.ESG_filter:
        df_list = []
        industries_no_mining = ['agriculture', 'clothing', 'construction', 'electronics', 'energy', 'entertainment']
        n_per_industry = app.n // 7
        for industry in industries_no_mining:
            df_i = df[df["Industry"] == industry].sort_values(by=sort_by, ascending=False).head(n_per_industry)
            df_list.append(df_i)
        n_leave = app.n - n_per_industry * 6
        df_i = df[df["Industry"] == "mining"].sort_values(by=sort_by, ascending=False).head(n_leave)
        df_list.append(df_i)
        df = pd.concat(df_list)

    elif app.industry_filter and app.ESG_filter:
        sort_by = ["Score"]
        df_list = []
        df = calculate_scores(df)
        industries_no_mining = ['agriculture', 'clothing', 'construction', 'electronics', 'energy', 'entertainment']
        n_per_industry = app.n // 7
        for industry in industries_no_mining:
            df_i = df[df["Industry"] == industry].sort_values(by=sort_by, ascending=False).head(n_per_industry)
            df_list.append(df_i)
        n_leave = app.n - n_per_industry * 6
        df_i = df[df["Industry"] == "mining"].sort_values(by=sort_by, ascending=False).head(n_leave)
        df_list.append(df_i)
        df = pd.concat(df_list)

    elif not app.industry_filter and app.ESG_filter:
        df = calculate_scores(df)

    else:
        df = df.sort_values(by=sort_by, ascending=False)
        
    return df
def calculate_scores(df):
    # 创建原始数据框的副本，避免修改原始数据
    df_processed = df.copy()

    # 计算 Performance 的最小值
    min_performance = df_processed['Performance'].min()
    # 如果最小值小于 0，则计算 shift_value，使得所有值都为正数
    shift_value = -min_performance + 1 if min_performance < 0 else 0

    # 创建一个新的列，存储平移后的 Performance 值
    df_processed['Performance_shifted'] = df_processed['Performance'] + shift_value

    # 定义指标列
    indicators = ['Performance_shifted', 'Environment', 'Social', 'Governance']

    # 保留相关的列
    df_filtered = df_processed[['ID'] + indicators]

    # 初始化 Min-Max 标准化器
    scaler = MinMaxScaler()

    # 对指标进行标准化
    df_normalized = df_filtered.copy()
    df_normalized[indicators] = scaler.fit_transform(df_filtered[indicators])

    # 计算 P 矩阵
    P = df_normalized[indicators].div(df_normalized[indicators].sum(axis=0), axis=1)

    # 替换 0 值以避免 log(0)
    P = P.replace(0, 1e-10)

    # 样本数量
    n = len(df_normalized)

    # 计算熵值 E
    k = 1 / np.log(n)
    E = -k * (P * np.log(P)).sum(axis=0)

    # 计算差异系数 d
    d = 1 - E

    # 计算权重
    weights = d / d.sum()

    # 计算综合得分 Score
    df_normalized['Score'] = df_normalized[indicators].mul(weights).sum(axis=1)

    # 将得分添加回原始数据框，不修改原始指标
    df_with_score = df.copy()
    df_with_score = df_with_score.merge(df_normalized[['ID', 'Score']], on='ID')

    # 按照得分排序
    df_ranked = df_with_score.sort_values(by='Score', ascending=False).reset_index(drop=True)

    return df_ranked


# Read data and initial the GUI
database = pd.read_csv("data/stocks.csv")
root = tk.Tk()
application = RecommendApp(root, database, stock_recommend)

root.mainloop()
