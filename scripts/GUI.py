from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class RecommendApp:
    """The GUI of our system """

    def __init__(self, root, database, stock_recommend_func):
        """

        :param root:
        :param database:
        :param stock_recommend_func:
        """
        self.root = root
        self.stock_recommend_func = stock_recommend_func
        self.industry_filter = None
        self.year_filter = None
        self.ESG_filter = None
        self.start = 0
        self.n = None
        self.year_input = None
        self.dataframe = database
        self.root.title("Stock Recommendation System")
        self.frm = ttk.Frame(self.root, padding="30 30 30 30")
        self.frm.grid(column=0, row=0, sticky="nwes")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.industry_var = BooleanVar()
        self.year_var = BooleanVar()
        self.esg_var = BooleanVar()

        # Initial the label and button of GUI
        label1 = ttk.Label(self.frm, text="Enter how many stocks do you want the system to recommend:")
        label2 = ttk.Label(self.frm, text="(Please enter a number greater than 0 and less than 100.)")
        self.num_entry = ttk.Entry(self.frm, width=10)
        label3 = ttk.Label(self.frm, text="Please check the box for the preferences you want to set:")
        check_button_1 = ttk.Checkbutton(self.frm, text="Highest in the industry", variable=self.industry_var)
        check_button_2 = ttk.Checkbutton(self.frm, text="Establishment year    Enter the year below:",
                                         variable=self.year_var)
        self.entry_year = ttk.Entry(self.frm, width=10)
        check_button_3 = ttk.Checkbutton(self.frm, text="ESG criteria", variable=self.esg_var)
        button_1 = ttk.Button(self.frm, text="Search", command=self.stock_search)
        label1.grid(column=1, row=1, sticky="w")
        label2.grid(column=1, row=2, sticky="w")
        self.num_entry.grid(column=1, row=3, sticky="w")
        button_1.grid(column=1, row=4, sticky="w")
        label3.grid(column=1, row=5, sticky="w")
        check_button_1.grid(column=1, row=6, sticky="w")
        check_button_2.grid(column=1, row=7, sticky="w")
        self.entry_year.grid(column=1, row=8, sticky="w")
        check_button_3.grid(column=1, row=9, sticky="w")

    def create_tree(self, dataframe):
        """
        Create the tree to show our final result on  our GUI
        :param dataframe:
        """
        tree = ttk.Treeview(self.frm)
        tree.grid(column=1, row=10, sticky='nsew')

        # Define the columns
        tree["columns"] = list(dataframe.columns)
        tree.column("#0", width=0)
        for col in dataframe.columns:
            tree.column(col, width=100)
            tree.heading(col, text=col, )

        # Remove old data
        for i in tree.get_children():
            tree.delete(i)

        # Insert new data
        for index, row in dataframe.iterrows():
            tree.insert("", "end", values=list(row))

        # Add a scroll bar
        vsb = ttk.Scrollbar(self.frm, orient="vertical", command=tree.yview)
        vsb.grid(column=2, row=10, sticky='ns')
        tree.configure(yscrollcommand=vsb.set)
        result_length = len(dataframe)
        if len(dataframe) < self.n:
            message = ("The requirements you set are too strict "
                       "resulting in fewer data points than your input value, with only {n} entries."
                                        "You may consider adjusting the filtering criteria.").format(n=result_length)
            messagebox.showerror("Attention!", message)

    def stock_search(self):
        """When press the search button, invoke this method"""
        self.start = 1
        self.industry_filter = self.industry_var.get()
        self.year_filter = self.year_var.get()
        self.ESG_filter = self.esg_var.get()

        # Check the input of n
        try:
            self.n = int(self.num_entry.get())
        except ValueError:
            messagebox.showerror("Input fault", "Please enter a number greater than 0 and less than 100.")
            return

        # Check the input of year
        if self.year_filter:
            try:
                self.year_input = int(self.entry_year.get())
            except ValueError:
                messagebox.showerror("Input fault", "Please enter a valid year.")
                return

        df = self.stock_recommend_func(self, self.dataframe)
        self.create_tree(df)
