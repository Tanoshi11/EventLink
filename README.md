# Ubuntu WSL Setup Guide

Follow these instructions to set up and run the platform on Ubuntu WSL.

---

## 1. Install Python and pip

Open your Ubuntu WSL terminal and run:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

Verify the installation:

```bash
python3 --version
pip3 --version
```

If you don’t have pip installed, install it using the commands above after installing Python.

## 2. Clone the GitHub Repository

Navigate to your desired directory and clone the repository:

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd <repository_folder>
```

Replace <YOUR_GITHUB_REPO_URL> with the actual URL of your repository, and <repository_folder> with the name of the cloned folder.

## 3. Create and Activate a Virtual Environment

Create a virtual environment to manage dependencies:

```bash
python3 -m venv eventlink
```

Activate the virtual environment:

```bash
source env/bin/activate
```

Your prompt should now display (eventlink) indicating the virtual environment is active.

## 4. Install Project Dependencies

```bash
pip install flet fastapi uvicorn pymongo bcrypt httpx
```

## 5. Run the FastAPI Server

The server code is located in server.py. In your terminal (or open a new tab/window), navigate to the project folder (and activate the virtual environment if needed), then run:

```bash
uvicorn server:app --reload
```

This starts the FastAPI server (typically at http://127.0.0.1:8000).

## 6. Run the Application (Login Page)

In another terminal window or tab (with the virtual environment activated), navigate to your project folder and run:

```bash
python3 login.py
```

This will launch the login page of the application.

## 7. Additional Notes

- **Order of Operations:** Ensure the FastAPI server (**server.py**) is running before launching **login.py**.
- **Virtual Environment:** Always run `source env/bin/activate` in your terminal before executing project commands.
- **Troubleshooting:** If you run into issues with Python or pip, verify that you have installed all required packages and are using the correct interpreter.
- **Development Workflow:** Use your Ubuntu WSL terminal for all operations (cloning, environment setup, running the server, etc.) for consistency.

---

## Unit Testing

This project includes a comprehensive unit test suite to verify the functionality of both your FastAPI endpoints and Flet UI components.

### What’s Tested?
- **FastAPI Endpoints:**  
  - Login, registration, user retrieval (via `/get_user`), event listing, and checks for duplicate usernames/emails.
- **Flet UI Functions:**  
  - Homepage view, login view, and profile view (using a `FakePage` to simulate a Flet page).

### How to Run the Tests

1. **Activate Your Virtual Environment**  
   Ensure your virtual environment is active. For example, in Ubuntu or WSL:
   
   ```bash
   source eventlink/bin/activate
   ```
   
2. **Install Dependencies**
   
    Make sure all required packages are installed. You can install them via:

    ```bash
    pip install -r requirements.txt
    ```
    (If you don’t have a requirements.txt, ensure packages like fastapi, uvicorn, pymongo, bcrypt, httpx, and flet are installed.)

3. **Run the Test Suite**
    From the project’s root directory, run:
    
    ```bash
    python test_app.py
    ```
    
    This command will execute all tests. The output will indicate which tests passed, failed, or were skipped.

4. **Review the Results**
 
   Check your terminal for test results. If any tests fail, review the error messages to troubleshoot and fix issues.
