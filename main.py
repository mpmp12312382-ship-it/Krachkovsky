import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

def load_data():
    if os.path.exists("movies.json"):
        with open("movies.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data():
    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

def add_movie():
    title = title_entry.get().strip()
    if not title:
        messagebox.showerror("Ошибка", "Введите название фильма")
        return
    
    genre = genre_combo.get()
    if not genre:
        messagebox.showerror("Ошибка", "Выберите жанр")
        return
    
    try:
        year = int(year_entry.get())
        if year < 1888 or year > 2026:
            messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2026")
            return
    except ValueError:
        messagebox.showerror("Ошибка", "Год должен быть числом")
        return
    
    try:
        rating = float(rating_entry.get())
        if rating < 0 or rating > 10:
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
            return
    except ValueError:
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
        return
    
    movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
    save_data()
    refresh_table()
    title_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    
    filtered = movies[:]
    
    if filter_genre.get():
        filtered = [m for m in filtered if m["genre"] == filter_genre.get()]
    
    if filter_year.get():
        try:
            filter_year_val = int(filter_year.get())
            filtered = [m for m in filtered if m["year"] == filter_year_val]
        except:
            pass
    
    for movie in filtered:
        tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

def apply_filters():
    refresh_table()

def clear_filters():
    filter_genre.set("")
    filter_year.delete(0, tk.END)
    refresh_table()

movies = load_data()

root = tk.Tk()
root.title("Movie Library - Крачковский Илья Андреевич")
root.geometry("850x550")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(main_frame, text="Название фильма:").grid(row=0, column=0, sticky=tk.W, pady=5)
title_entry = ttk.Entry(main_frame, width=30)
title_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(main_frame, text="Жанр:").grid(row=1, column=0, sticky=tk.W, pady=5)
genre_combo = ttk.Combobox(main_frame, values=["боевик", "комедия", "драма", "фантастика", "ужасы", "триллер", "мелодрама", "документальный"], width=28)
genre_combo.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(main_frame, text="Год выпуска:").grid(row=2, column=0, sticky=tk.W, pady=5)
year_entry = ttk.Entry(main_frame, width=30)
year_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(main_frame, text="Рейтинг (0-10):").grid(row=3, column=0, sticky=tk.W, pady=5)
rating_entry = ttk.Entry(main_frame, width=30)
rating_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = ttk.Button(main_frame, text="Добавить фильм", command=add_movie)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

ttk.Separator(main_frame, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)

ttk.Label(main_frame, text="Фильтрация", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=2, pady=5)

ttk.Label(main_frame, text="Фильтр по жанру:").grid(row=7, column=0, sticky=tk.W, pady=5)
filter_genre = ttk.Combobox(main_frame, values=[""] + ["боевик", "комедия", "драма", "фантастика", "ужасы", "триллер", "мелодрама", "документальный"], width=28)
filter_genre.grid(row=7, column=1, padx=5, pady=5)
filter_genre.set("")

ttk.Label(main_frame, text="Фильтр по году:").grid(row=8, column=0, sticky=tk.W, pady=5)
filter_year = ttk.Entry(main_frame, width=30)
filter_year.grid(row=8, column=1, padx=5, pady=5)

button_frame = ttk.Frame(main_frame)
button_frame.grid(row=9, column=0, columnspan=2, pady=10)

apply_button = ttk.Button(button_frame, text="Применить фильтры", command=apply_filters)
apply_button.pack(side=tk.LEFT, padx=5)

clear_button = ttk.Button(button_frame, text="Сбросить фильтры", command=clear_filters)
clear_button.pack(side=tk.LEFT, padx=5)

ttk.Separator(main_frame, orient="horizontal").grid(row=10, column=0, columnspan=2, sticky="ew", pady=10)

columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
tree.grid(row=11, column=0, columnspan=2, pady=10)

for col in columns:
    tree.heading(col, text=col)
    if col == "Название":
        tree.column(col, width=250)
    elif col == "Жанр":
        tree.column(col, width=120)
    elif col == "Год":
        tree.column(col, width=80)
    elif col == "Рейтинг":
        tree.column(col, width=80)

refresh_table()
root.mainloop()
