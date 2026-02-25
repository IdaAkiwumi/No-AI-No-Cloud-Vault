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
* **Metadata Preservation:** Restored files keep their original timestamps.
* **Secure Peek:** View files in a temporary environment that wipes itself clean on exit.
* **Vault Search:** Built-in **Quick** or **Deep Scan** to find any `.key` file containing "vault" on your drives.

---

### 🚀 Installation & Build

#### **For Windows Users:**
Just download the latest `DeCloudVault.exe` from the [Releases](https://github.com/YOUR_USERNAME/No-AI-No-Cloud-Vault/releases) page. No installation required.

#### **For Mac & Linux Users (Newbie Friendly):**
Since Mac and Linux require Python to run the source code, follow these steps:

1.  **Install Python:** * **Mac:** Download from [Python.org](https://www.python.org/downloads/macos/) or run `brew install python` in Terminal.
    * **Linux:** Usually pre-installed. If not, run `sudo apt install python3 python3-pip`.
2.  **Download the Code:** Click the green **Code** button above and select **Download ZIP**. Extract it.
3.  **Install Requirements:** Open your Terminal, navigate to the folder, and type:
    ```bash
    pip install customtkinter cryptography pillow
    ```
4.  **Run the App:** ```bash
    python3 main.py
    ```

---

### 🛠️ Developer Build Instructions
1. Clone the repo: `git clone https://github.com/IdaAkiwumi/No-AI-No-Cloud-Vault.git`
2. Install dependencies: `pip install customtkinter cryptography pillow`
3. Package as EXE: `pyinstaller --noconfirm --onefile --windowed --icon="decloud-logo.ico" --add-data "decloud-logo.png;." --add-data "decloud-logo.ico;." main.py`

---

### ☕ Support the Mission
If this tool helps you stay off the AI-grid, consider supporting the developer:
* [Sponsor on GitHub](https://github.com/sponsors/IdaAkiwumi)
* [Donate via PayPal](https://www.paypal.com/paypalme/iakiwumi)

---
*Disclaimer: This tool is provided "as is". The developer is not responsible for lost data due to lost master keys.*