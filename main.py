import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

def load_data():
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data():
    with open("expenses.json", "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)

def add_expense():
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
            return
        category = category_combo.get()
        if not category:
            messagebox.showerror("Ошибка", "Выберите категорию")
            return
        date = date_entry.get()
        datetime.strptime(date, "%Y-%m-%d")
        expenses.append({"amount": amount, "category": category, "date": date})
        save_data()
        refresh_table()
        amount_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Ошибка", "Неверный формат даты (используйте ГГГГ-ММ-ДД) или суммы")

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    filtered = expenses[:]
    if filter_category.get():
        filtered = [e for e in filtered if e["category"] == filter_category.get()]
    if filter_date.get():
        try:
            filter_date_val = filter_date.get()
            filtered = [e for e in filtered if e["date"] == filter_date_val]
        except:
            pass
    for exp in filtered:
        tree.insert("", tk.END, values=(exp["amount"], exp["category"], exp["date"]))
    calculate_sum()

def calculate_sum():
    try:
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        if start_date and end_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            total = sum(e["amount"] for e in expenses if start <= datetime.strptime(e["date"], "%Y-%m-%d") <= end)
            sum_label.config(text=f"Сумма за период: {total:.2f}")
        else:
            sum_label.config(text="Сумма за период: 0.00")
    except:
        sum_label.config(text="Ошибка формата дат")

def apply_filters():
    refresh_table()

expenses = load_data()

root = tk.Tk()
root.title("Expense Tracker - Крачковский Илья Андреевич")
root.geometry("800x500")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(main_frame, text="Сумма:").grid(row=0, column=0, sticky=tk.W)
amount_entry = ttk.Entry(main_frame, width=20)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(main_frame, text="Категория:").grid(row=1, column=0, sticky=tk.W)
category_combo = ttk.Combobox(main_frame, values=["еда", "транспорт", "развлечения", "коммунальные", "здоровье"], width=18)
category_combo.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(main_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky=tk.W)
date_entry = ttk.Entry(main_frame, width=20)
date_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = ttk.Button(main_frame, text="Добавить расход", command=add_expense)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

ttk.Label(main_frame, text="Фильтр по категории:").grid(row=4, column=0, sticky=tk.W)
filter_category = ttk.Combobox(main_frame, values=[""] + ["еда", "транспорт", "развлечения", "коммунальные", "здоровье"], width=18)
filter_category.grid(row=4, column=1, padx=5, pady=5)
filter_category.set("")

ttk.Label(main_frame, text="Фильтр по дате:").grid(row=5, column=0, sticky=tk.W)
filter_date = ttk.Entry(main_frame, width=20)
filter_date.grid(row=5, column=1, padx=5, pady=5)

ttk.Label(main_frame, text="Период (начало):").grid(row=6, column=0, sticky=tk.W)
start_date_entry = ttk.Entry(main_frame, width=20)
start_date_entry.grid(row=6, column=1, padx=5, pady=5)

ttk.Label(main_frame, text="Период (конец):").grid(row=7, column=0, sticky=tk.W)
end_date_entry = ttk.Entry(main_frame, width=20)
end_date_entry.grid(row=7, column=1, padx=5, pady=5)

apply_button = ttk.Button(main_frame, text="Применить фильтры", command=apply_filters)
apply_button.grid(row=8, column=0, columnspan=2, pady=5)

sum_label = ttk.Label(main_frame, text="Сумма за период: 0.00", font=("Arial", 10, "bold"))
sum_label.grid(row=9, column=0, columnspan=2, pady=10)

columns = ("Сумма", "Категория", "Дата")
tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
tree.grid(row=10, column=0, columnspan=2, pady=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

refresh_table()
root.mainloop()
