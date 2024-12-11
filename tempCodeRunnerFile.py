import tkinter as tk
from tkinter import filedialog, Text
from bs4 import BeautifulSoup
import json

def load_file(file_var):
    filepath = filedialog.askopenfilename(filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
    file_var.set(filepath)

def extract_content(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, 'html.parser')
    title = soup.title.string if soup.title else None
    meta_description = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_description["content"] if meta_description else None
    return title, meta_description

def compare_html():
    filepath1 = file1_var.get()
    filepath2 = file2_var.get()
    
    title1, meta_description1 = extract_content(filepath1)
    title2, meta_description2 = extract_content(filepath2)
    
    differences = {
        "title": {
            "html1.html": title1,
            "html2.html": title2
        },
        "meta": {
            "description": {
                "html1.html": meta_description1,
                "html2.html": meta_description2
            }
        }
    }
    
    json_output = json.dumps(differences, indent=4)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, json_output)

def save_json():
    json_output = text_output.get(1.0, tk.END)
    save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    with open(save_path, "w", encoding="utf-8") as file:
        file.write(json_output)

# Set up the GUI
root = tk.Tk()
root.title("HTML Comparator")

file1_var = tk.StringVar()
file2_var = tk.StringVar()

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="HTML File 1:").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(frame, textvariable=file1_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(frame, text="Browse", command=lambda: load_file(file1_var)).grid(row=0, column=2, padx=10, pady=5)

tk.Label(frame, text="HTML File 2:").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(frame, textvariable=file2_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(frame, text="Browse", command=lambda: load_file(file2_var)).grid(row=1, column=2, padx=10, pady=5)

tk.Button(frame, text="Compare", command=compare_html).grid(row=2, column=0, columnspan=3, pady=10)

text_output = Text(root, width=100, height=20)
text_output.pack(pady=20)

tk.Button(root, text="Save JSON", command=save_json).pack(pady=10)

root.mainloop()
