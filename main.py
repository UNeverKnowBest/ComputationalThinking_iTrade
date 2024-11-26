import tkinter as tk

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from scripts.GUI import RecommendApp


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
        df = df[(df["FoundationYear"] >= app.year_input)]

    # If user has only checked the checkbox "industry", execute the year filter algorithm
    if app.industry_filter and not app.ESG_filter:
        df_list = []

        # When the 'industry' checkbox is selected, show the same number of max values for each industry type
        industries_no_mining = ['agriculture', 'clothing', 'construction', 'electronics', 'energy', 'entertainment']
        n_per_industry = app.n // 7
        for industry in industries_no_mining:
            df_i = df[df["Industry"] == industry].sort_values(by=sort_by, ascending=False).head(n_per_industry)
            df_list.append(df_i)

        # Calculate the remainder and fill up to n items using data from the 'mining' category
        n_leave = app.n - n_per_industry * 6
        df_i = df[df["Industry"] == "mining"].sort_values(by=sort_by, ascending=False).head(n_leave)
        df_list.append(df_i)
        df = pd.concat(df_list)

    # Use the same algorithm for processing when both 'ESG' and 'industry' are selected,
    # but first calculate the score based on the entropy weighting method
    elif app.industry_filter and app.ESG_filter:
        sort_by = ["Score"]
        df_list = []

        # Calculate the score based on the entropy weighting method
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

    # If only the ESG is checked, just calculate the entropy score and rank it based on entropy score
    elif not app.industry_filter and app.ESG_filter:
        sort_by = ["Score"]
        df = calculate_scores(df)
        df = df.sort_values(by=sort_by, ascending=False).head(app.n)
    # If no box is checked, raking the data based on performance for high to low
    else:
        df = df.sort_values(by=sort_by, ascending=False).head(app.n)

    return df


def calculate_scores(df):
    """
    Calculate the scores based on entropy
    :param df:
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
