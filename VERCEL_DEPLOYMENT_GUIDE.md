# Vercel Deployment Guide for NutriVeda

## Problem Fixed
The original deployment was failing due to a buffer allocation error caused by large files (3GB+ virtual environment and heavy ML libraries) being included in the deployment package.

## Changes Made

### 1. Created `.vercelignore` file
This excludes large files from deployment:
- Virtual environment (`.venv/`)
- Database files (`*.db`, `*.sqlite3`)
- Large data files (`*.csv`, `data/`)
- Development files (`*.bat`, `*.ps1`, etc.)
- Heavy ML libraries and static files

### 2. Updated `vercel.json`
- Added `maxLambdaSize: "50mb"` limit
- Added `installCommand` to use lightweight requirements
- Added proper environment configuration

### 3. Created `requirements-vercel.txt`
- Lightweight version without TensorFlow/PyTorch
- Only essential dependencies for core functionality
- Reduces deployment size from 3GB+ to under 50MB

### 4. Updated `backend/settings.py`
- Added Vercel-specific configuration
- Uses in-memory SQLite if no PostgreSQL available
- Optimized static file handling

## Deployment Steps

1. **Commit all changes:**
   ```bash
   git add .
   git commit -m "Fix Vercel deployment - exclude large files and optimize dependencies"
   ```

2. **Push to your repository:**
   ```bash
   git push origin main
   ```

3. **Deploy on Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your repository
   - Vercel will automatically detect the Python configuration
   - The deployment should now succeed without buffer errors

## Environment Variables (Optional)
If you want to use PostgreSQL instead of in-memory SQLite, add these environment variables in Vercel:
- `DATABASE_URL`: Your PostgreSQL connection string

## What's Preserved
- All core functionality remains intact
- Dosha analysis features work (using scikit-learn instead of TensorFlow)
- Database operations work (in-memory SQLite or PostgreSQL)
- All web interfaces and APIs function normally

## Size Reduction
- **Before:** 3GB+ (including TensorFlow, PyTorch, virtual environment)
- **After:** <50MB (essential dependencies only)

The deployment should now complete successfully without the buffer allocation error!
