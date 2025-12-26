# Saleor Installation Guide

## Installation Methods

Saleor is typically installed by cloning the repository, not via pip. Here are the recommended approaches:

### Method 1: Clone Saleor Repository (Recommended)

```bash
cd backend
# Clone Saleor repository
git clone https://github.com/saleor/saleor.git saleor_temp
cd saleor_temp

# Copy Saleor source to your project
# Or install it as an editable package
pip install -e .

cd ..
```

### Method 2: Install from GitHub

```bash
cd backend
source venv/bin/activate

# Install directly from GitHub
pip install git+https://github.com/saleor/saleor.git@3.20

# Or install specific version
pip install git+https://github.com/saleor/saleor.git@main
```

### Method 3: Manual Setup (For Custom Integration)

1. **Clone Saleor repository:**
   ```bash
   cd /tmp  # or another location
   git clone https://github.com/saleor/saleor.git
   cd saleor
   ```

2. **Copy Saleor source to your project:**
   ```bash
   # Copy saleor package to your backend directory
   cp -r saleor /path/to/your/backend/
   ```

3. **Install dependencies:**
   ```bash
   cd /path/to/your/backend
   pip install -r saleor/requirements.txt
   ```

### Method 4: Use Saleor's Installation Script

Follow Saleor's official installation guide:
- https://docs.saleor.io/docs/3.x/developer/installation

## Recommended Approach for This Project

Since you're integrating custom extensions, I recommend:

1. **Clone Saleor separately** (for reference):
   ```bash
   cd ~/  # or another location
   git clone https://github.com/saleor/saleor.git saleor-reference
   ```

2. **Install Saleor as a package** (if using pip from GitHub):
   ```bash
   cd backend
   source venv/bin/activate
   pip install git+https://github.com/saleor/saleor.git
   ```

3. **OR integrate Saleor source directly** into your project structure:
   ```bash
   # This creates saleor/ directory in your backend
   cd backend
   git clone https://github.com/saleor/saleor.git saleor
   cd saleor
   pip install -e .
   ```

## After Installation

1. **Verify installation:**
   ```bash
   python -c "import saleor; print(saleor.__version__)"
   ```

2. **Check Saleor structure:**
   ```bash
   python -c "import saleor; import os; print(os.path.dirname(saleor.__file__))"
   ```

3. **Proceed with integration:**
   - Update settings (see `saleor_settings_integration.py`)
   - Update models (see `MODEL_UPDATES.md`)
   - Run migrations

## Important Notes

- Saleor requires PostgreSQL database
- Saleor requires Redis
- Make sure Python version is 3.11+ (though 3.9 might work)
- Follow Saleor's official documentation for full setup

## Troubleshooting

### If pip install fails:
- Try installing from GitHub: `pip install git+https://github.com/saleor/saleor.git`
- Check Python version: `python --version` (should be 3.11+)
- Upgrade pip: `pip install --upgrade pip`

### If import fails after installation:
- Check virtual environment is activated
- Verify installation: `pip list | grep saleor`
- Check Python path: `python -c "import sys; print(sys.path)"`

## Next Steps After Installation

1. ✅ Verify Saleor is installed
2. ✅ Initialize Saleor project structure (if needed)
3. ✅ Update settings.py with your extensions
4. ✅ Update models with ForeignKeys
5. ✅ Run migrations
6. ✅ Test integration


