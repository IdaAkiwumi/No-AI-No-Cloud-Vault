# 🛡️ No-AI-No-Cloud Vault (DeCloud Vault)
**Local-First, Zero-Knowledge Encryption for the Privacy-Conscious.**

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-GitHub-EA4AAA?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/IdaAkiwumi)
[![PayPal](https://img.shields.io/badge/Donate-PayPal-00457C?style=for-the-badge&logo=paypal)](https://www.paypal.com/paypalme/iakiwumi)
[![License: MIT](https://img.shields.io/badge/License-MIT-4F7942.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-8FBC8F.svg)](https://www.python.org/downloads/)

In an era where cloud providers scan your personal data to train AI models, **DeCloud Vault** acts as your digital fortress. It ensures your data is scrambled *before* it ever touches the cloud.

---

### ✨ Key Features
* **Zero-Knowledge:** No data is sent to any server. Encryption happens entirely on your machine.
* **Taurus-Grade Security:** A focus on physical key management. Your `vault.key` is your responsibility.
* **Metadata Preservation:** Restored files keep their original "Date Created" and "Date Modified" timestamps.
* **Secure Peek:** View your files in a temporary environment that wipes itself clean the moment you close the app.
* **Vault Search:** Lost your key? Use the built-in **Quick** or **Deep Scan** to find any file on your PC containing the word "vault".

---

### 🚀 How It Works
1.  **Generate your Key:** Save your `decloud-vault.key` to a physical USB drive.
2.  **Lock your Files:** Select files to encrypt. They will be turned into `.vault` files.
3.  **Upload Safely:** Move these `.vault` files to Google Drive, Dropbox, or OneDrive.
4.  **Secure Peek:** Need to check a document? Use Peek to open it without permanently decrypting it.

---

### 🛠️ Installation & Build
**For Users:**
Download the latest `DeCloudVault.exe` from the [Releases](https://github.com/YOUR_USERNAME/No-AI-No-Cloud-Vault/releases) page.

**For Developers:**
1. Clone the repo: `git clone https://github.com/IdaAkiwumi/No-AI-No-Cloud-Vault.git`
2. Install dependencies: `pip install customtkinter cryptography`
3. Run: `python main.py`

---

### ☕ Support the Mission
If this tool helps you stay off the AI-grid, consider supporting the developer:
* [Sponsor on GitHub](https://github.com/sponsors/IdaAkiwumi)
* [Donate via PayPal](https://www.paypal.com/paypalme/iakiwumi)

---
*Disclaimer: This tool is provided "as is". The developer is not responsible for lost data due to lost master keys.*