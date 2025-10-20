# 🔧 How to Connect Google Workspace (New Flow)

## Overview

Google Workspace integration now works just like Slack and Azure OpenAI - you configure it through the Settings UI!

**Two-Step Process:**
1. **Step 1**: Get and save Google OAuth credentials (Client ID & Secret)
2. **Step 2**: Connect your Google account

---

## Step 1: Get Google OAuth Credentials

### 1.1 Go to Google Cloud Console
Visit: **https://console.cloud.google.com/**

### 1.2 Create a Project
1. Click project dropdown (top left)
2. Click **"NEW PROJECT"**
3. Name: `My AI Bot` (or any name)
4. Click **"CREATE"**

### 1.3 Enable Required APIs
1. Menu → **"APIs & Services"** → **"Library"**
2. Search and enable:
   - ✅ **Google Drive API**
   - ✅ **Google Docs API**

### 1.4 Create OAuth Client ID

**Go to Credentials:**
1. Menu → **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"**
3. Select **"OAuth client ID"**

**Configure Consent Screen (if prompted):**
1. User Type: **External**
2. App name: `My AI Bot`
3. User support email: Your email
4. Developer contact: Your email
5. Click **"SAVE AND CONTINUE"**

6. **Scopes**: Click "ADD OR REMOVE SCOPES"
   - Add: `https://www.googleapis.com/auth/drive.file`
   - Add: `https://www.googleapis.com/auth/drive`
   - Add: `https://www.googleapis.com/auth/documents`
   - Click "UPDATE" → "SAVE AND CONTINUE"

7. **Test users**: Add your email → Click "SAVE AND CONTINUE"

**Create OAuth Client:**
1. Application type: **"Web application"**
2. Name: `OAuth Client`
3. **Authorized redirect URIs**:
   - Click "+ ADD URI"
   - Enter: `http://localhost:8000/api/oauth/google/callback`
   - ⚠️ **EXACT MATCH** - no trailing slash!
4. Click **"CREATE"**

### 1.5 Copy Your Credentials

You'll see a popup with:
```
Client ID: 123456789-abcdef...apps.googleusercontent.com
Client Secret: GOCSPX-xxxxxxxxxxxxx
```

**⚠️ SAVE THESE NOW!** You'll need them in the next step.

---

## Step 2: Configure in Settings UI

### 2.1 Go to Settings
1. Open your app: http://localhost:3000
2. Login
3. Go to **Settings** page

### 2.2 Find "Google OAuth Configuration"
Scroll down to the **"Google OAuth Configuration"** section

### 2.3 Enter Your Credentials

**Fill in the form:**
- **Client ID**: Paste your Client ID (ends with `.apps.googleusercontent.com`)
- **Client Secret**: Paste your Client Secret (starts with `GOCSPX-`)
- **Redirect URI**: Should be pre-filled as `http://localhost:8000/api/oauth/google/callback`

### 2.4 Save and Test
1. Click **"Save OAuth Credentials"**
2. Wait for success message
3. Connection status will show if credentials are valid

---

## Step 3: Connect Google Workspace

Now that OAuth credentials are configured:

### 3.1 Find "Google Workspace Connection"
It's right below the OAuth Configuration section

### 3.2 Click "Connect Google Workspace"
The button is now enabled (was disabled before you saved OAuth creds)

### 3.3 Authorize in Google
1. Browser redirects to Google
2. You see: "My AI Bot wants to access your Google Account"
3. Review permissions (Drive, Docs)
4. Click **"Allow"** or **"Continue"**

### 3.4 Success!
- Redirected back to your app
- See "Connected" status ✅
- Click "Test Connection" to verify

---

## ✅ What to Expect

### Before Configuration:
```
Settings → Google OAuth Configuration
  Status: Not configured
  Button: "Connect Google Workspace" (disabled)
```

### After Step 1 (OAuth Creds Saved):
```
Settings → Google OAuth Configuration
  Status: Pending/Success ✅
  Button: "Connect Google Workspace" (enabled)
```

### After Step 2 (Google Connected):
```
Settings → Google Workspace Connection
  Status: Connected ✅
  Test Connection: Works!
```

---

## 🎯 Testing the Integration

### Test 1: Create a Summary
1. Go to **Summaries** page
2. Click **"Create Summary"**
3. Enter title and content
4. Check ✅ **"Save to Google Drive"**
5. Click **"Create Summary"**
6. You'll get a Google Drive link!

### Test 2: Verify in Google Drive
1. Open the Google Drive link
2. You should see a Google Doc with your summary
3. ✅ Success!

---

## 🐛 Troubleshooting

### Issue: "Please configure Google OAuth credentials in Settings first"

**Cause**: You clicked "Connect" before saving OAuth credentials

**Fix**: 
1. Scroll up to "Google OAuth Configuration"
2. Enter Client ID and Client Secret
3. Click "Save OAuth Credentials"
4. Then click "Connect Google Workspace"

---

### Issue: "Invalid Client ID format"

**Cause**: Client ID doesn't end with `.apps.googleusercontent.com`

**Fix**: 
1. Go back to Google Cloud Console
2. Copy the Client ID again (full string)
3. Make sure it includes `.apps.googleusercontent.com` at the end

---

### Issue: "Invalid Client Secret format"

**Cause**: Client Secret doesn't start with `GOCSPX-`

**Fix**:
1. Verify you copied the Client Secret, not Client ID
2. It should look like: `GOCSPX-xxxxxxxxxxxxxxxx`
3. If you lost it, create a new OAuth client in Google Console

---

### Issue: "Redirect URI mismatch"

**Cause**: Redirect URI in Google Console doesn't match

**Fix**:
1. In Google Console → Credentials → Your OAuth Client
2. Under "Authorized redirect URIs"
3. Make sure it's exactly: `http://localhost:8000/api/oauth/google/callback`
4. No trailing slash, no https for localhost

---

### Issue: Can't find credentials after creating

**Solution**:
1. Go to Google Cloud Console
2. APIs & Services → Credentials
3. Under "OAuth 2.0 Client IDs"
4. Click on your client name
5. You can see Client ID (but not secret again)
6. For secret: Click "RESET SECRET" or create new client

---

## 📊 Summary

| Step | Action | Where |
|------|--------|-------|
| 1 | Get Client ID & Secret | Google Cloud Console |
| 2 | Save OAuth Credentials | Settings UI |
| 3 | Connect Google Workspace | Settings UI |
| 4 | Test Connection | Settings UI |
| 5 | Use in Summaries | Summaries Page |

---

## 🎊 Advantages of This Approach

✅ No need to edit `.env` files
✅ Each user can use their own Google account
✅ Same workflow as Slack and Azure OpenAI
✅ Easy to reconfigure if needed
✅ Works for multiple users
✅ Credentials stored securely in database

---

## 🔐 Security Note

Your Google OAuth credentials are:
- ✅ Encrypted in the database
- ✅ Never exposed in API responses
- ✅ Used only for OAuth flow
- ✅ Separate from your Google account token
- ✅ Can be deleted anytime

---

## ⚡ Quick Reference

**Get Credentials:**
https://console.cloud.google.com/apis/credentials

**Redirect URI:**
`http://localhost:8000/api/oauth/google/callback`

**Required Scopes:**
- `https://www.googleapis.com/auth/drive.file`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/documents`

**Where to Configure:**
Settings → Google OAuth Configuration

**Where to Connect:**
Settings → Google Workspace Connection

---

**That's it! Simple, secure, and consistent with other integrations.** 🚀
