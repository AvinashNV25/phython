import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from bs4 import BeautifulSoup
import json
import threading

class HTMLComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Comparator")

        # Maximize window
        self.root.state('zoomed')

        # Create GUI elements
        self.label = tk.Label(self.root, text="Upload HTML files and compare", font=("Arial", 24))
        self.label.pack(pady=20)

        # Frame to hold file names and buttons
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=20)

        self.old_filename_label = tk.Label(file_frame, text="Old File: None", font=("Arial", 18))
        self.old_filename_label.pack(side=tk.LEFT, padx=20)

        self.old_file_button = tk.Button(file_frame, text="Upload Old HTML", command=self.upload_old_file, bg="#4CAF50", fg="white", font=("Arial", 14))
        self.old_file_button.pack(side=tk.LEFT, padx=20)

        self.new_filename_label = tk.Label(file_frame, text="New File: None", font=("Arial", 18))
        self.new_filename_label.pack(side=tk.LEFT, padx=20)

        self.new_file_button = tk.Button(file_frame, text="Upload New HTML", command=self.upload_new_file, bg="#008CBA", fg="white", font=("Arial", 14))
        self.new_file_button.pack(side=tk.LEFT, padx=20)

        # Compare button
        self.compare_button = tk.Button(self.root, text="Compare", command=self.compare_files, bg="#f44336", fg="white", font=("Arial", 18))
        self.compare_button.pack(pady=20)

        # Save button
        self.save_button = tk.Button(self.root, text="Save Results", command=self.save_results, bg="#2196F3", fg="white", state=tk.DISABLED, font=("Arial", 18))
        self.save_button.pack(pady=20)

        # Result display area
        self.result_text = scrolledtext.ScrolledText(self.root, height=20, width=100, wrap=tk.WORD, font=("Arial", 14))
        self.result_text.pack(pady=20)

        # Initialize variables
        self.old_file = None
        self.new_file = None
        self.changes = None

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
        file_dialog = filedialog.askopenfilename(initialdir="/", title="Select HTML File", filetypes=(("HTML files", "*.html"), ("All files", "*.*")))
        return file_dialog

    def get_filename_from_path(self, filepath):
        return filepath.split("/")[-1]  # Adjust this for Windows if needed

    def check_files_uploaded(self):
        if self.old_file and self.new_file:
            self.compare_button.config(state=tk.NORMAL)
        else:
            self.compare_button.config(state=tk.DISABLED)

    def compare_files(self):
        if self.old_file and self.new_file:
            # Disable buttons during comparison
            self.compare_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)

            # Start a new thread for comparison
            threading.Thread(target=self.perform_comparison).start()

    def perform_comparison(self):
        old_content = self.load_file_content(self.old_file)
        new_content = self.load_file_content(self.new_file)

        # Compare using BeautifulSoup
        old_soup = BeautifulSoup(old_content, "html.parser")
        new_soup = BeautifulSoup(new_content, "html.parser")

        # Find all elements in old and new documents
        old_elements = old_soup.find_all()
        new_elements = new_soup.find_all()

        # Compare elements
        self.changes = self.find_changes(old_elements, new_elements)

        # Update GUI with results
        self.root.after(0, self.display_results, self.changes)

    def display_results(self, changes):
        # Display changes or do further processing
        if changes:
            self.display_changes(changes)
            self.save_button.config(state=tk.NORMAL)
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "No differences found.")
            self.save_button.config(state=tk.DISABLED)

        # Enable buttons after comparison
        self.compare_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)

    def load_file_content(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    def find_changes(self, old_elements, new_elements):
        changes = []
        for old_elem, new_elem in zip(old_elements, new_elements):
            if old_elem != new_elem:
                # Example comparison: tag names and attributes
                old_attrs = dict(old_elem.attrs)
                new_attrs = dict(new_elem.attrs)

                if old_attrs != new_attrs:
                    change = {
                        "tag": old_elem.name,
                        "old_attributes": old_attrs,
                        "new_attributes": new_attrs
                    }
                    changes.append(change)

                # Additional comparison logic as needed

        return changes

    def display_changes(self, changes):
        self.result_text.delete(1.0, tk.END)
        
        # Iterate through changes and display them in the ScrolledText widget
        for change in changes:
            self.result_text.insert(tk.END, f"Tag: {change['tag']}\n")
            self.result_text.insert(tk.END, "Old Attributes:\n")
            for key, value in change['old_attributes'].items():
                self.result_text.insert(tk.END, f"    {key}: {value}\n")
            self.result_text.insert(tk.END, "New Attributes:\n")
            for key, value in change['new_attributes'].items():
                self.result_text.insert(tk.END, f"    {key}: {value}\n")
            self.result_text.insert(tk.END, "\n")

    def save_results(self):
        # Generate JSON output
        if self.changes:
            json_output = json.dumps(self.changes, indent=2)
            # Save JSON output to a file
            save_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
            if save_file:
                with open(save_file, 'w', encoding='utf-8') as file:
                    file.write(json_output)
                messagebox.showinfo("Save Successful", "JSON results saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HTMLComparatorApp(root)
    root.mainloop()
