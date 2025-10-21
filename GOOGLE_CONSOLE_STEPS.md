# 📸 Google Cloud Console - Visual Guide

## Step-by-Step with Exact Clicks

### Step 1: Access Google Cloud Console

**URL:** https://console.cloud.google.com/

**What you'll see:** Google Cloud Console homepage

---

### Step 2: Create/Select Project

**Action:** 
1. Click the project dropdown (top left, next to "Google Cloud")
2. Click **"NEW PROJECT"**

**Fill in:**
- Project name: `Agentic-AI-Bot` (or your choice)
- Click **"CREATE"**
- Wait for project to be created (few seconds)
- Make sure it's selected in the project dropdown

---

### Step 3: Enable Google Drive API

**Navigation:**
1. Click hamburger menu (☰) in top left
2. Hover over **"APIs & Services"**
3. Click **"Library"**

**In the Library:**
1. Search box: Type `Google Drive API`
2. Click on **"Google Drive API"** (by Google)
3. Click blue **"ENABLE"** button
4. Wait for it to enable (few seconds)

---

### Step 4: Enable Google Docs API

**Still in Library:**
1. Search box: Type `Google Docs API`
2. Click on **"Google Docs API"** (by Google)
3. Click blue **"ENABLE"** button
4. Wait for it to enable

---

### Step 5: Go to Credentials

**Navigation:**
1. Click hamburger menu (☰)
2. **"APIs & Services"** → **"Credentials"**

**You should see:** Credentials page with a + CREATE CREDENTIALS button at top

---

### Step 6: Configure OAuth Consent Screen (First Time Only)

**If you see a banner saying "To create an OAuth client ID, you must first configure your consent screen":**

1. Click **"CONFIGURE CONSENT SCREEN"**

**Choose User Type:**
- Select **"External"** (unless you have Google Workspace, then "Internal")
- Click **"CREATE"**

**OAuth consent screen - App information:**
```
App name: Agentic AI Slack Bot
User support email: [Your email - use dropdown]
App logo: [Skip this]
Application home page: [Leave empty]
Application privacy policy link: [Leave empty]
Application terms of service link: [Leave empty]
Authorized domains: [Leave empty]
Developer contact information: [Your email]
```
- Click **"SAVE AND CONTINUE"**

**Scopes:**
1. Click **"ADD OR REMOVE SCOPES"**
2. In the filter box, search: `drive`
3. Check these boxes:
   - ✅ `.../auth/drive.file` (See, edit, create, and delete only specific files)
   - ✅ `.../auth/drive` (See, edit, create, and delete all files)
4. Search: `documents`
5. Check:
   - ✅ `.../auth/documents` (See, edit, create, and delete documents)
6. Click **"UPDATE"** (bottom right)
7. Scroll down
8. Click **"SAVE AND CONTINUE"**

**Test users:**
1. Click **"+ ADD USERS"**
2. Enter your email address
3. Click **"ADD"**
4. Click **"SAVE AND CONTINUE"**

**Summary:**
- Review and click **"BACK TO DASHBOARD"**

---

### Step 7: Create OAuth Client ID

**Back at Credentials page:**
1. Click **"+ CREATE CREDENTIALS"** (top of page)
2. Select **"OAuth client ID"**

**Create OAuth client ID form:**
```
Application type: [Dropdown] → Select "Web application"

Name: Agentic AI Bot OAuth

Authorized JavaScript origins:
  [Leave empty or add http://localhost:3000 if you want]

Authorized redirect URIs:
  Click "+ ADD URI"
  Enter: http://localhost:8000/api/oauth/google/callback
  ⚠️ EXACT MATCH REQUIRED - no trailing slash!
```

3. Click **"CREATE"** (bottom)

---

### Step 8: Copy Your Credentials

**You'll see a popup: "OAuth client created"**

```
Your Client ID:
  123456789-abcdefghijklmnop.apps.googleusercontent.com
  [Click the copy icon]

Your Client Secret:
  GOCSPX-xxxxxxxxxxxxxxxxxxxx
  [Click the copy icon]
```

**IMPORTANT:** Save these somewhere safe! You'll need them in the next step.

You can always come back and see:
- Client ID: Visible anytime
- Client Secret: Only shown once, but you can create new ones

Click **"OK"** to close the popup

---

### Step 9: Find Your Credentials Later

If you need to find them again:

1. Go to **"APIs & Services"** → **"Credentials"**
2. Under **"OAuth 2.0 Client IDs"** section
3. You'll see your client (name: "Agentic AI Bot OAuth")
4. Click on the name
5. You can see:
   - Client ID ✅ (visible)
   - Client secret ⚠️ (not shown after creation)
6. If you lost the secret:
   - Click **"ADD SECRET"** to create a new one
   - Or delete and recreate the OAuth client

---

## ✅ Verification Checklist

After completing all steps, verify:

- [ ] Project created and selected
- [ ] Google Drive API enabled
- [ ] Google Docs API enabled
- [ ] OAuth consent screen configured
- [ ] Test user (your email) added
- [ ] OAuth Client ID created
- [ ] Redirect URI is: `http://localhost:8000/api/oauth/google/callback`
- [ ] Client ID copied
- [ ] Client Secret copied

---

## 📋 What to Do with Credentials

### Copy to .env file:

1. Open `backend/.env`
2. Add:
```env
GOOGLE_CLIENT_ID=123456789-abc.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your-secret-here
GOOGLE_REDIRECT_URI=http://localhost:8000/api/oauth/google/callback
```
3. Replace with YOUR actual values
4. Save file

### Restart Backend:
```bash
# Press CTRL+C in backend terminal
python main.py
```

### Test Connection:
1. Go to http://localhost:3000/settings
2. Click "Connect Google Workspace"
3. Should redirect to Google
4. Click "Allow"
5. Returns to your app
6. Shows "Connected" ✅

---

## 🆘 Common Mistakes

### ❌ Wrong redirect URI
**Problem:** `redirect_uri_mismatch` error

**Fix:** 
- In Google Console, redirect URI must be EXACTLY:
  `http://localhost:8000/api/oauth/google/callback`
- No trailing slash
- No https (for localhost)
- Exact port 8000

### ❌ Forgot to enable APIs
**Problem:** API not found errors

**Fix:**
- Go to "APIs & Services" → "Library"
- Enable both Google Drive API and Google Docs API

### ❌ Didn't add test user
**Problem:** "Access blocked: This app's request is invalid"

**Fix:**
- Go to "OAuth consent screen"
- Scroll to "Test users"
- Add your email

### ❌ Client Secret not saved
**Problem:** Lost the secret after closing popup

**Fix:**
- Go to Credentials
- Click on your OAuth client
- Click "ADD SECRET" or create new client

---

## 🎯 Success Indicators

You'll know it worked when:
- ✅ No 500 error when clicking "Connect"
- ✅ Google OAuth page loads
- ✅ Shows your app name "Agentic AI Slack Bot"
- ✅ Shows permissions for Drive and Docs
- ✅ After allowing, returns to your app
- ✅ Settings shows "Connected" status

---

**Need more help?** See `GOOGLE_OAUTH_SETUP.md` for detailed explanations.
