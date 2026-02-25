import customtkinter as ctk
from cryptography.fernet import Fernet
import os
import tempfile
import shutil
import subprocess
import threading
import time
import string
from tkinter import filedialog, messagebox

# Platform-specific sound support
if os.name == 'nt':
    import winsound

class DeCloudVault(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DeCloud Vault | Taurus Edition")
        self.geometry("600x750") # Slightly increased to fit two buttons
        self.minsize(600, 700)
        ctk.set_appearance_mode("dark")
        
        # --- App State ---
        self.font_scale = 1.0
        self.base_font_size = 18
        self.temp_dirs = []
        self.key_path = "No Key Loaded"
        self.fernet = None 
        
        # Security Setup - Window renders first, alerts follow 300ms later
        self.after(300, self.initial_setup)

        # --- UI LAYOUT ---
        self.font_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.font_frame.pack(side="top", anchor="ne", padx=10, pady=5)
        
        self.font_down = ctk.CTkButton(self.font_frame, text="a", width=30, height=25, command=lambda: self.change_font(-2))
        self.font_down.pack(side="left", padx=2)
        self.font_up = ctk.CTkButton(self.font_frame, text="A", width=30, height=25, command=lambda: self.change_font(2))
        self.font_up.pack(side="left", padx=2)

        self.label = ctk.CTkLabel(self, text="🛡️ DeCloud Vault", font=("Arial", 32, "bold"), text_color="#8FBC8F")
        self.label.pack(pady=(5, 2))
        
        self.sub_label = ctk.CTkLabel(self, text="Batch Security for the Privacy-Conscious", font=("Arial", 16))
        self.sub_label.pack(pady=(0, 15))

        # 1. ENCRYPT SECTION
        self.enc_btn = ctk.CTkButton(self, text="🔒 ENCRYPT FILES", fg_color="#4F7942", hover_color="#3E6034", height=65, command=self.encrypt_action)
        self.enc_btn.pack(pady=(5, 0), padx=80, fill="x")
        self.enc_desc = ctk.CTkLabel(self, text="Lock files. Metadata/Dates are preserved.", text_color="#A9A9A9")
        self.enc_desc.pack(pady=(0, 12))

        # 2. PEEK SECTION
        self.peek_btn = ctk.CTkButton(self, text="👁️ SECURE PEEK", fg_color="#3B5335", hover_color="#2D4029", height=65, command=self.peek_action)
        self.peek_btn.pack(pady=(5, 0), padx=80, fill="x")
        self.peek_desc = ctk.CTkLabel(self, text="Temporary view. No trace left behind.", text_color="#A9A9A9")
        self.peek_desc.pack(pady=(0, 12))

        # 3. DECRYPT SECTION
        self.dec_btn = ctk.CTkButton(self, text="🔓 PERMANENT RESTORE", fg_color="#333333", hover_color="#444444", height=65, command=self.decrypt_action)
        self.dec_btn.pack(pady=(5, 0), padx=80, fill="x")
        self.dec_desc = ctk.CTkLabel(self, text="Unlock files back to original state.", text_color="#A9A9A9")
        self.dec_desc.pack(pady=(0, 12))

        # --- PERMANENT DISCLAIMER & SEARCH ---
        self.disclaimer_frame = ctk.CTkFrame(self, fg_color="#2B1B1B", border_color="#722F37", border_width=1)
        self.disclaimer_frame.pack(pady=(5, 5), padx=60, fill="x")
        
        self.key_path_label = ctk.CTkLabel(self.disclaimer_frame, text=f"ACTIVE KEY: {self.key_path}", text_color="#8FBC8F")
        self.key_path_label.pack(pady=(5, 0))

        self.liab_text = ctk.CTkLabel(self.disclaimer_frame, text="DEVELOPER DISCLAIMER: Not responsible for lost data/keys.", text_color="#FF9999")
        self.liab_text.pack(pady=(2, 0))

        self.disclaimer_text = ctk.CTkLabel(
            self.disclaimer_frame, 
            text="⚠️ IMPORTANT: 1. Ensure 'vault' is in the key name. 2. Copy to multiple physical drives. 3. Without this file, data is lost forever. 4. If you correctly add vault to the filename, you can search for it using the buttons below.",
            text_color="#FFCCCC", wraplength=400
        )
        self.disclaimer_text.pack(pady=(2, 5))

        # Search Button Container
        self.btn_container = ctk.CTkFrame(self.disclaimer_frame, fg_color="transparent")
        self.btn_container.pack(pady=(5, 10))

        self.quick_search_btn = ctk.CTkButton(self.btn_container, text="⚡ Quick Home Scan", fg_color="#444", width=160, command=lambda: self.search_for_key(deep=False))
        self.quick_search_btn.pack(side="left", padx=5)

        self.deep_search_btn = ctk.CTkButton(self.btn_container, text="🔍 Deep PC Scan", fg_color="#555", width=160, command=lambda: self.search_for_key(deep=True))
        self.deep_search_btn.pack(side="left", padx=5)

        self.status = ctk.CTkLabel(self, text="Status: Ready", text_color="#8FBC8F")
        self.status.pack(side="bottom", pady=10)
        
        self.update_font_sizes()

    def play_alert(self):
        """Native system alert sound"""
        try:
            if os.name == 'nt':
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            else:
                # Standard terminal bell for Mac/Linux
                print('\a - main.py:106')
        except:
            pass

    def update_key_display(self, path):
        self.key_path = path
        display_path = (path[:20] + "..." + path[-25:]) if len(path) > 50 else path
        self.key_path_label.configure(text=f"ACTIVE KEY: {display_path}")

    def initial_setup(self):
        self.fernet = self.setup_encryption()
        if not self.fernet:
            self.status.configure(text="Status: No Key Loaded - Security Disabled", text_color="#FF9999")

    def change_font(self, delta):
        self.base_font_size = max(12, min(28, self.base_font_size + delta))
        self.update_font_sizes()

    def update_font_sizes(self):
        main_f = ("Arial", self.base_font_size, "bold")
        desc_f = ("Arial", max(10, self.base_font_size - 6), "italic")
        small_f = ("Arial", max(9, self.base_font_size - 8), "bold")
        warn_f = ("Arial", max(10, self.base_font_size - 7))

        self.label.configure(font=("Arial", self.base_font_size + 14, "bold"))
        self.sub_label.configure(font=("Arial", self.base_font_size - 2))
        self.enc_btn.configure(font=main_f)
        self.peek_btn.configure(font=main_f)
        self.dec_btn.configure(font=main_f)
        self.enc_desc.configure(font=desc_f)
        self.peek_desc.configure(font=desc_f)
        self.dec_desc.configure(font=desc_f)
        self.key_path_label.configure(font=small_f)
        self.liab_text.configure(font=small_f)
        self.disclaimer_text.configure(font=warn_f)
        self.quick_search_btn.configure(font=("Arial", self.base_font_size - 4))
        self.deep_search_btn.configure(font=("Arial", self.base_font_size - 4))
        self.status.configure(font=main_f)

    def setup_encryption(self):
        messagebox.showinfo("Security Requirement", 
            "Welcome to DeCloud Vault.\n\n"
            "1. Key filename must contain 'vault'.(VERY IMPORTANT)\n"
            "2. Redundancy: Copy to multiple physical drives.\n"
            "3. Offline Storage Only. DO NOT Save in Cloud Storage (e.g., Google Drive, Dropbox).\n"
            "4. Lost key = Lost data.", parent=self)

        has_key = messagebox.askyesno("Key Setup", "Do you already have a 'vault' key file?", parent=self)
        
        if has_key:
            path = filedialog.askopenfilename(title="Select your vault key", filetypes=[("Key files", "*.key")], parent=self)
            if path:
                self.update_key_display(path)
                self.status.configure(text="Status: Master Key Loaded", text_color="#8FBC8F")
                return Fernet(open(path, "rb").read())
        else:
            path = filedialog.asksaveasfilename(title="Save NEW master key", defaultextension=".key", initialfile="decloud-vault.key", parent=self)
            if path:
                key = Fernet.generate_key()
                with open(path, "wb") as f: f.write(key)
                self.update_key_display(path)
                self.status.configure(text="Status: New Key Created", text_color="#8FBC8F")
                return Fernet(key)
        return None

    def search_for_key(self, deep=False):
        search_win = ctk.CTkToplevel(self)
        mode_text = "Deep PC Scan..." if deep else "Quick Home Scan..."
        search_win.title(mode_text)
        search_win.geometry("450x300")
        search_win.attributes("-topmost", True)
        
        lbl = ctk.CTkLabel(search_win, text=f"Scanning: {mode_text}", font=("Arial", 16, "bold"))
        lbl.pack(pady=(20, 10))
        
        p_bar = ctk.CTkProgressBar(search_win, width=350, mode="indeterminate")
        p_bar.pack(pady=10)
        p_bar.start()
        
        stats_lbl = ctk.CTkLabel(search_win, text="Initializing Scan...", font=("Arial", 13))
        stats_lbl.pack(pady=2)

        dir_lbl = ctk.CTkLabel(search_win, text="", font=("Arial", 11, "italic"), text_color="gray", wraplength=400)
        dir_lbl.pack(pady=5)

        def perform_search():
            found_keys = []
            scanned_dirs = 0
            
            if not deep:
                # Quick search only looks at the user's home directory
                drives = [os.path.expanduser("~")]
            else:
                # Deep search looks at all connected letters/volumes
                if os.name == 'nt':
                    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
                else:
                    drives = [os.path.expanduser("~"), "/Volumes"]

            for drive in drives:
                self.after(0, lambda d=drive: dir_lbl.configure(text=f"Drive: {d}"))
                for root, dirs, files in os.walk(drive):
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in 
                              ['appdata', 'library', 'cache', 'windows', 'node_modules', 'program files', 'program files (x86)', '$recycle.bin']]
                    
                    scanned_dirs += 1
                    for file in files:
                        if "vault" in file.lower() and file.endswith(".key"):
                            found_keys.append(os.path.join(root, file))
                    
                    if scanned_dirs % 15 == 0:
                        current_dir = os.path.basename(root)
                        self.after(0, lambda sd=scanned_dirs, cd=current_dir: (
                            stats_lbl.configure(text=f"Folders Checked: {sd}"),
                            dir_lbl.configure(text=f"Scanning: .../{cd}")
                        ))
            
            self.after(0, lambda: finalize_search(found_keys))

        def finalize_search(keys):
            if search_win.winfo_exists(): 
                p_bar.stop()
                search_win.destroy()
            
            self.play_alert() # Trigger alert sound on completion
            
            if keys: 
                self.show_found_keys(keys)
            else: 
                messagebox.showinfo("Scan Complete", "No '.key' files with 'vault' found.", parent=self)

        threading.Thread(target=perform_search, daemon=True).start()

    def show_found_keys(self, keys):
        results_win = ctk.CTkToplevel(self)
        results_win.title("Found Keys")
        results_win.geometry("550x450")
        results_win.attributes("-topmost", True)
        
        ctk.CTkLabel(results_win, text="Keys Located Across Drives:", font=("Arial", 16, "bold")).pack(pady=15)
        scroll_frame = ctk.CTkScrollableFrame(results_win, width=500, height=350)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        for path in keys:
            frame = ctk.CTkFrame(scroll_frame)
            frame.pack(pady=5, fill="x", padx=5)
            short_path = (path[:3] + "..." + path[-35:]) if len(path) > 40 else path
            lbl = ctk.CTkLabel(frame, text=short_path, font=("Arial", 11))
            lbl.pack(side="left", padx=10, pady=5)
            btn = ctk.CTkButton(frame, text="View Folder", width=100, command=lambda p=path: self.open_file_folder(p))
            btn.pack(side="right", padx=10)

    def open_file_folder(self, path):
        folder = os.path.dirname(path)
        if os.name == 'nt': os.startfile(folder)
        else: subprocess.run(['open', folder])

    def encrypt_action(self):
        if not self.fernet:
            messagebox.showwarning("No Key", "Please load or create a key first.", parent=self)
            return
        file_paths = filedialog.askopenfilenames(parent=self)
        if not file_paths: return
        count = 0
        for path in file_paths:
            stat = os.stat(path)
            with open(path, "rb") as f: data = f.read()
            encrypted = self.fernet.encrypt(data)
            vault_path = path + ".vault"
            with open(vault_path, "wb") as f: f.write(encrypted)
            os.utime(vault_path, (stat.st_atime, stat.st_mtime))
            os.remove(path)
            count += 1
        self.status.configure(text=f"Locked {count} files.")

    def peek_action(self):
        if not self.fernet:
            messagebox.showwarning("No Key", "Please load or create a key first.", parent=self)
            return
        file_paths = filedialog.askopenfilenames(filetypes=[("Vault Files", "*.vault")], parent=self)
        if not file_paths: return
        temp_dir = tempfile.mkdtemp()
        self.temp_dirs.append(temp_dir)
        for path in file_paths:
            try:
                stat = os.stat(path)
                with open(path, "rb") as f: decrypted = self.fernet.decrypt(f.read())
                temp_file = os.path.join(temp_dir, os.path.basename(path).replace(".vault", ""))
                with open(temp_file, "wb") as f: f.write(decrypted)
                os.utime(temp_file, (stat.st_atime, stat.st_mtime))
                if os.name == 'nt': os.startfile(temp_file)
                else: subprocess.run(['open', temp_file])
            except: messagebox.showerror("Error", "Key mismatch or corrupted file.", parent=self)

    def decrypt_action(self):
        if not self.fernet:
            messagebox.showwarning("No Key", "Please load or create a key first.", parent=self)
            return
        file_paths = filedialog.askopenfilenames(filetypes=[("Vault Files", "*.vault")], parent=self)
        if not file_paths: return
        count = 0
        for path in file_paths:
            stat = os.stat(path)
            with open(path, "rb") as f: decrypted = self.fernet.decrypt(f.read())
            orig_path = path.replace(".vault", "")
            with open(orig_path, "wb") as f: f.write(decrypted)
            os.utime(orig_path, (stat.st_atime, stat.st_mtime))
            os.remove(path)
            count += 1
        self.status.configure(text=f"Restored {count} files.")

    def on_closing(self):
        for d in self.temp_dirs:
            if os.path.exists(d): shutil.rmtree(d)
        self.destroy()

if __name__ == "__main__":
    app = DeCloudVault()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()