import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from bs4 import BeautifulSoup
import json
import threading

class HTMLComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Comparator")
        self.root.state('zoomed')

        self.create_gui_elements()
        self.old_file = None
        self.new_file = None

    def create_gui_elements(self):
        tk.Label(self.root, text="Upload HTML files and compare", font=("Arial", 24)).pack(pady=20)

        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=20)

        self.old_filename_label = tk.Label(file_frame, text="Old File: None", font=("Arial", 18))
        self.old_filename_label.pack(side=tk.LEFT, padx=20)

        tk.Button(file_frame, text="Upload Old HTML", command=self.upload_old_file, bg="#4CAF50", fg="white", font=("Arial", 14)).pack(side=tk.LEFT, padx=20)

        self.new_filename_label = tk.Label(file_frame, text="New File: None", font=("Arial", 18))
        self.new_filename_label.pack(side=tk.LEFT, padx=20)

        tk.Button(file_frame, text="Upload New HTML", command=self.upload_new_file, bg="#008CBA", fg="white", font=("Arial", 14)).pack(side=tk.LEFT, padx=20)

        self.compare_button = tk.Button(self.root, text="Compare", command=self.compare_files, bg="#f44336", fg="white", font=("Arial", 18))
        self.compare_button.pack(pady=20)

        self.save_button = tk.Button(self.root, text="Save Results", command=self.save_results, bg="#2196F3", fg="white", state=tk.DISABLED, font=("Arial", 18))
        self.save_button.pack(pady=20)

        self.result_text = scrolledtext.ScrolledText(self.root, height=20, width=100, wrap=tk.WORD, font=("Arial", 14))
        self.result_text.pack(pady=20)

    def upload_old_file(self):
        self.old_file = self.get_file_from_dialog()
        if self.old_file:
            self.old_filename_label.config(text=f"Old File: {self.get_filename_from_path(self.old_file)}")
            self.check_files_uploaded()

    def upload_new_file(self):
        self.new_file = self.get_file_from_dialog()
        if self.new_file:
            self.new_filename_label.config(text=f"New File: {self.get_filename_from_path(self.new_file)}")
            self.check_files_uploaded()

    def get_file_from_dialog(self):
        return filedialog.askopenfilename(initialdir="/", title="Select HTML File", filetypes=[("HTML files", "*.html"), ("All files", "*.*")])

    def get_filename_from_path(self, filepath):
        return filepath.split("/")[-1]

    def check_files_uploaded(self):
        self.compare_button.config(state=tk.NORMAL if self.old_file and self.new_file else tk.DISABLED)

    def compare_files(self):
        if self.old_file and self.new_file:
            self.compare_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
            threading.Thread(target=self.perform_comparison).start()

    def perform_comparison(self):
        old_content = self.load_file_content(self.old_file)
        new_content = self.load_file_content(self.new_file)

        old_soup = BeautifulSoup(old_content, "html.parser")
        new_soup = BeautifulSoup(new_content, "html.parser")

        old_elements = self.extract_elements(old_soup)
        new_elements = self.extract_elements(new_soup)

        changes = self.find_changes(old_elements, new_elements)

        self.root.after(0, self.display_results, changes)

    def extract_elements(self, soup):
        elements = []
        for elem in soup.descendants:
            if elem.name:
                elements.append({
                    "tag": elem.name,
                    "attributes": dict(elem.attrs),
                    "text": elem.get_text(strip=True)
                })
        return elements

    def find_changes(self, old_elements, new_elements):
        changes = []
        max_len = max(len(old_elements), len(new_elements))

        for i in range(max_len):
            old_elem = old_elements[i] if i < len(old_elements) else None
            new_elem = new_elements[i] if i < len(new_elements) else None

            if old_elem and new_elem:
                if old_elem["tag"] != new_elem["tag"]:
                    changes.append({
                        "index": i,
                        "type": "Tag Change",
                        "old_tag": old_elem["tag"],
                        "new_tag": new_elem["tag"],
                        "reason": "Tag name changed"
                    })

                old_attrs = old_elem["attributes"]
                new_attrs = new_elem["attributes"]

                if old_attrs != new_attrs:
                    changes.append({
                        "index": i,
                        "type": "Attribute Change",
                        "tag": old_elem["tag"],
                        "old_attributes": self.highlight_differences(old_attrs, new_attrs),
                        "new_attributes": self.highlight_differences(new_attrs, old_attrs)
                    })

                old_text = old_elem["text"]
                new_text = new_elem["text"]

                if old_text != new_text:
                    changes.append({
                        "index": i,
                        "type": "Text Change",
                        "tag": old_elem["tag"],
                        "old_text": old_text,
                        "new_text": new_text
                    })

            elif old_elem:
                changes.append({
                    "index": i,
                    "type": "Tag Removal",
                    "old_tag": old_elem["tag"],
                    "old_attributes": old_elem["attributes"],
                    "reason": "Tag removed"
                })

            elif new_elem:
                changes.append({
                    "index": i,
                    "type": "Tag Addition",
                    "new_tag": new_elem["tag"],
                    "new_attributes": new_elem["attributes"],
                    "reason": "Tag added"
                })

        return changes

    def highlight_differences(self, dict1, dict2):
        highlighted = {}
        for key in dict1:
            if key in dict2 and dict1[key] != dict2[key]:
                highlighted[key] = {"old": dict1[key], "new": dict2[key]}
            else:
                highlighted[key] = dict1[key]
        return highlighted

    def display_results(self, changes):
        self.result_text.delete(1.0, tk.END)
        if changes:
            self.result_text.insert(tk.END, json.dumps(changes, indent=2), 'json_output')
            self.save_button.config(state=tk.NORMAL)
        else:
            self.result_text.insert(tk.END, "No differences found.")
            self.save_button.config(state=tk.DISABLED)

        self.compare_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)

    def save_results(self):
        changes = json.loads(self.result_text.get(1.0, tk.END).strip())
        save_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if save_file:
            with open(save_file, 'w', encoding='utf-8') as file:
                file.write(json.dumps(changes, indent=2))
            messagebox.showinfo("Save Successful", "JSON results saved successfully!")

    def load_file_content(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

if __name__ == "__main__":
    root = tk.Tk()
    app = HTMLComparatorApp(root)
    root.mainloop()
