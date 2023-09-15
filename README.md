1. 1ST TIME SETUP:
   - Navigate to the 'club-site' directory:
     ```bash
     cd club-site
     ```
   - Set up a virtual environment:
     ```bash
     python -m venv env
     ```
   - Open PowerShell as administrator and allow unrestricted execution:
     ```bash
     Set-ExecutionPolicy Unrestricted
     ```
   - Activate the virtual environment and install dependencies:
     ```bash
     .\env\Scripts\activate
     pip install -r requirements.txt
     ```
   - Preview the website:
     ```bash
     .\env\Scripts\activate
     flask --app app.py run
     ```
     A line displaying "Running on http://<address>:<port>" will appear. Hold 'Ctrl' and left click on the link to open it in your browser.

2. RETURNING USERS:
   - Navigate to the 'club-site' directory:
     ```bash
     cd club-site
     ```
   - Preview the website:
     ```bash
     .\env\Scripts\activate
     flask --app app.py run
     ```
     As before, click on the provided link to preview the site.

3. EDITING THE WEBSITE:
   - Backend: Modify the 'app.py' file.
   - HTML: Edit files within the 'templates' directory.
   - CSS: Edit the './static/style.css' file.
     - For assistance with CSS, refer to:
       - [Bootstrap Introduction](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
       - [Bootstrap Examples](https://getbootstrap.com/docs/5.3/examples/)
   - JavaScript: Modify the './static/index.js' file.
   - Database: The account database is located at 'accounts.db'.
   - Dependencies: To add new dependencies, update the 'requirements.txt' file.