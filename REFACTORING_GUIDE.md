# GitHub Repository Structure Refactoring Guide

This guide provides a step-by-step process to refactor the `carbon-dashboard` repository into a more professional and maintainable structure.

## 🚨 IMPORTANT: Backup Your Project First!

Before you begin, please create a backup of your project. This will ensure that you can recover your work in case of any mistakes.

```bash
# Create a zip archive of your project
zip -r carbon-dashboard-backup.zip carbon-dashboard
```

## 🎯 Goal: A Clean and Professional Project Structure

We will transform the current project structure into a more organized and scalable one.

### Before
```
carbon-dashboard/
├── .vscode/
├── backend/
│   └── data/
├── css/
├── js/
├── data/
├── .DS_Store
├── app.py
├── *.html (7 files)
├── structure.md
└── README.md
```

### After
```
carbon-dashboard/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── data/
│       └── ...
├── frontend/
│   ├── *.html (7 files)
│   └── assets/
│       ├── css/
│       └── js/
├── docs/
│   └── structure.md
├── .gitignore
└── README.md
```

---

## 📚 Step-by-Step Refactoring Guide

### Step 1: Clean Up Unnecessary Files from Git

First, we will remove files that should not be tracked by Git. We use `git rm --cached` to remove them from the index while keeping them locally.

1.  **Remove `.DS_Store`:**
    ```bash
    # For Mac/Linux
    git rm --cached .DS_Store -f
    # For Windows (if Thumbs.db exists)
    # git rm --cached Thumbs.db -f
    ```

2.  **Remove `.vscode` directory:**
    ```bash
    # This command removes the entire .vscode directory from git tracking
    git rm -r --cached .vscode
    ```

3.  **Verification:** Check the status to see the removed files.
    ```bash
    git status
    # You should see ".DS_Store" and ".vscode/settings.json" as deleted.
    ```

### Step 2: Create New Directories

Let's create the new folder structure for `frontend` and `docs`.

1.  **Create directories:**
    ```bash
    # For Mac/Linux
    mkdir -p frontend/assets/css frontend/assets/js docs
    
    # For Windows
    mkdir frontend
    mkdir frontend\assets
    mkdir frontend\assets\css
    mkdir frontend\assets\js
    mkdir docs
    ```

2.  **Verification:**
    ```bash
    # For Mac/Linux
    ls -l
    
    # For Windows
    dir
    # You should see the new 'frontend' and 'docs' directories.
    ```

### Step 3: Move Files and Directories

Now, we will move the existing files into the new structure.

1.  **Move HTML files:**
    ```bash
    # For Mac/Linux
    mv *.html frontend/
    
    # For Windows
    move *.html frontend\
    ```

2.  **Move CSS and JS files:**
    ```bash
    # For Mac/Linux
    mv css/* frontend/assets/css/
    mv js/* frontend/assets/js/
    
    # For Windows
    move css\* frontend\assets\css\
    move js\* frontend\assets\js\
    ```

3.  **Move `structure.md`:**
    ```bash
    # For Mac/Linux
    mv structure.md docs/
    
    # For Windows
    move structure.md docs\
    ```

4.  **Move `app.py`:**
    ```bash
    # For Mac/Linux
    mv app.py backend/
    
    # For Windows
    move app.py backend\
    ```

5.  **Remove old, empty directories:**
    ```bash
    # For Mac/Linux
    rmdir css js
    
    # For Windows
    rmdir css
    rmdir js
    ```

6.  **Verification:**
    ```bash
    # For Mac/Linux
    ls -R
    
    # For Windows
    dir /s
    # Check that all files are in their new locations.
    ```

### Step 4: Create `.gitignore`

A `.gitignore` file tells Git which files to ignore.

