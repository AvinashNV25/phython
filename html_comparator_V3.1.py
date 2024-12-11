import tkinter as tk
from tkinter import filedialog, Text, messagebox
from tkinter.ttk import Style, Button, Frame, Label, Entry
from bs4 import BeautifulSoup
import json

def load_file(file_var):
    filepath = filedialog.askopenfilename(filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
    file_var.set(filepath)

def extract_content(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup

def compare_elements(elem1, elem2, path=""):
    differences = {}

    if elem1.name != elem2.name:
        differences[path + "tag"] = {"old value": elem1.name, "new value": elem2.name}

    attrs1 = elem1.attrs if elem1 else {}
    attrs2 = elem2.attrs if elem2 else {}
    all_keys = set(attrs1.keys()).union(set(attrs2.keys()))

    for key in all_keys:
        val1 = attrs1.get(key)
        val2 = attrs2.get(key)
        if val1 != val2:
            if path + key not in differences:
                differences[path + key] = {"old value": val1, "new value": val2}
            else:
                differences[path + key]["old value"] = val1
                differences[path + key]["new value"] = val2

    if elem1.string != elem2.string:
        differences[path + "string"] = {"old value": elem1.string, "new value": elem2.string}

    return differences

def compare_html():
    filepath1 = file1_var.get()
    filepath2 = file2_var.get()
    print(filepath1)
    if not filepath1 or not filepath2:
        messagebox.showerror("Error", "Please select both files to compare.")
        return
    
    soup1 = extract_content(filepath1)
    soup2 = extract_content(filepath2)

    differences = compare_recursive(soup1, soup2)
    print(soup1)
    print("=======================================================================================================")
    print(soup2)
    json_output = json.dumps(differences, indent=4)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, json_output)

def compare_recursive(soup1, soup2, path=""):
    differences = {}

    if soup1.name != soup2.name:
        differences["tag"] = {"old value": soup1.name, "new value": soup2.name}

    attrs1 = soup1.attrs if soup1 else {}
    attrs2 = soup2.attrs if soup2 else {}
    all_keys = set(attrs1.keys()).union(set(attrs2.keys()))

    for key in all_keys:
        val1 = attrs1.get(key)
        val2 = attrs2.get(key)
        if val1 != val2:
            if key not in differences:
                differences[key] = {"old value": val1, "new value": val2}
            else:
                differences[key]["old value"] = val1
                differences[key]["new value"] = val2

    if soup1.string != soup2.string:
        differences["string"] = {"old value": soup1.string, "new value": soup2.string}

    children1 = list(soup1.children)
    children2 = list(soup2.children)

    for i, (child1, child2) in enumerate(zip(children1, children2)):
        if child1.name and child2.name:
            child_diffs = compare_recursive(child1, child2, path + f"{child1.name}[{i}]/")
            differences.update({f"{child1.name}[{i}]" + '/' + k: v for k, v in child_diffs.items()})

    return differences


def save_json():
    json_output = text_output.get(1.0, tk.END)
    if not json_output.strip():
        messagebox.showerror("Error", "No JSON output to save.")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if save_path:
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(json_output)
        messagebox.showinfo("Saved", "JSON output saved successfully!")

# Set up the GUI
root = tk.Tk()
root.title("HTML Comparator by aviworld")
root.state('zoomed')

# Light theme colors
background_color = "#F0F0F0"
text_color = "#000000"
button_color = "#E0E0E0"
entry_background = "#FFFFFF"
entry_foreground = "#000000"

root.configure(bg=background_color)

style = Style()
style.configure('TButton', background=button_color, foreground=text_color, font=('Helvetica', 10))
style.configure('TFrame', background=background_color)
style.configure('TLabel', background=background_color, foreground=text_color, font=('Helvetica', 12))
style.configure('TEntry', fieldbackground=entry_background, foreground=entry_foreground, font=('Helvetica', 10))

file1_var = tk.StringVar()
file2_var = tk.StringVar()

frame = Frame(root)
frame.pack(pady=20, padx=20, fill=tk.X, expand=True)

Label(frame, text="Old HTML File:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
Entry(frame, textvariable=file1_var, width=50).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
Button(frame, text="Browse", command=lambda: load_file(file1_var)).grid(row=0, column=2, padx=10, pady=5)

Label(frame, text="New HTML File:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
Entry(frame, textvariable=file2_var, width=50).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
Button(frame, text="Browse", command=lambda: load_file(file2_var)).grid(row=1, column=2, padx=10, pady=5)

Button(frame, text="Compare", command=compare_html).grid(row=2, column=0, columnspan=3, pady=10)

text_output = Text(root, width=100, height=20, bg=entry_background, fg=entry_foreground, insertbackground='black')
text_output.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

Button(root, text="Save JSON", command=save_json).pack(pady=10)

# Display the creator name
Label(root, text="Created by aviworld", font=('Helvetica', 10, 'italic')).pack(side=tk.BOTTOM, pady=5)

root.mainloop()
