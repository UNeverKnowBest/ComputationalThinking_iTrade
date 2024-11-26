from tkinter import *
from tkinter import ttk


class RecommendApp:
    def __init__(self, root):
        self.root = root
        self.industry_filter = None
        self.year_filter =  None
        self.ESG_filter = None
        self.start = 0
        self.n = None
        self.year_input = None
        self.dataframe = None
        self.root.title("Stock Recommendation System")
        self.frm = ttk.Frame(self.root, padding="30 30 30 30")
        self.frm.grid(column=0, row=0, sticky="nwes")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        label1 = ttk.Label(self.frm, text="Enter how many stocks do you want the system to recommend:")
        label2 = ttk.Label(self.frm, text="(Please enter a number greater than 0 and less than 100.)")
        self.num_entry = ttk.Entry(self.frm, width=10)
        self.num_entry.grid(column=1, row=3, sticky="w")
        ttk.Label(self.frm, text="Please check the box for the preferences you want to set:").grid(column=1, row=5,
                                                                                              sticky="w")
        self.industry_var = BooleanVar()
        self.year_var = BooleanVar()
        self.esg_var = BooleanVar()
        ttk.Checkbutton(self.frm, text="Highest in the industry", variable=self.industry_var).grid(column=1, row=6, sticky="w")
        ttk.Checkbutton(self.frm, text="Establishment year    Enter the year below:", variable=self.year_var).grid(column=1, row=7,
                                                                                sticky="w")
        entry_year = ttk.Entry(self.frm, width=10)
        ttk.Checkbutton(self.frm, text="ESG criteria", variable=self.esg_var).grid(column=1, row=9, sticky="w")
        ttk.Button(self.frm, text="Search", command=self.stock_search).grid(column=1, row=4, sticky="w")
        label1.grid(column=1, row=1, sticky="w")
        label2.grid(column=1, row=2, sticky="w")
        entry_year.grid(column=1, row=8, sticky="w")

    def create_tree(self, dataframe):
        self.dataframe = dataframe
        tree = ttk.Treeview(self.frm, columns=list(dataframe.columns))
        tree.column("#0", width=0)
        tree.grid(column=1, row=10)
        for col in dataframe.columns:
            tree.column(col)
            tree.heading(col)
            for i in tree.get_children():
                tree.delete(i)
                # 向树中添加新行
            for row in dataframe.to_records(index=False):
                tree.insert("", "end", values=row)

    def stock_search(self):
        self.start = 1
        self.industry_filter = self.industry_var.get()
        self.year_filter = self.year_var.get()
        self.ESG_filter = self.esg_var.get()
        self.n = self.num_entry.get()
        self.year_input = slef.entry_year.get()





