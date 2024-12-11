import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class AVDManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AVD Manager")
        self.root.geometry("400x300")

        self.avd_list = self.get_avd_list()

        self.label = tk.Label(root, text="Select an AVD to open:")
        self.label.pack(pady=10)

        self.avd_var = tk.StringVar(root)
        if self.avd_list:
            self.avd_var.set(self.avd_list[0])  # set the default option

        self.avd_menu = tk.OptionMenu(root, self.avd_var, *self.avd_list)
        self.avd_menu.pack(pady=10)

        self.open_button = tk.Button(root, text="Open AVD", command=self.open_avd)
        self.open_button.pack(pady=10)

    def get_avd_list(self):
        try:
            result = subprocess.run(["emulator", "-list-avds"], capture_output=True, text=True)
            avd_names = result.stdout.splitlines()
            return avd_names
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get AVD list: {e}")
            return []

    def open_avd(self):
        avd_name = self.avd_var.get()
        try:
            # Adjust the path to the emulator executable if necessary
            emulator_path = os.path.join(os.environ['ANDROID_HOME'], 'emulator', 'emulator.exe')
            subprocess.Popen([emulator_path, "-avd", avd_name])
            messagebox.showinfo("Success", f"AVD {avd_name} is starting...")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start AVD {avd_name}: {e}")

if __name__ == "__main__":
    # Ensure ANDROID_HOME environment variable is set
    if 'ANDROID_HOME' not in os.environ:
        messagebox.showerror("Error", "ANDROID_HOME environment variable is not set.")
    else:
        root = tk.Tk()
        app = AVDManagerApp(root)
        root.mainloop()
