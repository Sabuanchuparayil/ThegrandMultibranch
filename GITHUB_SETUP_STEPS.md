# GitHub Repository Setup - Step by Step

## Quick Setup Guide

### Step 1: Create GitHub Repository

1. **Go to GitHub**: https://github.com
2. **Sign in** to your account
3. **Click** the "+" icon in top right → **"New repository"**
4. **Fill in details**:
   ```
   Repository name: grand-gold-multibranch
   Description: Multi-branch jewellery e-commerce platform with Saleor backend and Next.js frontend
   Visibility: Private (recommended for production) or Public
   
   ✅ Initialize this repository with:
   - [ ] Add a README file (optional - we have one)
   - [x] Add .gitignore: Node (or Python)
   - [ ] Choose a license (optional)
   ```
5. **Click** "Create repository"

### Step 2: Initialize Local Repository

Open terminal and run:

```bash
# Navigate to your project directory
cd "/Users/apple/Desktop/Grand Gold/The grand-Multibranch"

# Check if git is already initialized
git status

# If not initialized, initialize it
git init

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/grand-gold-multibranch.git

# Replace YOUR_USERNAME with your GitHub username
```

### Step 3: Stage and Commit Files

```bash
# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Multi-branch jewellery e-commerce platform

- Saleor backend with 20 custom extension modules
- Next.js admin dashboard with 12 modules
- Next.js customer storefront
- GraphQL API for inventory and branch management
- Multi-region and multi-currency support
- Railway deployment configuration"

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 4: Verify Repository

1. Go to your GitHub repository page
2. Verify all files are uploaded
3. Check that `.gitignore` is working (node_modules, .env, etc. should not be visible)

## Repository Structure

Your GitHub repository should contain:

```
grand-gold-multibranch/
├── backend/
│   ├── saleor/
│   ├── saleor_extensions/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   └── ...
├── frontend/
│   ├── admin/
│   ├── storefront/
│   └── shared/
├── docs/
├── .gitignore
├── README.md
└── RAILWAY_AND_GITHUB_SETUP.md
```

## GitHub Settings

### Branch Protection (Recommended for Production)

1. Go to repository **Settings** → **Branches**
2. Add rule for `main` branch:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1)
   - ✅ Require status checks to pass

### GitHub Secrets (For CI/CD)

If you want to automate deployments:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add secrets:
   - `RAILWAY_TOKEN`
   - `DATABASE_URL`
   - `SECRET_KEY`

## Next Steps

After GitHub setup:

1. ✅ Connect to Railway (see RAILWAY_AND_GITHUB_SETUP.md)
2. ✅ Set up environment variables
3. ✅ Deploy services
4. ✅ Configure domain

---

**Your repository URL**: `https://github.com/YOUR_USERNAME/grand-gold-multibranch`

