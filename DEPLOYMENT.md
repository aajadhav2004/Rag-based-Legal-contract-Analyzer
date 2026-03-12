# Deployment Guide - Render.com

This guide will help you deploy your RAG-based Legal Contract Analyzer to Render.com for free.

## Prerequisites

1. GitHub account with your code pushed
2. MongoDB Atlas account (free tier)
3. Groq API key
4. Render.com account (free)

## Step-by-Step Deployment

### 1. Sign Up for Render

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with your GitHub account

### 2. Create a New Web Service

1. Click "New +" button in the top right
2. Select "Web Service"
3. Connect your GitHub account if not already connected
4. Find and select your repository: `Rag-based-Legal-contract-Analyzer`

### 3. Configure Your Web Service

Fill in the following settings:

**Basic Settings:**

- **Name**: `legal-contract-analyzer` (or any name you prefer)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`

**Build & Deploy:**

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**Instance Type:**

- Select **Free** tier

### 4. Add Environment Variables

Click "Advanced" and add these environment variables:

| Key              | Value                          | Notes                           |
| ---------------- | ------------------------------ | ------------------------------- |
| `GROQ_API_KEY`   | Your Groq API key              | Get from groq.com               |
| `MONGODB_URI`    | Your MongoDB connection string | From MongoDB Atlas              |
| `SECRET_KEY`     | Random secret string           | Generate a secure random string |
| `PYTHON_VERSION` | `3.10.0`                       | Python version                  |

**How to generate SECRET_KEY:**

```python
import secrets
print(secrets.token_hex(32))
```

### 5. Deploy

1. Click "Create Web Service"
2. Wait for the build to complete (5-10 minutes first time)
3. Your app will be live at: `https://your-app-name.onrender.com`

## Important Notes

### Free Tier Limitations

- **Sleep after inactivity**: App sleeps after 15 minutes of no requests
- **Wake-up time**: Takes ~30 seconds to wake up on first request
- **RAM**: 512 MB
- **Build minutes**: 750 hours/month (more than enough)

### MongoDB Atlas Setup

Make sure your MongoDB Atlas is configured:

1. Go to MongoDB Atlas dashboard
2. Click "Network Access"
3. Add IP Address: `0.0.0.0/0` (Allow access from anywhere)
4. This allows Render to connect to your database

### File Uploads

- Uploaded PDFs are stored temporarily
- Files are deleted when the service restarts
- For persistent storage, upgrade to paid plan with disk storage

## Troubleshooting

### Build Fails

**Issue**: Dependencies fail to install
**Solution**: Check requirements.txt has all packages with correct names

### App Crashes on Start

**Issue**: Missing environment variables
**Solution**: Double-check all environment variables are set correctly

### MongoDB Connection Error

**Issue**: Can't connect to MongoDB
**Solution**:

- Verify MONGODB_URI is correct
- Check MongoDB Atlas Network Access allows 0.0.0.0/0
- Ensure MongoDB user has correct permissions

### Groq API Errors

**Issue**: API key not working
**Solution**:

- Verify GROQ_API_KEY is correct
- Check you have API credits remaining
- Ensure no extra spaces in the key

## Monitoring Your App

1. Go to Render dashboard
2. Click on your service
3. View:
   - **Logs**: Real-time application logs
   - **Metrics**: CPU, Memory usage
   - **Events**: Deployment history

## Updating Your App

Render automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update message"
git push origin main
```

Render will automatically detect the push and redeploy.

## Custom Domain (Optional)

1. Go to your service settings
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records as instructed

## Upgrading (If Needed)

If you need:

- No sleep time
- More RAM
- Persistent disk storage
- Faster performance

Consider upgrading to Render's paid plans starting at $7/month.

## Alternative: Railway.app

If Render doesn't work, try Railway:

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables
6. Deploy!

Railway gives $5 free credit monthly (requires credit card but won't charge).

## Support

If you encounter issues:

- Check Render logs for errors
- Review this guide
- Check MongoDB Atlas connection
- Verify all environment variables

---

Good luck with your deployment! 🚀
