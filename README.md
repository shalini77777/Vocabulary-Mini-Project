# 📚 Vocabulary Builder

A desktop Vocabulary Builder application developed using **Python, Tkinter, and SQLite**.

This application allows users to create and manage their personal vocabulary collection through a simple and professional graphical user interface.

---

## ✨ Features

- ➕ Add new words and meanings
- ✏️ Edit existing vocabulary
- 🗑️ Delete words
- 🔍 Search for words
- 🔎 Search using both words and meanings
- 📋 Display all saved vocabulary
- 🖱️ Select a word directly from the table
- 💾 Store vocabulary permanently using SQLite
- 📊 Display the total number of saved words
- 🎨 Professional dark-themed GUI
- 🖱️ Interactive buttons with hover effects
- ⌨️ Keyboard shortcuts for easier interaction
- ⚠️ Input validation and confirmation messages

---

## 🖥️ Application Interface

The application provides a dashboard-style interface for managing vocabulary.

### Add / Edit Word

Users can enter a word and its meaning. Existing words can also be selected from the table and edited.

### Search

Users can search for a word or meaning using the search bar.

### Vocabulary Table

All saved words and their meanings are displayed in an organized table.

### Word Management

Users can add, edit, delete, and clear vocabulary entries using the available buttons.

---

## 🛠️ Technologies Used

- **Python** – Programming language
- **Tkinter** – Graphical User Interface
- **SQLite** – Database management
- **Git** – Version control
- **GitHub** – Source code hosting

---

## 📂 Project Structure

```text
Vocabulary-Mini-Project/
│
├── vocabulary_mini_project.py
├── README.md
└── .gitignore
````

The `vocabulary.db` database file is created automatically when the application is run and is not included in the repository.

---

## ⚙️ Requirements

Python 3.x is required.

The project uses Python's built-in libraries:

* `tkinter`
* `sqlite3`

No external Python packages are required.

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/shalini77777/Vocabulary-Mini-Project.git
```

### 2. Open the Project Folder

```bash
cd Vocabulary-Mini-Project
```

### 3. Run the Application

```bash
python vocabulary_mini_project.py
```

The application will open automatically.

The SQLite database will be created automatically when the application is run.

---

## 📖 How to Use

### ➕ Add a Word

1. Enter a word in the **Word** field.
2. Enter its meaning in the **Meaning** field.
3. Click **Add Word**.
4. The word will be added to the vocabulary table.
5. The word and meaning will be saved in the SQLite database.

### 🔍 Search

1. Enter a word or meaning in the search box.
2. Click **Search**.
3. Matching entries will be displayed.
4. Click **Show All** to display all vocabulary entries again.

### ✏️ Edit a Word

1. Select a word from the vocabulary table.
2. The word and meaning will appear in the input fields.
3. Modify the required information.
4. Click **Edit**.
5. The changes will be saved to the database.

### 🗑️ Delete a Word

1. Select a word from the vocabulary table.
2. Click **Delete**.
3. Confirm the deletion.
4. The word will be removed from the application and database.

### 🧹 Clear

Click **Clear** to remove the current input and table selection.

---

## 🗄️ Database

The application uses **SQLite** to store vocabulary data permanently.

The database contains a `words` table with the following columns:

| Column    | Description             |
| --------- | ----------------------- |
| `id`      | Unique ID for each word |
| `word`    | Vocabulary word         |
| `meaning` | Meaning of the word     |

The database is created automatically when the application is first run.

---

## 🧠 What I Learned

Through this project, I practiced:

* Python GUI development using Tkinter
* Creating and configuring GUI widgets
* Using frames to organize a GUI
* Using `pack()` and `grid()` for layout management
* Creating labels, buttons, entry fields, and tables
* Using `ttk.Treeview`
* Handling button events with functions
* Searching and filtering data
* Adding, editing, and deleting records
* Connecting Python applications with SQLite
* Executing SQL queries from Python
* Using parameterized SQL queries
* Managing application data using Python lists
* Input validation
* Using message boxes for warnings and confirmations
* Creating a professional dark-themed GUI
* Using Git for version control
* Uploading and managing projects on GitHub

---

## 🔮 Future Improvements

Possible future improvements include:

* 📌 Add vocabulary categories
* 📅 Add the date when a word was added
* ⭐ Add favorite words
* 🔊 Add pronunciation support
* 📈 Add vocabulary learning statistics
* 🧠 Add a vocabulary quiz mode
* 🌐 Add translation support
* 📤 Export vocabulary to CSV or Excel
* 🔐 Add user login and multiple vocabulary profiles

---

## 👩‍💻 Author

**R V Shalini**

B.Tech Information Technology

---

## 📄 License

This project is created for learning and educational purposes.



