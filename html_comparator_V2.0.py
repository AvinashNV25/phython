import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import html_to_json
import json
from jsondiff import diff
import threading

old_json = {}
new_json = {}
json_diff = {}

def open_file(entry, label, json_storage):
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                entry.delete("1.0", tk.END)
                entry.insert(tk.END, content)
                label.config(text=f"File: {file_path}")
                json_storage.clear()
                json_storage.update(html_to_json.convert(content))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")

def save_json(json_data, file_type):
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")], initialfile=f"{file_type}_json.json")
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4)
            messagebox.showinfo("Success", f"{file_type} JSON saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save {file_type} JSON: {e}")

def compare_json():
    global json_diff
    if old_json and new_json:
        try:
            json_diff = diff(old_json, new_json)
            diff_text.delete("1.0", tk.END)
            for key in json_diff.keys():
                diff_text.insert(tk.END, f"{key}: {json_diff[key]}\n", "highlight")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare JSON: {e}")

def highlight_diff():
    try:
        diff_text.tag_remove("highlight", "1.0", tk.END)
        for line_num, line in enumerate(diff_text.get("1.0", tk.END).splitlines(), 1):
            if '"differ": true' in line:
                diff_text.tag_add("highlight", f"{line_num}.0", f"{line_num}.end")
        diff_text.tag_configure("highlight", background="yellow")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to highlight differences: {e}")

def save_comparison():
    comparison_result = diff_text.get("1.0", tk.END).strip()
    if comparison_result:
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")], initialfile="comparison_result.json")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(comparison_result)
                messagebox.showinfo("Success", "Comparison result saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save comparison result: {e}")

def start_compare_thread():
    comparison_thread = threading.Thread(target=compare_json)
    comparison_thread.start()

# Initialize GUI window
window = tk.Tk()
window.title("HTML to JSON Converter and Comparator")
window.state('zoomed')
window.configure(bg="#f0f0f0")

# Styles
label_font = ("Arial", 12, "bold")
button_font = ("Arial", 10, "bold")
text_bg = "#e0e0e0"
text_font = ("Courier", 10)

# Define text areas for HTML input and JSON output
old_html_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg=text_bg, font=text_font)
old_html_text.grid(row=3, column=0)
old_html_text.grid_remove()

new_html_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg=text_bg, font=text_font)
new_html_text.grid(row=3, column=1)
new_html_text.grid_remove()

# Labels to display file names
old_file_label = tk.Label(window, text="Old HTML File: None", font=label_font, bg="#f0f0f0")
old_file_label.grid(row=1, column=0, padx=10, pady=5)

new_file_label = tk.Label(window, text="New HTML File: None", font=label_font, bg="#f0f0f0")
new_file_label.grid(row=1, column=1, padx=10, pady=5)

# Buttons for uploading HTML and conversion
tk.Button(window, text="Upload Old HTML", font=button_font, bg="#4caf50", fg="white", command=lambda: open_file(old_html_text, old_file_label, old_json)).grid(row=0, column=0, padx=10, pady=5)
tk.Button(window, text="Upload New HTML", font=button_font, bg="#4caf50", fg="white", command=lambda: open_file(new_html_text, new_file_label, new_json)).grid(row=0, column=1, padx=10, pady=5)
tk.Button(window, text="Compare JSON", font=button_font, bg="#ff9800", fg="white", command=start_compare_thread).grid(row=0, column=2, padx=10, pady=5)
tk.Button(window, text="Highlight Differences", font=button_font, bg="#ff5722", fg="white", command=highlight_diff).grid(row=0, column=3, padx=10, pady=5)
tk.Button(window, text="Save Comparison Result", font=button_font, bg="#9c27b0", fg="white", command=save_comparison).grid(row=0, column=4, padx=10, pady=5)

# Differences output
tk.Label(window, text="Differences", font=label_font, bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, columnspan=5)
diff_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg=text_bg, font=text_font)
diff_text.grid(row=3, column=0, columnspan=5, padx=10, pady=5, sticky="nsew")

# Configure grid weights to make JSON outputs expand
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)
window.grid_columnconfigure(4, weight=1)

# Highlighting style (use tag_configure here)
diff_text.tag_configure("highlight", background="yellow")

# Run the GUI loop
window.mainloop()
