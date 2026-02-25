import customtkinter as ctk
from cryptography.fernet import Fernet
import os
import tempfile
import shutil
import subprocess
import threading
import time
from tkinter import filedialog, messagebox

class DeCloudVault(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DeCloud Vault | Taurus Edition")
        self.geometry("600x600") 
        ctk.set_appearance_mode("dark")
        
        # Security Setup
        self.key_path = None
        self.fernet = self.setup_encryption()
        self.temp_dirs = []

        # Custom Fonts
        self.btn_font = ctk.CTkFont(family="Arial", size=18, weight="bold")
        self.desc_font = ctk.CTkFont(family="Arial", size=11, slant="italic")
        self.warning_font = ctk.CTkFont(family="Arial", size=11, weight="bold")
        self.path_font = ctk.CTkFont(family="Arial", size=10)

        # --- UI LAYOUT ---
        self.label = ctk.CTkLabel(self, text="🛡️ DeCloud Vault", font=("Arial", 32, "bold"), text_color="#8FBC8F")
        self.label.pack(pady=(15, 2))
        
        self.sub_label = ctk.CTkLabel(self, text="Batch Security for the Privacy-Conscious", font=("Arial", 13))
        self.sub_label.pack(pady=(0, 10))

        # 1. ENCRYPT SECTION
        self.enc_btn = ctk.CTkButton(self, text="🔒 ENCRYPT FILES", font=self.btn_font, fg_color="#4F7942", hover_color="#3E6034", height=55, command=self.encrypt_action)
        self.enc_btn.pack(pady=(5, 0), padx=80, fill="x")
        self.enc_desc = ctk.CTkLabel(self, text="Lock files. Metadata/Dates are preserved.", font=self.desc_font, text_color="#A9A9A9")
        self.enc_desc.pack(pady=(0, 8))

        # 2. PEEK SECTION
        self.peek_btn = ctk.CTkButton(self, text="👁️ SECURE PEEK", font=self.btn_font, fg_color="#3B5335", hover_color="#2D4029", height=55, command=self.peek_action)
        self.peek_btn.pack(pady=(5, 0), padx=80, fill="x")
        self.peek_desc = ctk.CTkLabel(self, text="Temporary view. No trace left behind.", font=self.desc_font, text_color="#A9A9A9")
        self.peek_desc.pack(pady=(0, 8))

        # 3. DECRYPT SECTION
        self.dec_btn = ctk.CTkButton(self, text="🔓 PERMANENT RESTORE", font=self.btn_font, fg_color="#333333", hover_color="#444444", height=55, command=self.decrypt_action)
        self.dec_btn.pack(pady=(5, 0), padx=80, fill="x")
        self.dec_desc = ctk.CTkLabel(self, text="Unlock files back to original state.", font=self.desc_font, text_color="#A9A9A9")
        self.dec_desc.pack(pady=(0, 8))

        # --- PERMANENT DISCLAIMER BOX ---
        self.disclaimer_frame = ctk.CTkFrame(self, fg_color="#2B1B1B", border_color="#722F37", border_width=1)
        self.disclaimer_frame.pack(pady=(5, 5), padx=60, fill="x")
        
        self.disclaimer_text = ctk.CTkLabel(
            self.disclaimer_frame, 
            text="⚠️ ATTENTION: Store key on a flash drive. Developer is NOT responsible for lost keys.\nKeep 'vault' in the filename so the app can find it if lost!",
            font=self.warning_font, text_color="#FF9999", wraplength=450
        )
        self.disclaimer_text.pack(pady=(8, 2))

        self.key_info_label = ctk.CTkLabel(self.disclaimer_frame, text=f"Active Key Path: {self.key_path}", font=self.path_font, text_color="gray")
        self.key_info_label.pack(pady=(0, 5))

        self.search_btn = ctk.CTkButton(self.disclaimer_frame, text="🔍 Search PC for 'vault' Keys", font=("Arial", 11, "bold"), fg_color="#444", height=24, command=self.search_for_key)
        self.search_btn.pack(pady=(0, 8))

        self.status = ctk.CTkLabel(self, text="Status: Ready", font=("Arial", 13, "bold"), text_color="#8FBC8F")
        self.status.pack(side="bottom", pady=5)

    def setup_encryption(self):
        has_key = messagebox.askyesno("Key Setup", "Do you already have a 'decloud-vault.key' file?")
        if has_key:
            messagebox.showinfo("Note", "Ensure your existing key has 'vault' in the filename for auto-discovery features.")
            path = filedialog.askopenfilename(title="Select your vault key", filetypes=[("Key files", "*.key")])
            if path:
                self.key_path = path
                return Fernet(open(path, "rb").read())
            else:
                messagebox.showerror("Error", "No key selected. App will now close.")
                self.destroy()
        else:
            messagebox.showwarning("CRITICAL: Master Key Security", 
                "You are about to create your Master Key.\n\n"
                "1. DEVELOPER LIABILITY: The developer is not responsible for lost keys or data.\n"
                "2. REDUNDANCY: Keep it on a physical USB drive and a backup location.\n"
                "3. IMPORTANT: Ensure 'vault' stays in the filename (e.g., decloud-vault.key).")
            
            path = filedialog.asksaveasfilename(title="Save NEW master key (OFFLINE ONLY)", 
                                                defaultextension=".key", initialfile="decloud-vault.key")
            if path:
                key = Fernet.generate_key()
                with open(path, "wb") as f: f.write(key)
                self.key_path = path
                messagebox.showinfo("Success", f"Key saved to: {path}\n\nBackup to a physical drive now!")
                return Fernet(key)
            else:
                self.destroy()

    def search_for_key(self):
        # UI for progress
        search_win = ctk.CTkToplevel(self)
        search_win.title("Scanning System...")
        search_win.geometry("400x200")
        search_win.attributes("-topmost", True)
        
        lbl = ctk.CTkLabel(search_win, text="Searching for files with 'vault' in name...", font=("Arial", 12))
        lbl.pack(pady=20)
        
        p_bar = ctk.CTkProgressBar(search_win, width=300)
        p_bar.pack(pady=10)
        p_bar.set(0)
        
        stats_lbl = ctk.CTkLabel(search_win, text="Preparing scan...", font=("Arial", 10))
        stats_lbl.pack(pady=5)

        def perform_search():
            found_keys = []
            search_root = os.path.expanduser("~") 
            
            # Step 1: Estimate work for percentage
            all_dirs = []
            for root, dirs, _ in os.walk(search_root):
                all_dirs.append(root)
            
            total_dirs = len(all_dirs)
            start_time = time.time()

            # Step 2: Actual Scan
            for i, root in enumerate(all_dirs):
                try:
                    files = os.listdir(root)
                    for file in files:
                        if "vault" in file.lower() and file.endswith(".key"):
                            found_keys.append(os.path.join(root, file))
                except PermissionError:
                    continue
                
                # Update progress
                progress_val = (i + 1) / total_dirs
                p_bar.set(progress_val)
                
                # Time estimation
                elapsed = time.time() - start_time
                if i > 0:
                    remaining = (elapsed / (i + 1)) * (total_dirs - (i + 1))
                    stats_lbl.configure(text=f"{int(progress_val*100)}% complete | Est. remaining: {int(remaining)}s")
                search_win.update_idletasks()

            search_win.destroy()
            
            if found_keys:
                self.show_found_keys(found_keys)
            else:
                messagebox.showinfo("Not Found", "No files containing 'vault' and '.key' found.")

        threading.Thread(target=perform_search, daemon=True).start()

    def show_found_keys(self, keys):
        results_win = ctk.CTkToplevel(self)
        results_win.title("Keys Found")
        results_win.geometry("500x400")
        
        ctk.CTkLabel(results_win, text="Click a button to open the folder containing the key:", font=("Arial", 12, "bold")).pack(pady=10)
        
        scroll_frame = ctk.CTkScrollableFrame(results_win, width=450, height=300)
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        for path in keys:
            frame = ctk.CTkFrame(scroll_frame)
            frame.pack(pady=5, fill="x")
            
            lbl = ctk.CTkLabel(frame, text=os.path.basename(path), font=("Arial", 11))
            lbl.pack(side="left", padx=10)
            
            btn = ctk.CTkButton(frame, text="Open Folder", width=100, height=24, 
                               command=lambda p=path: self.open_file_folder(p))
            btn.pack(side="right", padx=10)

    def open_file_folder(self, path):
        folder = os.path.dirname(path)
        if os.name == 'nt':
            os.startfile(folder)
        else:
            subprocess.run(['open', folder])

    def encrypt_action(self):
        file_paths = filedialog.askopenfilenames()
        if not file_paths: return
        count = 0
        for path in file_paths:
            stat = os.stat(path)
            orig_times = (stat.st_atime, stat.st_mtime)
            with open(path, "rb") as f: data = f.read()
            encrypted = self.fernet.encrypt(data)
            vault_path = path + ".vault"
            with open(vault_path, "wb") as f: f.write(encrypted)
            os.utime(vault_path, orig_times)
            os.remove(path)
            count += 1
        self.status.configure(text=f"Locked {count} files.")
        messagebox.showinfo("Success", f"{count} files encrypted.")

    def peek_action(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Vault Files", "*.vault")])
        if not file_paths: return
        temp_dir = tempfile.mkdtemp()
        self.temp_dirs.append(temp_dir)
        for path in file_paths:
            try:
                stat = os.stat(path)
                orig_times = (stat.st_atime, stat.st_mtime)
                with open(path, "rb") as f: decrypted = self.fernet.decrypt(f.read())
                orig_name = os.path.basename(path).replace(".vault", "")
                temp_file = os.path.join(temp_dir, orig_name)
                with open(temp_file, "wb") as f: f.write(decrypted)
                os.utime(temp_file, orig_times)
                if os.name == 'nt': os.startfile(temp_file)
                else: subprocess.run(['open', temp_file])
            except:
                messagebox.showerror("Error", f"Decryption failed for {os.path.basename(path)}")
        self.status.configure(text="Viewing session active.")

    def decrypt_action(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Vault Files", "*.vault")])
        if not file_paths: return
        count = 0
        for path in file_paths:
            stat = os.stat(path)
            orig_times = (stat.st_atime, stat.st_mtime)
            with open(path, "rb") as f: decrypted = self.fernet.decrypt(f.read())
            orig_path = path.replace(".vault", "")
            with open(orig_path, "wb") as f: f.write(decrypted)
            os.utime(orig_path, orig_times)
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