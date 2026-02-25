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
        
        # Security Setup
        self.key_path = "vault.key"
        self.key = self.get_or_create_key()
        self.fernet = Fernet(self.key)
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

    def get_or_create_key(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f: f.write(key)
            messagebox.showwarning("Key Created", "New 'vault.key' generated locally. BACK THIS UP!")
        return open(self.key_path, "rb").read()

    def encrypt_action(self):
        file_paths = filedialog.askopenfilenames()
        if not file_paths: return
        
        count = 0
        for path in file_paths:
            # Capture original timestamps
            stat = os.stat(path)
            orig_times = (stat.st_atime, stat.st_mtime)
            
            with open(path, "rb") as f:
                data = f.read()
            
            encrypted = self.fernet.encrypt(data)
            vault_path = path + ".vault"
            
            with open(vault_path, "wb") as f:
                f.write(encrypted)
            
            # Transfer original timestamps to the vault file so we don't lose them
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
                # Capture the "Original" timestamps from the vault file
                stat = os.stat(path)
                orig_times = (stat.st_atime, stat.st_mtime)

                with open(path, "rb") as f:
                    decrypted = self.fernet.decrypt(f.read())
                
                orig_name = os.path.basename(path).replace(".vault", "")
                temp_file = os.path.join(temp_dir, orig_name)
                
                with open(temp_file, "wb") as f:
                    f.write(decrypted)
                
                # Apply timestamps to temp file
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
            
            # Re-apply the original timestamps to the restored file
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