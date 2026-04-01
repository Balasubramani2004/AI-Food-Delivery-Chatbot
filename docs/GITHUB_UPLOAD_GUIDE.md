# 🚀 GitHub Upload Guide - FoodieBot

## Step-by-Step Instructions to Upload Your Project

---

## 📋 Prerequisites

Before uploading, ensure you have:
- ✅ **Git installed** ([download](https://git-scm.com/download/win))
- ✅ **GitHub account** ([create here](https://github.com/signup))
- ✅ **Project cleaned** (unnecessary files deleted)
- ✅ **README.md updated** (with project details)

---

## 🎯 Step 1: Create GitHub Repository

### **Option A: Via GitHub Website**

1. Go to [https://github.com/new](https://github.com/new)
2. **Repository name:** `FoodieBot` (or your choice)
3. **Description:** Smart Food Delivery Chatbot with ML Intent Detection
4. **Visibility:** Public (to share) or Private
5. **Add README:** ❌ NO (we have our own)
6. **Add .gitignore:** ❌ NO (we have our own)
7. **Add License:** ✅ YES - Choose **MIT License**
8. Click **"Create repository"**

### **After Creating:**
- You'll see a repository URL like:
  ```
  https://github.com/YOUR_USERNAME/FoodieBot.git
  ```
  OR
  ```
  git@github.com:YOUR_USERNAME/FoodieBot.git
  ```

✅ **Copy this URL - you'll need it**

---

## 🔧 Step 2: Initialize Git (if not already done)

Open **PowerShell** in your project directory:

```powershell
cd "c:\Users\BALASUBRAMANI M\OneDrive\class web\Food Delivery Chatbot"

# Check if git is already initialized
git status
```

**If you see an error** ("not a git repository"):

```powershell
# Initialize git
git init

# Set your Git name and email
git config user.name "Your Name"
git config user.email "your.email@example.com"

# (Optional) Set globally so you don't repeat this
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 📝 Step 3: Add Remote Repository

```powershell
# Add the GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/FoodieBot.git

# Verify it was added
git remote -v
```

**Expected output:**
```
origin  https://github.com/YOUR_USERNAME/FoodieBot.git (fetch)
origin  https://github.com/YOUR_USERNAME/FoodieBot.git (push)
```

---

## 📦 Step 4: Stage All Files

```powershell
# Stage all files
git add .

# Check what will be committed
git status
```

**Expected output:**
```
On branch master
Changes to be committed:
  new file:   README.md
  new file:   app.py
  new file:   chatbot.py
  ...
```

---

## 💾 Step 5: Create First Commit

```powershell
# Commit with a message
git commit -m "Initial commit: FoodieBot - Smart Food Delivery Chatbot with ML"
```

**Or more detailed:**
```powershell
git commit -m "Initial commit: FoodieBot

- Hybrid ML + rule-based intent detection
- Flask web server with REST APIs
- Glassmorphism UI chatbot interface
- Order management and tracking
- 91% accuracy on 12 intent classes
- Complete documentation and evaluation metrics"
```

---

## 🚀 Step 6: Push to GitHub

```powershell
# Push to GitHub
git push -u origin master
```

⚠️ **Note:** GitHub may ask for authentication:

### **Authentication Option 1: SSH Key** (Recommended)
- Already generated? → It will push directly
- Need to generate? → Follow [GitHub SSH guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

### **Authentication Option 2: Personal Access Token (PAT)**
1. Go to GitHub Settings → [Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Create new token with "repo" scope
3. Copy the token
4. When prompted for password, paste the token
5. Push will complete

### **Authentication Option 3: HTTPS** (Simplest)
1. When prompted, enter your GitHub username
2. When prompted for password, enter your **Personal Access Token** (not your password)
3. On Windows, you may get a credential manager popup - save your credentials

---

## ✅ Verify Upload

### **In PowerShell:**
```powershell
# Check git log
git log --oneline

# Check remote
git remote -v
```

### **In Browser:**
1. Go to `https://github.com/YOUR_USERNAME/FoodieBot`
2. Verify all files are visible:
   - ✅ README.md
   - ✅ app.py, chatbot.py, ml_intent_detector.py
   - ✅ docs/ folder with all subfolders
   - ✅ templates/index.html

---

## 🎯 Complete Quick Command (All-in-One)

If git is already initialized:

```powershell
cd "c:\Users\BALASUBRAMANI M\OneDrive\class web\Food Delivery Chatbot"

git add .

git commit -m "Initial commit: FoodieBot - Smart Food Delivery Chatbot with ML"

git push -u origin master
```

---

## 🐛 Troubleshooting

### **Problem: "fatal: not a git repository"**
**Solution:**
```powershell
git init
git remote add origin https://github.com/YOUR_USERNAME/FoodieBot.git
```

### **Problem: "error: src refspec master does not match any"**
**Solution:** (Branch might be named "main")
```powershell
git push -u origin HEAD:main
```

### **Problem: "Permission denied (publickey)"**
**Solution:** Use HTTPS instead of SSH, or [add SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

### **Problem: "refusing to merge unrelated histories"**
**Solution:**
```powershell
git pull origin master --allow-unrelated-histories
git push origin master
```

### **Problem: Authentication keeps failing**
**Solution:**
1. Generate Personal Access Token: [GitHub → Settings → Tokens](https://github.com/settings/tokens)
2. Use token as password when prompted
3. Or use SSH key authentication

---

## 📊 After Upload - Next Steps

### **1. Share Your Repository**
- Copy the GitHub URL
- Share on social media, portfolio, resume
- Example: `https://github.com/YOUR_USERNAME/FoodieBot`

### **2. Add GitHub Badge to README**
```markdown
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
```

### **3. Enable Discussions** (Optional)
- GitHub → Settings → Discussions → Enable

### **4. Add Topics** (Optional)
- GitHub → About (gear icon) → Topics
- Add: `chatbot`, `nlp`, `ml`, `flask`, `food-delivery`

### **5. Pin Repository** (If you have multiple)
- GitHub Profile → Customize your pins
- Pin FoodieBot

---

## 📚 Recommended Additional Files

### **Optional: Add LICENSE file**
```
MIT License - Already selected during repo creation
Check if LICENSE file exists in your repo
```

### **Optional: Add .github/workflows/** for CI/CD
```
(Advanced - for automated testing)
```

### **Optional: Add CONTRIBUTING.md**
```
Guidelines for others to contribute
```

---

## 📈 GitHub Repository Stats

After upload, your repository will show:
- ✅ Code
- ✅ Issues (if anyone finds bugs)
- ✅ Pull Requests (if anyone contributes)
- ✅ Stars (if people like it)
- ✅ Forks (if people copy it)
- ✅ Commit history
- ✅ Network graph
- ✅ Insights

---

## 🎓 Team Sharing

Once uploaded, share the link with your team:

### **Survey Team:**
`https://github.com/YOUR_USERNAME/FoodieBot` → docs/team/SURVEY_TABLE.csv

### **Review Team:**
`https://github.com/YOUR_USERNAME/FoodieBot` → docs/team/REVIEW_TABLE.csv

### **Coding Team:**
`https://github.com/YOUR_USERNAME/FoodieBot` → Source code analysis

### **PPT Team:**
`https://github.com/YOUR_USERNAME/FoodieBot` → docs/PROJECT_BRIEF.md

---

## ✨ Final Checklist

Before uploading:
- [ ] All unnecessary files deleted
- [ ] README.md updated and ready
- [ ] .gitignore configured
- [ ] docs/ folder complete
- [ ] requirements.txt has all dependencies
- [ ] app.py, chatbot.py, ml_intent_detector.py present
- [ ] templates/index.html present

After uploading:
- [ ] Repository visible on GitHub
- [ ] All files accessible
- [ ] README renders correctly
- [ ] Code highlighted properly
- [ ] docs/ structure visible
- [ ] Clone URL ready to share

---

## 🚀 That's It!

Your FoodieBot is now on GitHub! 🎉

**GitHub URL:** `https://github.com/YOUR_USERNAME/FoodieBot`

Share it with:
- Your team
- Your resume/portfolio
- GitHub profile
- Social media
- Job applications

---

## 📞 Need Help?

**GitHub Documentation:**
- [Hello World](https://guides.github.com/activities/hello-world/)
- [Fork a Repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
- [Pushing to a Remote](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository)

---

**Congratulations on uploading FoodieBot!** 🌟

**Last Updated:** April 1, 2026
