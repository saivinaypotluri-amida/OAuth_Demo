# 🔧 Google Workspace OAuth Setup Guide

## Why You're Getting 500 Error

The error message is:
```
"Google OAuth not configured. Please set up Google credentials in the admin panel."
```

This means your `backend/.env` file doesn't have Google OAuth credentials configured.

---

## 📋 Step-by-Step Setup

### Step 1: Get Google OAuth Credentials

#### 1.1 Go to Google Cloud Console
Visit: https://console.cloud.google.com/

#### 1.2 Create or Select Project
- Click "Select a project" at the top
- Click "NEW PROJECT"
- Name it: "Agentic AI Slack Bot" (or your preferred name)
- Click "CREATE"

#### 1.3 Enable Required APIs
1. In the left sidebar, go to **"APIs & Services"** → **"Library"**
2. Search for and enable these APIs:
   - **Google Drive API** - Click "ENABLE"
   - **Google Docs API** - Click "ENABLE"

#### 1.4 Create OAuth Credentials
1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"OAuth client ID"**

4. **Configure OAuth Consent Screen** (if prompted):
   - User Type: **External** (or Internal if you have Google Workspace)
   - Click **"CREATE"**
   
   - **App information**:
     - App name: `Agentic AI Slack Bot`
     - User support email: Your email
     - Developer contact: Your email
   - Click **"SAVE AND CONTINUE"**
   
   - **Scopes**: Click **"ADD OR REMOVE SCOPES"**
     - Add these scopes:
       - `https://www.googleapis.com/auth/drive.file`
       - `https://www.googleapis.com/auth/drive`
       - `https://www.googleapis.com/auth/documents`
     - Click **"UPDATE"**
     - Click **"SAVE AND CONTINUE"**
   
   - **Test users** (if External):
     - Click **"+ ADD USERS"**
     - Add your email address
     - Click **"SAVE AND CONTINUE"**

5. **Create OAuth Client ID**:
   - Application type: **"Web application"**
   - Name: `Agentic AI Bot`
   
   - **Authorized redirect URIs**:
     - Click **"+ ADD URI"**
     - Enter: `http://localhost:8000/api/oauth/google/callback`
     - Click **"CREATE"**

6. **Copy Your Credentials**:
   - You'll see a popup with:
     - **Client ID**: Starts with something like `123456789-abc...apps.googleusercontent.com`
     - **Client Secret**: Random string like `GOCSPX-...`
   - **SAVE THESE!** You'll need them in the next step

---

### Step 2: Configure Backend Environment

#### 2.1 Open Your `.env` File
Navigate to: `backend/.env`

If it doesn't exist, copy from example:
```bash
cd backend
cp .env.example .env
```

#### 2.2 Add Google Credentials
Open `backend/.env` in a text editor and add/update these lines:

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
GOOGLE_REDIRECT_URI=http://localhost:8000/api/oauth/google/callback
```

**Replace:**
- `YOUR_CLIENT_ID_HERE` with your actual Client ID
- `YOUR_CLIENT_SECRET_HERE` with your actual Client Secret

**Example:**
```env
GOOGLE_CLIENT_ID=123456789-abcdefghijk.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwx
GOOGLE_REDIRECT_URI=http://localhost:8000/api/oauth/google/callback
```

#### 2.3 Save the File

---

### Step 3: Restart Backend

**IMPORTANT**: You must restart the backend to load the new environment variables!

```bash
# In your backend terminal:
# Press CTRL+C to stop

# Restart:
python main.py
```

---

### Step 4: Test Google OAuth Connection

1. **Go to your frontend**: http://localhost:3000

2. **Login** with your credentials

3. **Go to Settings**

4. **Scroll to "Google Workspace Configuration"**

5. **Click "Connect Google Workspace"**

6. **What should happen**:
   - ✅ Browser redirects to Google OAuth page
   - ✅ You see app name and requested permissions
   - ✅ Click "Allow" or "Continue"
   - ✅ Redirected back to your app
   - ✅ See "OAuth success" message
   - ✅ Connection status shows "Connected"

---

## 🐛 Troubleshooting

### Issue: Still getting 500 error

**Solution:**
1. Verify `.env` file has the correct credentials
2. Make sure there are no extra spaces in the values
3. Restart the backend: `python main.py`
4. Check backend logs for specific error

### Issue: "Redirect URI mismatch" error

**Solution:**
1. Go to Google Cloud Console → Credentials
2. Edit your OAuth Client ID
3. Make sure redirect URI is exactly: `http://localhost:8000/api/oauth/google/callback`
4. No trailing slash, exact match

### Issue: "Access blocked: This app is not verified"

**Solution:**
This is normal for development!
1. Click "Advanced" (at bottom left)
2. Click "Go to [App Name] (unsafe)"
3. Click "Continue"

For production, you'd need to verify your app.

### Issue: Can't see the credentials

**Solution:**
Check if you saved them. If not:
1. Go to Google Cloud Console → Credentials
2. Click on your OAuth 2.0 Client ID
3. You can see Client ID (but not secret again)
4. If you lost the secret, create a new client ID

---

## ✅ Verification Checklist

Before clicking "Connect":
- [ ] Created Google Cloud Project
- [ ] Enabled Google Drive API
- [ ] Enabled Google Docs API
- [ ] Created OAuth Client ID
- [ ] Copied Client ID and Secret
- [ ] Updated `backend/.env` file
- [ ] Added correct redirect URI in Google Console
- [ ] Restarted backend
- [ ] Backend logs show no errors

---

## 📊 Expected Backend Logs

After successful OAuth:

```
INFO: GET /api/oauth/google/authorize → 200 OK
# (Browser redirects to Google)
# (User authorizes)
# (Google redirects back)
INFO: GET /api/oauth/google/callback → 307 Temporary Redirect
# (Backend saves credentials and redirects to frontend)
```

---

## 🎯 After Successful Connection

Once connected:
- ✅ Test connection in Settings
- ✅ Create a summary
- ✅ Choose "Save to Google Drive"
- ✅ Summary gets saved as Google Doc
- ✅ You get a shareable link

---

## 📝 Example `.env` File

Here's what your `backend/.env` should look like:

```env
# Application Settings
APP_NAME="Agentic AI Slack Bot"
APP_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///./slack_ai_bot.db

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# JWT Configuration
JWT_SECRET_KEY=jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Google OAuth Configuration (REQUIRED FOR GOOGLE WORKSPACE)
GOOGLE_CLIENT_ID=123456789-abc123def456.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your-secret-here
GOOGLE_REDIRECT_URI=http://localhost:8000/api/oauth/google/callback

# Slack Configuration (Optional - configure via Settings UI)
# SLACK_BOT_TOKEN=xoxb-your-bot-token
# SLACK_SIGNING_SECRET=your-signing-secret

# Azure OpenAI Configuration (Optional - configure via Settings UI)
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_API_KEY=your-api-key
# AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

---

## 🎊 Summary

**What you need:**
1. Google Cloud Project
2. OAuth Client ID credentials
3. Update `backend/.env`
4. Restart backend
5. Click "Connect Google Workspace"

**Time needed:** 5-10 minutes (first time)

**Cost:** FREE (Google Cloud free tier is sufficient)

---

## 🆘 Need Help?

If you're stuck:
1. Check the exact error in backend logs
2. Verify your `.env` file formatting
3. Make sure backend was restarted
4. Check redirect URI matches exactly

---

**Once configured, Google OAuth will work seamlessly for all users!** 🚀
