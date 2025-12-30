# 🪟 Ultimate Beginner's Guide: Setup on Windows

Welcome! This guide is designed for **absolute beginners**. Follow these steps exactly, and you will have the Smart Class Companion running on your Windows computer in minutes!

---

## 🛑 Step 1: Install Python (Must Do First!)

Before anything else, your computer needs to understand Python code.

1.  **Download Python**: Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest version (e.g., Python 3.12 or newer).
2.  **Run the Installer**: Double-click the downloaded file.
3.  **⚠️ CRITICAL STEP**: On the first screen of the installer, look at the bottom.
    *   ✅ **CHECK THE BOX** that says: **"Add Python to PATH"** or **"Add Python to environment variables"**.
    *   *If you miss this, nothing will work!*
4.  Click **Install Now** and wait for it to finish.

---

## 📥 Step 2: Get the Project Code

1.  Go to the top of this GitHub page.
2.  Click the green **Code** button.
3.  Select **Download ZIP**.
4.  Once downloaded, finding the ZIP file in your Downloads folder.
5.  **Right-click** the ZIP file and select **Extract All...**
6.  Click **Extract**.
7.  Open the extracted folder (you should see files like `setup.bat`, `manage.py`, etc.).

---

## ⚙️ Step 3: The "One-Click" Setup

We made a special file to do all the hard work for you.

1.  In the folder you just extracted, look for a file named **`setup.bat`** (it might just show as `setup`).
2.  **Double-click** `setup.bat`.
3.  A black window (terminal) will pop up. **Don't panic!** It will ask you a few simple questions.

### 📝 How to Answer the Questions:

*   **Database Type?**
    *   Type `2` and press **Enter** (This chooses SQLite, which is easiest).
*   **Create superuser?**
    *   Type `y` and press **Enter**.
    *   Type a username (e.g., `admin`) -> Enter.
    *   Type an email (e.g., `admin@test.com`) -> Enter.
    *   Type a password (e.g., `1234`) -> Enter. (Note: **You won't see the password typing on screen**, that is normal!).
    *   Type password again -> Enter.
*   **Run tests?**
    *   Type `n` and press **Enter**.
*   **Start server?**
    *   Type `y` and press **Enter**.

---

## 🎉 Step 4: Use the App!

If everything went well, the black window will say "Starting development server..." and show a link.

1.  Open your web browser (Chrome, Edge, Firefox).
2.  Type this into the address bar: **`http://127.0.0.1:8000`**
3.  Press **Enter**.
4.  You should see the Smart Class Companion homepage!

### How to Log In as Admin
1.  Go to `http://127.0.0.1:8000/admin`
2.  Use the username/password you created in Step 3.

---

## 🔁 Step 5: How to Run It Next Time

When you close the black window, the website stops working. To start it again tomorrow:

1.  Open the project folder.
2.  Double-click **`setup.bat`** again.
3.  It will jump straight to asking if you want to start the server.
4.  Type `y` and press **Enter**.

---

## ❓ Troubleshooting (Help! It didn't work)

### "Python is not installed" error?
*   You probably missed the **"Add Python to PATH"** checkbox in Step 1.
*   **Fix**: Uninstall Python, restart your computer, and reinstall it. **Make sure to check that box!**

### The black window opens and closes immediately?
*   This usually means Python isn't found. Try the fix above.
*   Or, try right-clicking `setup.ps1` and selecting **"Run with PowerShell"**.

### "Port already in use"?
*   You already have the server running in another window!
*   Find the other black window and close it, or press `Ctrl + C` inside it.

### Browser says "Unable to connect"?
*   Make sure the black window is **still open**. If you close it, the app stops.

---

**Enjoy your new Smart Class!** 🎓
