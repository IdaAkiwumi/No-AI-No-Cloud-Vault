import customtkinter as ctk
from cryptography.fernet import Fernet
import os
import tempfile
import shutil
import subprocess
from tkinter import filedialog, messagebox

class DeCloudVault(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DeCloud Vault | Taurus Edition")
        self.geometry("600x500")
        ctk.set_appearance_mode("dark")
        
        # Security Setup
        self.key_path = "vault.key"
        self.key = self.get_or_create_key()
        self.fernet = Fernet(self.key)
        self.temp_dirs = []

        # --- UI LAYOUT ---
        self.label = ctk.CTkLabel(self, text="🛡️ DeCloud Vault", font=("Arial", 28, "bold"), text_color="#8FBC8F")
        self.label.pack(pady=30)

        # Action Buttons
        self.enc_btn = ctk.CTkButton(self, text="🔒 Encrypt for Cloud", fg_color="#4F7942", height=50, command=self.encrypt_action)
        self.enc_btn.pack(pady=10, padx=50, fill="x")

        self.peek_btn = ctk.CTkButton(self, text="👁️ Secure Peek (View Only)", fg_color="#3B5335", height=50, command=self.peek_action)
        self.peek_btn.pack(pady=10, padx=50, fill="x")

        self.dec_btn = ctk.CTkButton(self, text="🔓 Permanent Decrypt", fg_color="#333333", height=50, command=self.decrypt_action)
        self.dec_btn.pack(pady=10, padx=50, fill="x")

        self.status = ctk.CTkLabel(self, text="Ready to protect your data.", text_color="gray")
        self.status.pack(side="bottom", pady=20)

    def get_or_create_key(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f: f.write(key)
            messagebox.showwarning("Key Created", "A new 'vault.key' has been created. Back it up! If you lose it, your data is gone forever.")
        return open(self.key_path, "rb").read()

    def encrypt_action(self):
        file_path = filedialog.askopenfilename()
        if not file_path: return
        
        with open(file_path, "rb") as f:
            data = f.read()
        
        encrypted = self.fernet.encrypt(data)
        out_path = file_path + ".vault"
        
        with open(out_path, "wb") as f:
            f.write(encrypted)
        
        if messagebox.askyesno("Confirm", "Encryption successful. Delete original file?"):
            os.remove(file_path)
            self.status.configure(text=f"Locked: {os.path.basename(out_path)}")

    def peek_action(self):
        file_path = filedialog.askopenfilename(filetypes=[("Vault Files", "*.vault")])
        if not file_path: return
        
        # Create hidden temp dir
        temp_dir = tempfile.mkdtemp()
        self.temp_dirs.append(temp_dir)
        
        try:
            with open(file_path, "rb") as f:
                decrypted = self.fernet.decrypt(f.read())
            
            original_name = os.path.basename(file_path).replace(".vault", "")
            temp_file = os.path.join(temp_dir, original_name)
            
            with open(temp_file, "wb") as f:
                f.write(decrypted)
            
            # Launch file
            if os.name == 'nt': os.startfile(temp_file)
            else: subprocess.run(['open', temp_file])
            
            self.status.configure(text="Viewing secure file. Close app to wipe temp data.")
        except:
            messagebox.showerror("Error", "Decryption failed.")

    def decrypt_action(self):
        file_path = filedialog.askopenfilename(filetypes=[("Vault Files", "*.vault")])
        if not file_path: return
        
        with open(file_path, "rb") as f:
            decrypted = self.fernet.decrypt(f.read())
        
        original_path = file_path.replace(".vault", "")
        with open(original_path, "wb") as f:
            f.write(decrypted)
        
        os.remove(file_path)
        self.status.configure(text="File restored to original state.")

    def on_closing(self):
        # Taurus Housekeeping: Clean up all temp files on exit
        for d in self.temp_dirs:
            if os.path.exists(d):
                shutil.rmtree(d)
        self.destroy()

if __name__ == "__main__":
    app = DeCloudVault()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()