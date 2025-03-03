# Ubuntu WSL Setup Guide

Follow these instructions to set up and run the platform on Ubuntu WSL.

---

## 1. Install Python,Git and pip

Open your Ubuntu WSL terminal and run:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install git-all
```

Verify the installation:

```bash
python3 --version
pip3 --version
git --version
```

If you don’t have pip installed, install it using the commands above after installing Python.

## 2. Setting up Git and Connecting to Github
Note: Github account is need. 

Open your Ubuntu WSL terminal and run:

git config --global user.name [input your username]
git config --global user.email [input your email]
For cheking: run git config --list user.email and user.name must be in the output

Proceed to Step 3 if using https when cloning. Do the steps below when using SSH

To generate SSH key and Connect to github
ssh-keygen -t rsa 
ls -l ~/.ssh/ 
cat ~/.ssh/id_rsa.pub [copy and paste the ssh key in github found in settings]
Testing for connecton: ssh -T git@github.com 

## 3. Clone the GitHub Repository

Navigate to your desired directory and clone the repository:

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd <repository_folder>
```

Replace <YOUR_GITHUB_REPO_URL> with the actual URL of your repository, and <repository_folder> with the name of the cloned folder.

## 4. Create and Activate a Virtual Environment

Create a virtual environment to manage dependencies:

```bash
python3 -m venv eventlink
```

Activate the virtual environment:

```bash
source eventlink/bin/activate
```

Your prompt should now display (eventlink) indicating the virtual environment is active.

## 5. Install Project Dependencies

```bash
pip install flet fastapi uvicorn pymongo bcrypt httpx pydantic[email]
```

## 6. Run the FastAPI Server

The server code is located in server.py. In your terminal (or open a new tab/window), navigate to the project folder (and activate the virtual environment if needed), then run:

```bash
python3 -m uvicorn server:app --reload 
```

This starts the FastAPI server (typically at http://127.0.0.1:8000).

## 7. Run the Application (Login Page)

In another terminal window or tab (with the virtual environment activated), navigate to your project folder and run:

```bash
python3 login.py
```

This will launch the login page of the application.

## 8. Additional Notes

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
    python3 test_app.py
    ```
    
    This command will execute all tests. The output will indicate which tests passed, failed, or were skipped.

4. **Review the Results**
 
   Check your terminal for test results. If any tests fail, review the error messages to troubleshoot and fix issues.
