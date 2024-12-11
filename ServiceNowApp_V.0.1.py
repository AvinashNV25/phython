import tkinter as tk
from tkinter import messagebox
import requests
from requests.auth import HTTPBasicAuth

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ServiceNow_APP_AviWorld_V.0.1")
        self.root.geometry("800x600")  # Larger size for better view
        self.root.configure(bg='#f0f0f0')  # Light grey background

        # Maximize the window
        self.root.state('zoomed')

        # Title Label
        self.title_label = tk.Label(root, text="ServiceNow API Query", font=("Helvetica", 16, "bold"), bg='#f0f0f0', fg='#333')
        self.title_label.pack(pady=10)

        # Instance URL
        self.url_label = tk.Label(root, text="Instance URL:", bg='#f0f0f0', anchor='w')
        self.url_label.pack(pady=5, padx=10, fill='x')
        self.url_entry = tk.Entry(root, width=100)
        self.url_entry.insert(0, "https://dev260663.service-now.com")  # Default URL
        self.url_entry.pack(pady=5, padx=10, fill='x')

        # Username
        self.username_label = tk.Label(root, text="Username:", bg='#f0f0f0', anchor='w')
        self.username_label.pack(pady=5, padx=10, fill='x')
        self.username_entry = tk.Entry(root, width=100)
        self.username_entry.insert(0, "admin")  # Default username
        self.username_entry.pack(pady=5, padx=10, fill='x')

        # Password
        self.password_label = tk.Label(root, text="Password:", bg='#f0f0f0', anchor='w')
        self.password_label.pack(pady=5, padx=10, fill='x')
        self.password_entry = tk.Entry(root, show='*', width=100)
        self.password_entry.insert(0, "Au9L!%wWw0Aa")  # Default password
        self.password_entry.pack(pady=5, padx=10, fill='x')

        # Submit Button
        self.submit_button = tk.Button(root, text="Submit", command=self.submit, bg='#007bff', fg='white', font=("Helvetica", 12, "bold"), activebackground='#0056b3', activeforeground='white')
        self.submit_button.pack(pady=20)

        # Output Area
        self.output_text = tk.Text(root, wrap='word', height=20, width=100, bg='#fff', fg='#000', font=("Helvetica", 12))
        self.output_text.pack(pady=10, padx=10, fill='both', expand=True)

    def submit(self):
        instance_url = self.url_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not instance_url or not username or not password:
            messagebox.showerror("Input Error", "Please provide all required fields.")
            return

        api_url = f"{instance_url}/api/now/table/change_request"
        params = {
            'sysparm_fields': 'number,short_description,sys_created_on'
        }

        try:
            response = requests.get(api_url, auth=HTTPBasicAuth(username, password), params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Print the raw response for debugging
            print("Status Code:", response.status_code)
            print("Raw Response:", response.text)
            
            data = response.json().get('result', [])
            self.output_text.delete(1.0, tk.END)

            if data:
                for change in data:
                    self.output_text.insert(tk.END, f"Change Number: {change.get('number', 'N/A')}\n")
                    self.output_text.insert(tk.END, f"Description: {change.get('short_description', 'N/A')}\n")
                    self.output_text.insert(tk.END, f"Created On: {change.get('sys_created_on', 'N/A')}\n\n")
            else:
                self.output_text.insert(tk.END, "No data found.")

            self.submit_button.config(bg='#28a745', fg='white')  # Change button color to green on successful request

        except requests.RequestException as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
