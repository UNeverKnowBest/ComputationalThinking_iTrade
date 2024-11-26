import pandas as pd
import tkinter as tk


from scripts.GUI import RecommendApp

def stock_recommend(app, data):
        if app.year_filter:
            pass



database = pd.read_csv("data/stocks.csv")
root = tk.Tk()
application = RecommendApp(root)

if application.start and application.n is not None:
    stock_recommend(application, database)



root.mainloop()

