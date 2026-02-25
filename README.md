# 🛡️ No AI No Cloud Vault (DeCloud Vault)
**Local-First, Zero-Knowledge Encryption for the Privacy-Conscious.**

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-GitHub-EA4AAA?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/IdaAkiwumi)
[![PayPal](https://img.shields.io/badge/Donate-PayPal-00457C?style=for-the-badge&logo=paypal)](https://www.paypal.com/paypalme/iakiwumi)

[![License: MIT](https://img.shields.io/badge/License-MIT-4F7942.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-8FBC8F.svg)](https://www.python.org/downloads/)

In an era where cloud providers scan your personal data to train AI models, **DeCloud Vault** acts as your digital fortress. It ensures your data is scrambled *before* it ever touches the cloud.

---

### ✨ Key Features
* **Zero-Knowledge:** No data is sent to any server. Encryption happens entirely on your machine.
* **Metadata Preservation:** Restored files keep their original "Date Created" and "Date Modified" timestamps.
* **Secure Peek:** View files in a temporary environment that wipes itself clean on exit.
* **Vault Search:** Built-in **Quick** or **Deep Scan** to find any `.key` file containing the word "vault" on your drives.
---

### 🚀 Installation & Build

#### **For Windows Users:**
Download the latest `DeCloudVault.exe` from the [Releases](https://github.com/IdaAkiwumi/No-AI-No-Cloud-Vault/releases) page. **No Python installation required.**

#### **For Mac & Linux Users:**
Mac and Linux users run the app using Python. Follow these steps:

1.  **Install Python:** * **Mac:** Download from [Python.org](https://www.python.org/downloads/macos/) or run `brew install python`.
    * **Linux:** Usually pre-installed. If not, run `sudo apt install python3 python3-pip`.
2.  **Download the Code:** Click the green **Code** button above and select **Download ZIP**. Extract it.
3.  **Install Requirements:** Open Terminal in the extracted folder and run:
    ```bash
    pip install customtkinter cryptography pillow
    ```
4.  **Run the App:** 
    ```bash
    python3 main.py
    ```

---

### 🛠️ Developer Build Instructions
To bundle the app into a standalone Windows executable:

1. Clone the repo: `git clone https://github.com/IdaAkiwumi/No-AI-No-Cloud-Vault.git`
2. Install dependencies: `pip install -r requirements.txt` or `pip install customtkinter cryptography pillow pyinstaller`
3. Run the build command:
   ```bash
   python -m PyInstaller --noconfirm --onefile --windowed --name "DeCloudVault" --icon="decloud-logo.ico" --add-data "decloud-logo.png;." --add-data "decloud-logo.ico;." main.py

---
## 📖 How to Use
1. **Prepare your Key:** Always keep your `.key` file on a physical USB drive, not on your computer.
2. **Encrypting:** Click 'Encrypt', select your files. They will turn into `.vault` files.
3. **Storing:** Move the `.vault` files to your preferred cloud provider (Google Drive, iCloud, etc.).
4. **Viewing:** Use 'Secure Peek' to open a file temporarily without permanently unlocking it.
5. **Restoring:** Use 'Permanent Restore' when you want to turn the `.vault` file back into a regular file.

## 📁 How to Encrypt Folders
[!IMPORTANT]
DeCloud Vault encrypts individual files. To secure an entire folder and preserve its internal structure, you must compress it first.

Right-click the folder you want to secure.

Select "Compress to ZIP file" (Windows) or "Compress" (macOS).

Open DeCloud Vault.

Click 🔒 ENCRYPT FILES and select your new .zip file.
Your folder is now a secure .vault file, ready for cloud storage.

---
## 🔍 Troubleshooting & FAQ
1. "Error: Key mismatch or corrupted file"
The Cause: You are trying to unlock a file with a different .key file than the one used to lock it.
The Fix: Ensure the "Active Key" path at the bottom of the window matches the key you generated for these specific files.
The Reality: If you have lost the specific key used for a file, the data cannot be recovered. This is by design for maximum security.

2. "Why did my file size increase?"
The Explanation: DeCloud Vault uses AES-128 encryption bundled in a Base64 wrapper. This ensures the file remains "safe to transport" across different cloud services and operating systems.
The Result: You will typically see a ~33% increase in file size (e.g., a 1MB photo becomes a 1.3MB .vault file).

3. "I can't find my key!"
The Fix: Use the Quick Scan or Deep Scan buttons at the bottom of the app.
How it works: The app will search your connected drives for any file ending in .key that contains the word "vault" in the filename.
Pro-Tip: This is why we recommend naming your keys something like personal-vault.key.

4. "Windows flagged the EXE as unsafe"
The Explanation: Because DeCloud Vault is a new, "unsigned" executable created with PyInstaller, Windows Defender might show a "Windows protected your PC" popup.
The Fix: Click "More Info" and then "Run Anyway." As an open-source project, you can always verify the safety of the app by reviewing the main.py code here on GitHub.

5. "Does 'Secure Peek' leave files on my computer?"
The Answer: No.
The Tech: When you "Peek," a temporary, hidden folder is created to hold the decrypted file while you view it. As soon as you close the DeCloud Vault app, that folder and its contents are permanently wiped.

---
### ☕ Support the Mission
If this tool helps you stay off the AI-grid, consider supporting the developer:
* [Sponsor on GitHub](https://github.com/sponsors/IdaAkiwumi)
* [Donate via PayPal](https://www.paypal.com/paypalme/iakiwumi)

---
*Disclaimer: This tool is provided "as is". The developer is not responsible for lost data due to lost master keys.*
