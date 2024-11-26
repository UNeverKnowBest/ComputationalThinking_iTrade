import tkinter as tk

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from scripts.GUI import RecommendApp

def stock_recommend_by_industry(df, n, sort_by):
    """
    When the 'industry' checkbox is selected, show the same number of max values for each industry type
    :param df: original dataframe
    :param n: the number of recommendations
    :param sort_by: sort based on which value
    :return: dataframe
    """

    df_list = []

    industries_no_mining = ['agriculture', 'clothing', 'construction',
                            'electronics', 'energy', 'entertainment',
                            'mining']

    # Make sure sub n of per type have an int value and calculate the reminder
    n_per_industry = n // 7
    n_leave = n - n_per_industry * 7

    for industry in industries_no_mining:
        # Use the reminder to assign to former industry type to fulfill the requirement n
        if n_leave > 0:
            df_i = df[df["Industry"] == industry].sort_values(by=sort_by, ascending=False).head(n_per_industry + 1)
            n_leave -= 1
        else:
            # When it meets the user's requirement n
            df_i = df[df["Industry"] == industry].sort_values(by=sort_by, ascending=False).head(n_per_industry)
        df_list.append(df_i)
    df = pd.concat(df_list)
    return df

def stock_recommend_by_year(df, year):
    """Return the dataframe filtered by year"""
    df = df[(df["FoundationYear"] >= year)]
    return df

def stock_recommend_by_ESG(df):
    """Return the dataframe calculated by entropy algorithm"""
    df = calculate_scores(df)
    return df
def stock_recommend(app, df):
    """
    Return the data by using pandas dataframe filter
    based on user choose which checkbox
    :param app:
    :param df:
    :return: The data which is processed by recommendation algorithm
    """
    # Default the rank strategy based on performance
    sort_by = ["Performance"]

    # If the user has checked the checkbox "year", execute the year filter algorithm to reduce the number of data
    # It should be processed firstly to reduce the computational time
    if app.year_filter:
        df = stock_recommend_by_year(df, app.year_input)

    if app.ESG_filter:
        sort_by = ["Score"]
        df = stock_recommend_by_ESG(df)

    # Then industry recommend's sort is different with other, so we split the sort algorithm into 2 parts.
    if app.industry_filter:
        # Industry sort type
        df = stock_recommend_by_industry(df, app.n, sort_by)
    else:
        # Ordinary type
        df = df.sort_values(by=sort_by, ascending=False).head(app.n)

    return df


def calculate_scores(df):
    """
    Calculate the scores based on entropy
    :param df:  Original dataframe
    :return: The changed dataframe which is added a score colum
    """

    df_processed = df.copy()
    min_performance = df_processed['Performance'].min()
    # If the minimum value is less than 0, calculate 'shift_value' to make all values positive
    shift_value = -min_performance + 1 if min_performance < 0 else 0

    # Create a new column to store the shifted 'Performance' values
    df_processed['Performance_shifted'] = df_processed['Performance'] + shift_value
    indicators = ['Performance_shifted', 'Environment', 'Social', 'Governance']

    # Retain relevant columns
    df_filtered = df_processed[['ID'] + indicators]
    scaler = MinMaxScaler()
    df_normalized = df_filtered.copy()
    df_normalized[indicators] = scaler.fit_transform(df_filtered[indicators])

    # Calculate the P matrix
    p = df_normalized[indicators].div(df_normalized[indicators].sum(axis=0), axis=1)
    p = p.replace(0, 1e-10)
    n = len(df_normalized)

    # Calculate entropy value E
    k = 1 / np.log(n)
    e = -k * (p * np.log(p)).sum(axis=0)

    # Calculate the coefficient of variation d and weights
    d = 1 - e
    weights = d / d.sum()

    # Compute the composite score 'Score'
    df_normalized['Score'] = df_normalized[indicators].mul(weights).sum(axis=1)

    # Add the score back to the original dataframe without modifying the original metrics
    df_with_score = df.copy()
    df_with_score = df_with_score.merge(df_normalized[['ID', 'Score']], on='ID')
    return df_with_score


# Read data and initial the GUI
database = pd.read_csv("data/stocks.csv")
root = tk.Tk()
application = RecommendApp(root, database, stock_recommend)
root.mainloop()