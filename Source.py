import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import csv
 
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = []
        self.categories = ['Food', 'Transportation', 'Entertainment', 'Utilities']
 
        # GUI Elements
        self.label_category = ttk.Label(root, text="Expense Category:")
        self.category_var = tk.StringVar(value=self.categories[0])
        self.entry_category = ttk.Combobox(root, textvariable=self.category_var, values=self.categories)
 
        self.label_amount = ttk.Label(root, text="Expense Amount:")
        self.entry_amount = ttk.Entry(root)
 
        self.label_date = ttk.Label(root, text="Expense Date:")
        self.entry_date = ttk.Entry(root)
        self.entry_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
 
        self.button_add = ttk.Button(root, text="Add Expense", command=self.add_expense)
        self.button_plot = ttk.Button(root, text="Plot Expenses", command=self.plot_expenses)
        self.button_total = ttk.Button(root, text="Calculate Total", command=self.calculate_total)
        self.button_save = ttk.Button(root, text="Save Expenses", command=self.save_expenses)
        self.button_load = ttk.Button(root, text="Load Expenses", command=self.load_expenses)
 
        self.label_total = ttk.Label(root, text="Total Expenses: $0.00")
 
        self.listbox_expenses = tk.Listbox(root, selectmode=tk.SINGLE)
        self.scrollbar_expenses = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.listbox_expenses.yview)
        self.listbox_expenses.config(yscrollcommand=self.scrollbar_expenses.set)
 
        # Layout
        self.label_category.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_category.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
 
        self.label_amount.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_amount.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
 
        self.label_date.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_date.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
 
        self.button_add.grid(row=3, column=0, columnspan=2, pady=10)
        self.button_plot.grid(row=4, column=0, columnspan=2, pady=10)
        self.button_total.grid(row=5, column=0, columnspan=2, pady=10)
        self.button_save.grid(row=6, column=0, columnspan=2, pady=10)
        self.button_load.grid(row=7, column=0, columnspan=2, pady=10)
 
        self.label_total.grid(row=8, column=0, columnspan=2, pady=10)
 
        self.listbox_expenses.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)
        self.scrollbar_expenses.grid(row=9, column=2, sticky=tk.NS)
 
        # Configure grid row and column weights
        root.grid_rowconfigure(9, weight=1)
        root.grid_columnconfigure(1, weight=1)
 
    def add_expense(self):
        category = self.entry_category.get()
        amount = float(self.entry_amount.get())
        date_str = self.entry_date.get()
 
        try:
            expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")
            return
 
        expense = {'category': category, 'amount': amount, 'date': expense_date}
        self.expenses.append(expense)
 
        self.update_expenses_listbox()
        self.clear_entry_fields()
 
    def plot_expenses(self):
        categories = [expense['category'] for expense in self.expenses]
        amounts = [expense['amount'] for expense in self.expenses]
 
        plt.bar(categories, amounts)
        plt.xlabel('Expense Categories')
        plt.ylabel('Amount ($)')
        plt.title('Monthly Expenses')
 
        # Display the plot in a new window
        plt.show()
 
    def calculate_total(self):
        total_expenses = sum(expense['amount'] for expense in self.expenses)
        self.label_total.config(text=f"Total Expenses: ${total_expenses:.2f}")
 
    def clear_entry_fields(self):
        self.entry_category.set(self.categories[0])
        self.entry_amount.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
 
    def save_expenses(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Category', 'Amount', 'Date'])
                    for expense in self.expenses:
                        writer.writerow([expense['category'], expense['amount'], expense['date']])
                messagebox.showinfo("Save Successful", "Expenses saved successfully.")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving expenses:\n{str(e)}")
 
    def load_expenses(self):
        filename = tk.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, 'r') as file:
                    reader = csv.reader(file)
                    header = next(reader)  # Skip the header row
                    self.expenses = [{'category': row[0], 'amount': float(row[1]), 'date': row[2]} for row in reader]
                self.update_expenses_listbox()
                messagebox.showinfo("Load Successful", "Expenses loaded successfully.")
            except Exception as e:
                messagebox.showerror("Load Error", f"An error occurred while loading expenses:\n{str(e)}")
 
    def update_expenses_listbox(self):
        self.listbox_expenses.delete(0, tk.END)
        for expense in self.expenses:
            self.listbox_expenses.insert(tk.END, f"{expense['category']}: ${expense['amount']} ({expense['date']})")
 
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
