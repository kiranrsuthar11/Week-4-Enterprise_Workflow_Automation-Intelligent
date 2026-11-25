# Publish this project to GitHub (Windows)

1. Create a new **public** repository on GitHub named `PY-W4-004`. Do not initialize it with a README, license, or .gitignore if uploading this existing folder.
2. Open PowerShell in the extracted `PY-W4-004` project folder.
3. Run these commands (replace the URL with your own repository URL):

```powershell
git init
git add .
git status
git commit -m "Submit Week 4 Python workflow automation project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/PY-W4-004.git
git push -u origin main
```

4. Open the repository in a browser and copy its URL into the submission email.
5. Never commit `.env`, passwords, API tokens, real employee data, or confidential documents. The supplied `.gitignore` should exclude local secrets and runtime files; review `git status` before committing.