1.  **Create the `.gitignore` file** with the following content:
    ```
    # Python
    *.pyc
    __pycache__/
    venv/
    env/
    *.egg-info/
    
    # OS
    .DS_Store
    Thumbs.db
    
    # IDE
    .vscode/
    .idea/
    *.swp
    *.swo
    
    # Data (if sensitive)
    # backend/data/*.csv
    
    # Logs
    *.log
    ```
    You can create this file using a text editor or the following command:
    ```bash
    # For Mac/Linux
    cat > .gitignore << EOF
    # Python
    *.pyc
    __pycache__/
    venv/
    env/
    *.egg-info/
    # OS
    .DS_Store
    Thumbs.db
    # IDE
    .vscode/
    .idea/
    *.swp
    *.swo
    # Data (if sensitive)
    # backend/data/*.csv
    # Logs
    *.log
    EOF
    
    # For Windows (using PowerShell)
    @"\
    # Python
    *.pyc
    __pycache__/\n    venv/\n    env/\n    *.egg-info/\n    # OS
    .DS_Store\n    Thumbs.db\n    # IDE
    .vscode/\n    .idea/\n    *.swp\n    *.swo\n    # Data (if sensitive)\n    # backend/data/*.csv\n    # Logs
    *.log\n    "@ | Out-File -Encoding utf8 .gitignore
    ```

### Step 5: Create `requirements.txt`

This file lists the Python dependencies for the backend.

1.  **Create `backend/requirements.txt`** with the following content:
    ```
    Flask==2.3.0
    Flask-CORS==4.0.0
    pandas==2.0.3
    ```
    You can create this file using a text editor or the following command:
    ```bash
    # For Mac/Linux
    cat > backend/requirements.txt << EOF
    Flask==2.3.0
    Flask-CORS==4.0.0
    pandas==2.0.3
    EOF

    # For Windows (using PowerShell)
    @"\
    Flask==2.3.0\n    Flask-CORS==4.0.0\n    pandas==2.0.3\n    "@ | Out-File -Encoding utf8 backend\requirements.txt
    ```

### Step 6: Update `app.py`

Update the Flask application to find the `frontend` files in their new location.

-   **File:** `backend/app.py`

-   **Before:**
    ```python
    app = Flask(__name__, template_folder='.', static_folder='.')
    DATA_DIR = "data"
    ```

-   **After:**
    ```python
    app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/assets')
    DATA_DIR = "data"
    ```
    *Note: The `DATA_DIR` path is relative to `app.py`, so it should remain `"data"`. The HTML routes should be removed if you are serving them as static files.*

### Step 7: Commit and Push the Changes

Finally, commit all your changes to the repository.

1.  **Stage all changes:**
    ```bash
    git add .
    ```

2.  **Commit the changes:**
    ```bash
    git commit -m "refactor: reorganize project structure for better maintainability"
    ```

3.  **Push to the remote repository:**
    ```bash
    git push origin master
    ```

---

## 🎁 Bonus Section

### Common Mistakes to Avoid

-   **Never use `git rm -rf /`:** This is a dangerous command that can delete your entire file system.
-   **Don't commit large data files:** Keep large CSV files out of Git if possible. Use `.gitignore` to exclude them.
-   **Don't mix file types:** Keep backend code, frontend code, and documentation in separate directories.

### Performance and Collaboration Benefits

-   **Faster Navigation:** A clean structure makes it easier to find files.
-   **Improved CI/CD:** A well-structured project is easier to build, test, and deploy with CI/CD pipelines.
-   **Easier Collaboration:** Team members can easily understand the project layout and contribute more effectively.

### Pull Request Template for Your Team

When you create a pull request with these changes, use a template like this:

```markdown
## 🚀 Refactor: Project Structure Overhaul

### Description
This PR refactors the entire project structure for better maintainability and scalability, following our new repository guidelines.

### Changes
-   Separated `frontend` and `backend` concerns.
-   Moved all static assets to `frontend/assets`.
-   Added `.gitignore` and `requirements.txt`.
-   Updated `app.py` to reflect the new structure.

### How to Test
1.  Pull this branch.
2.  Run `pip install -r backend/requirements.txt`.
3.  Run `python backend/app.py`.
4.  Open `frontend/index.html` in your browser.
5.  Verify that the dashboard loads correctly.

### Checklist
-   [x] All files moved to their new locations.
-   [x] `.gitignore` is working as expected.
-   [x] `app.py` has been updated.
-   [x] The application runs without errors.
```

---

## ✅ Final Checklist

-   [ ] Project backed up.
-   [ ] `.DS_Store` and `.vscode` removed from Git.
-   [ ] `.gitignore` file created and configured.
-   [ ] `frontend` directory created with all HTML, CSS, and JS files.
-   [ ] `docs` directory created with `structure.md`.
-   [ ] `backend` directory contains `app.py` and `requirements.txt`.
-   [ ] `app.py` updated with new `template_folder` and `static_folder` paths.
-   [ ] All changes committed and pushed to the remote repository.
