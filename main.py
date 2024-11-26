import pandas as pd
import tkinter as tk


from scripts.GUI import RecommendApp

def stock_recommend(app, df):
        # If the year_filter was checked, we filter data and only show final data from this year
        if app.year_filter:
            df = df[(df["FoundationYear"] >= app.year_input)]
        # If the ESG_filter was checked. we use the entropy algorithm to calculate a Composite Score and
        # ranking based on it
        if app.ESG_filter:
            df = stock_entropy_calculate(df)

        if app.industry_filter:
            df = df[(df["IndustryType"] == 'Industry')]

        return df

def stock_entropy_calculate(df):
    composite_score = 0
    return composite_score



database = pd.read_csv("data/stocks.csv")
root = tk.Tk()
application = RecommendApp(root)

# When users press the "search" button, and they have already input n, the search algorithm start to process
if application.start and application.n is not None:
    stock_recommend(application, database)



root.mainloop()

