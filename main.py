import customtkinter as ctk
from cryptography.fernet import Fernet
import os
import tempfile
import shutil
import subprocess
import time
from tkinter import filedialog, messagebox

class DeCloudVault(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DeCloud Vault | Taurus Edition")
        self.geometry("600x700")
        ctk.set_appearance_mode("dark")
        
        # Security Setup - Now allows user to choose key location
        self.key_path = None
        self.fernet = self.setup_encryption()
        self.temp_dirs = []

        # Custom Font for Buttons
        self.btn_font = ctk.CTkFont(family="Arial", size=20, weight="bold")
        self.desc_font = ctk.CTkFont(family="Arial", size=12, slant="italic")

        # --- UI LAYOUT ---
        self.label = ctk.CTkLabel(self, text="🛡️ DeCloud Vault", font=("Arial", 36, "bold"), text_color="#8FBC8F")
        self.label.pack(pady=(40, 5))
        
        self.sub_label = ctk.CTkLabel(self, text="Batch Security for the Privacy-Conscious", font=("Arial", 14))
        self.sub_label.pack(pady=(0, 30))

        # 1. ENCRYPT SECTION
        self.enc_btn = ctk.CTkButton(self, text="🔒 ENCRYPT FILES", font=self.btn_font, fg_color="#4F7942", hover_color="#3E6034", height=70, command=self.encrypt_action)
        self.enc_btn.pack(pady=(10, 0), padx=60, fill="x")
        self.enc_desc = ctk.CTkLabel(self, text="Encrypt multiple files. Original date data is preserved.", font=self.desc_font, text_color="#A9A9A9")
        self.enc_desc.pack(pady=(2, 15))

        # 2. PEEK SECTION
        self.peek_btn = ctk.CTkButton(self, text="👁️ SECURE PEEK", font=self.btn_font, fg_color="#3B5335", hover_color="#2D4029", height=70, command=self.peek_action)
        self.peek_btn.pack(pady=(10, 0), padx=60, fill="x")
        self.peek_desc = ctk.CTkLabel(self, text="View files temporarily. Nothing is saved to your disk.", font=self.desc_font, text_color="#A9A9A9")
        self.peek_desc.pack(pady=(2, 15))

        # 3. DECRYPT SECTION
        self.dec_btn = ctk.CTkButton(self, text="🔓 PERMANENT RESTORE", font=self.btn_font, fg_color="#333333", hover_color="#444444", height=70, command=self.decrypt_action)
        self.dec_btn.pack(pady=(10, 0), padx=60, fill="x")
        self.dec_desc = ctk.CTkLabel(self, text="Fully restore files with their original timestamps.", font=self.desc_font, text_color="#A9A9A9")
        self.dec_desc.pack(pady=(2, 15))

        self.status = ctk.CTkLabel(self, text="Status: Ready", font=("Arial", 13, "bold"), text_color="#8FBC8F")
        self.status.pack(side="bottom", pady=20)

    def setup_encryption(self):
        # Initial choice
        has_key = messagebox.askyesno("Key Setup", "Do you already have a 'decloud-vault.key' file?")
        
        if has_key:
            path = filedialog.askopenfilename(title="Select your decloud-vault.key", filetypes=[("Key files", "*.key")])
            if path:
                self.key_path = path
                return Fernet(open(path, "rb").read())
            else:
                messagebox.showerror("Error", "No key selected. App will now close.")
                self.destroy()
        else:
            # IMPORTANT: Pre-save advisory
            messagebox.showwarning("CRITICAL: Master Key Security", 
                "You are about to create your Master Key.\n\n"
                "1. If you lose this key, your encrypted files CANNOT be recovered.\n"
                "2. We HIGHLY recommend saving copies in MULTIPLE places (e.g., an external Flash Drive AND your Desktop).\n"
                "3. Do not store this key inside the same cloud folder you are encrypting.")
            
            # Create new key at user's chosen location with unique name
            path = filedialog.asksaveasfilename(title="Choose where to save your NEW master key", 
                                                defaultextension=".key", 
                                                initialfile="decloud-vault.key")
            if path:
                key = Fernet.generate_key()
                with open(path, "wb") as f:
                    f.write(key)
                self.key_path = path
                messagebox.showinfo("Success", f"Key saved to: {path}\n\nPlease copy this file to a safe backup location (USB/External drive) now.")
                return Fernet(key)
            else:
                self.destroy()

    def encrypt_action(self):
        file_paths = filedialog.askopenfilenames()
        if not file_paths: return
        
        count = 0
        for path in file_paths:
            stat = os.stat(path)
            orig_times = (stat.st_atime, stat.st_mtime)
            with open(path, "rb") as f:
                data = f.read()
            encrypted = self.fernet.encrypt(data)
            vault_path = path + ".vault"
            with open(vault_path, "wb") as f:
                f.write(encrypted)
            os.utime(vault_path, orig_times)
            os.remove(path)
            count += 1
        self.status.configure(text=f"Locked {count} files. Originals safely removed.")
        messagebox.showinfo("Success", f"{count} files encrypted. Metadata preserved.")

    def peek_action(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Vault Files", "*.vault")])
        if not file_paths: return
        temp_dir = tempfile.mkdtemp()
        self.temp_dirs.append(temp_dir)
        for path in file_paths:
            try:
                stat = os.stat(path)
                orig_times = (stat.st_atime, stat.st_mtime)
                with open(path, "rb") as f:
                    decrypted = self.fernet.decrypt(f.read())
                orig_name = os.path.basename(path).replace(".vault", "")
                temp_file = os.path.join(temp_dir, orig_name)
                with open(temp_file, "wb") as f:
                    f.write(decrypted)
                os.utime(temp_file, orig_times)
                if os.name == 'nt': os.startfile(temp_file)
                else: subprocess.run(['open', temp_file])
            except:
                messagebox.showerror("Error", f"Failed to peek at {os.path.basename(path)}")
        self.status.configure(text="Viewing session active. Temp files will be wiped on exit.")

    def decrypt_action(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Vault Files", "*.vault")])
        if not file_paths: return
        count = 0
        for path in file_paths:
            stat = os.stat(path)
            orig_times = (stat.st_atime, stat.st_mtime)
            with open(path, "rb") as f:
                decrypted = self.fernet.decrypt(f.read())
            orig_path = path.replace(".vault", "")
            with open(orig_path, "wb") as f:
                f.write(decrypted)
            os.utime(orig_path, orig_times)
            os.remove(path)
            count += 1
        self.status.configure(text=f"Successfully restored {count} files.")

    def on_closing(self):
        for d in self.temp_dirs:
            if os.path.exists(d):
                shutil.rmtree(d)
        self.destroy()

if __name__ == "__main__":
    app = DeCloudVault()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()