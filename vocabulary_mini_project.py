code = r'''import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ============================================================
# DATABASE
# ============================================================

connection = sqlite3.connect("vocabulary.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT UNIQUE,
    meaning TEXT
)
""")
connection.commit()


# ============================================================
# COLORS
# ============================================================

BG = "#0B1220"
CARD = "#111C2E"
CARD_2 = "#16243A"
BORDER = "#263852"
BLUE = "#3B82F6"
BLUE_HOVER = "#2563EB"
GREEN = "#22C55E"
GREEN_HOVER = "#16A34A"
RED = "#EF4444"
RED_HOVER = "#DC2626"
GRAY = "#94A3B8"
LIGHT = "#E2E8F0"
WHITE = "#FFFFFF"
ENTRY_BG = "#0F1A2B"


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()
window.title("Vocabulary Builder")
window.geometry("1050x760")
window.minsize(950, 680)
window.configure(bg=BG)


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=CARD_2,
    foreground=LIGHT,
    fieldbackground=CARD_2,
    rowheight=38,
    borderwidth=0,
    font=("Segoe UI", 11)
)

style.configure(
    "Treeview.Heading",
    background="#1D3150",
    foreground=WHITE,
    font=("Segoe UI", 11, "bold"),
    padding=10,
    relief="flat"
)

style.map(
    "Treeview",
    background=[("selected", "#2455A4")],
    foreground=[("selected", WHITE)]
)

style.configure(
    "Vertical.TScrollbar",
    background="#243650",
    troughcolor=CARD,
    bordercolor=CARD,
    arrowcolor=LIGHT
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def make_button(parent, text, command, bg, hover, width=13):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        height=1,
        font=("Segoe UI", 10, "bold"),
        bg=bg,
        fg=WHITE,
        activebackground=hover,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=10,
        pady=8
    )

    button.bind("<Enter>", lambda event: button.config(bg=hover))
    button.bind("<Leave>", lambda event: button.config(bg=bg))

    return button


def clear_inputs():
    word_entry.delete(0, tk.END)
    meaning_entry.delete(0, tk.END)
    word_entry.focus()
    word_table.selection_remove(word_table.selection())


def update_count():
    count_label.config(text=f"{len(words)} words")


# ============================================================
# WORD DATA
# ============================================================

words = []

cursor.execute("SELECT word, meaning FROM words ORDER BY word COLLATE NOCASE")
saved_words = cursor.fetchall()

for word, meaning in saved_words:
    words.append((word, meaning))


# ============================================================
# DISPLAY WORDS
# ============================================================

def display_words():
    for item in word_table.get_children():
        word_table.delete(item)

    for word, meaning in words:
        word_table.insert("", tk.END, values=(word, meaning))

    update_count()


# ============================================================
# SEARCH
# ============================================================

def search_word():
    search_text = search_entry.get().strip().lower()

    if search_text == "":
        display_words()
        return

    for item in word_table.get_children():
        word_table.delete(item)

    found = False

    for word, meaning in words:
        if search_text in word.lower() or search_text in meaning.lower():
            word_table.insert("", tk.END, values=(word, meaning))
            found = True

    if not found:
        messagebox.showinfo(
            "Search",
            "No matching word or meaning found."
        )


def show_all_words():
    search_entry.delete(0, tk.END)
    display_words()


# ============================================================
# ADD WORD
# ============================================================

def add_word():
    word = word_entry.get().strip()
    meaning = meaning_entry.get().strip()

    if word == "" or meaning == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter both the word and its meaning."
        )
        return

    for existing_word, existing_meaning in words:
        if existing_word.lower() == word.lower():
            messagebox.showwarning(
                "Duplicate Word",
                "This word already exists."
            )
            return

    words.append((word, meaning))

    cursor.execute(
        "INSERT INTO words (word, meaning) VALUES (?, ?)",
        (word, meaning)
    )
    connection.commit()

    display_words()
    clear_inputs()

    messagebox.showinfo(
        "Success",
        f'"{word}" was added successfully.'
    )


# ============================================================
# SELECT WORD
# ============================================================

def select_word(event=None):
    selected_item = word_table.selection()

    if not selected_item:
        return

    item = word_table.item(selected_item[0])
    values = item["values"]

    word_entry.delete(0, tk.END)
    word_entry.insert(0, values[0])

    meaning_entry.delete(0, tk.END)
    meaning_entry.insert(0, values[1])


# ============================================================
# EDIT WORD
# ============================================================

def edit_word():
    selected_item = word_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Selection",
            "Select a word from the table first."
        )
        return

    new_word = word_entry.get().strip()
    new_meaning = meaning_entry.get().strip()

    if new_word == "" or new_meaning == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter both the word and its meaning."
        )
        return

    item = word_table.item(selected_item[0])
    old_word = item["values"][0]

    for existing_word, existing_meaning in words:
        if (
            existing_word.lower() == new_word.lower()
            and existing_word.lower() != old_word.lower()
        ):
            messagebox.showwarning(
                "Duplicate Word",
                "Another word with this name already exists."
            )
            return

    for i in range(len(words)):
        if words[i][0].lower() == old_word.lower():
            words[i] = (new_word, new_meaning)
            break

    cursor.execute(
        """
        UPDATE words
        SET word = ?, meaning = ?
        WHERE word = ?
        """,
        (new_word, new_meaning, old_word)
    )
    connection.commit()

    display_words()
    clear_inputs()

    messagebox.showinfo(
        "Success",
        f'"{new_word}" was updated successfully.'
    )


# ============================================================
# DELETE WORD
# ============================================================

def delete_word():
    selected_item = word_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Selection",
            "Select a word from the table first."
        )
        return

    item = word_table.item(selected_item[0])
    word_to_delete = item["values"][0]

    confirm = messagebox.askyesno(
        "Delete Word",
        f'Are you sure you want to delete "{word_to_delete}"?'
    )

    if not confirm:
        return

    for i in range(len(words)):
        if words[i][0].lower() == word_to_delete.lower():
            words.pop(i)
            break

    cursor.execute(
        "DELETE FROM words WHERE word = ?",
        (word_to_delete,)
    )
    connection.commit()

    display_words()
    clear_inputs()

    messagebox.showinfo(
        "Deleted",
        f'"{word_to_delete}" was deleted.'
    )


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(window, bg=BG)
header.pack(fill="x", padx=35, pady=(28, 10))

title_area = tk.Frame(header, bg=BG)
title_area.pack(side="left")

tk.Label(
    title_area,
    text="MY VOCABULARY",
    font=("Segoe UI", 25, "bold"),
    bg=BG,
    fg=WHITE
).pack(anchor="w")

tk.Label(
    title_area,
    text="Build, search and manage your personal word collection",
    font=("Segoe UI", 10),
    bg=BG,
    fg=GRAY
).pack(anchor="w", pady=(3, 0))

count_label = tk.Label(
    header,
    text="0 words",
    font=("Segoe UI", 11, "bold"),
    bg=CARD_2,
    fg=LIGHT,
    padx=18,
    pady=9
)
count_label.pack(side="right")


# ============================================================
# INPUT CARD
# ============================================================

input_card = tk.Frame(
    window,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)
input_card.pack(fill="x", padx=35, pady=10)

tk.Label(
    input_card,
    text="ADD / EDIT WORD",
    font=("Segoe UI", 11, "bold"),
    bg=CARD,
    fg=BLUE
).grid(row=0, column=0, columnspan=4, sticky="w", padx=22, pady=(18, 12))

tk.Label(
    input_card,
    text="Word",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=LIGHT
).grid(row=1, column=0, sticky="w", padx=(22, 8), pady=8)

word_entry = tk.Entry(
    input_card,
    font=("Segoe UI", 11),
    bg=ENTRY_BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    bd=0
)
word_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=8,
    pady=8,
    ipady=8
)

tk.Label(
    input_card,
    text="Meaning",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=LIGHT
).grid(row=2, column=0, sticky="w", padx=(22, 8), pady=(4, 18))

meaning_entry = tk.Entry(
    input_card,
    font=("Segoe UI", 11),
    bg=ENTRY_BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    bd=0
)
meaning_entry.grid(
    row=2,
    column=1,
    sticky="ew",
    padx=8,
    pady=(4, 18),
    ipady=8
)

input_card.grid_columnconfigure(1, weight=1)

add_button = make_button(
    input_card, "＋  Add Word", add_word, BLUE, BLUE_HOVER, 14
)
add_button.grid(row=1, column=2, padx=8, pady=8)

edit_button = make_button(
    input_card, "✎  Edit", edit_word, GREEN, GREEN_HOVER, 12
)
edit_button.grid(row=2, column=2, padx=8, pady=(4, 18))

delete_button = make_button(
    input_card, "Delete", delete_word, RED, RED_HOVER, 12
)
delete_button.grid(row=1, column=3, padx=(8, 22), pady=8)

clear_button = make_button(
    input_card, "Clear", clear_inputs, "#475569", "#334155", 12
)
clear_button.grid(row=2, column=3, padx=(8, 22), pady=(4, 18))


# ============================================================
# SEARCH CARD
# ============================================================

search_card = tk.Frame(
    window,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)
search_card.pack(fill="x", padx=35, pady=(2, 10))

tk.Label(
    search_card,
    text="SEARCH",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=BLUE
).pack(side="left", padx=(18, 10), pady=13)

search_entry = tk.Entry(
    search_card,
    font=("Segoe UI", 11),
    bg=ENTRY_BG,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    bd=0
)
search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5,
    pady=8,
    ipady=7
)

make_button(
    search_card, "Search", search_word, BLUE, BLUE_HOVER, 11
).pack(side="left", padx=6, pady=7)

make_button(
    search_card, "Show All", show_all_words, "#475569", "#334155", 11
).pack(side="left", padx=(0, 15), pady=7)


# ============================================================
# TABLE CARD
# ============================================================

table_card = tk.Frame(
    window,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)
table_card.pack(fill="both", expand=True, padx=35, pady=(0, 25))

tk.Label(
    table_card,
    text="YOUR WORDS",
    font=("Segoe UI", 11, "bold"),
    bg=CARD,
    fg=BLUE
).pack(anchor="w", padx=18, pady=(15, 8))

table_area = tk.Frame(table_card, bg=CARD)
table_area.pack(fill="both", expand=True, padx=15, pady=(0, 15))

word_table = ttk.Treeview(
    table_area,
    columns=("Word", "Meaning"),
    show="headings",
    selectmode="browse"
)

word_table.heading("Word", text="WORD")
word_table.heading("Meaning", text="MEANING")

word_table.column("Word", width=250, anchor="w")
word_table.column("Meaning", width=650, anchor="w")

scrollbar = ttk.Scrollbar(
    table_area,
    orient="vertical",
    command=word_table.yview,
    style="Vertical.TScrollbar"
)

word_table.configure(yscrollcommand=scrollbar.set)

word_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# ============================================================
# KEYBOARD SHORTCUTS
# ============================================================

search_entry.bind("<Return>", lambda event: search_word())
word_entry.bind("<Return>", lambda event: add_word())
meaning_entry.bind("<Return>", lambda event: add_word())
word_table.bind("<<TreeviewSelect>>", select_word)


# ============================================================
# CLOSE APPLICATION
# ============================================================

def close_app():
    connection.close()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", close_app)


# ============================================================
# START APPLICATION
# ============================================================

display_words()
word_entry.focus()
window.mainloop()
'''

path = "/mnt/data/Vocabulary_Builder_Professional.py"
with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print(path)
