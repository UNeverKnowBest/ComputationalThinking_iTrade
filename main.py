import pandas as pd
import tkinter as tk


from scripts.GUI import RecommendApp

def stock_recommend(app, df):

        sort_by = ["Performance"]
        # If the year_filter was checked, we filter data and only show final data from this year
        if app.year_filter:
            df = df[(df["FoundationYear"] >= app.year_input)]
            df = df.sort_values(by=sort_by, ascending=False)
        # If the ESG_filter was checked. we use the entropy algorithm to calculate a composite score and
        # ranking based on it
        if app.ESG_filter:
            sort_by = ["Composite_score"]
            df = stock_entropy_calculate(df)

        if app.industry_filter:
            df[df["Industry"] == 'agriculture'].sort_values(by=sort_by).head(app.n//7)
            df[df["Industry"] == 'clothing'].sort_values(by=sort_by).head(app.n // 7)
            df[df["Industry"] == 'construction'].sort_values(by=sort_by).head(app.n // 7 )
            df[df["Industry"] == 'electronics'].sort_values(by=sort_by).head(app.n // 7)
            df[df["Industry"] == 'energy'].sort_values(by=sort_by).head(app.n // 7)
            df[df["Industry"] == 'entertainment'].sort_values(by=sort_by).head(app.n // 7)
            df[df["Industry"] == 'mining'].sort_values(by=sort_by).head(app.n // 7)
        return df

def stock_entropy_calculate(df):
    composite_score = 0
    return composite_score

# Read data and initial the GUI
database = pd.read_csv("data/stocks.csv")
root = tk.Tk()
application = RecommendApp(root, database, stock_recommend)

# Load data which is processed by our algorithms

# GUI loop

# When users press the "search" button, and they have already input n, the search algorithm start to process


root.mainloop()