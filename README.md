# EventLink

**Local Event Coordination Platform (Ubuntu WSL)**

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

This will launch the login page of your application.

## 7. Additional Notes

- **Order of Operations:** Ensure the FastAPI server (**server.py**) is running before launching **login.py**.
- **Virtual Environment:** Always run `source env/bin/activate` in your terminal before executing project commands.
- **Troubleshooting:** If you run into issues with Python or pip, verify that you have installed all required packages and are using the correct interpreter.
- **Development Workflow:** Use your Ubuntu WSL terminal for all operations (cloning, environment setup, running the server, etc.) for consistency.
