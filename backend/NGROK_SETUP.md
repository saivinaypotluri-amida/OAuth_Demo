# 🌐 ngrok Setup Guide

## What is ngrok?

ngrok creates a **secure tunnel** from the internet to your localhost, giving you a public URL for testing webhooks and APIs.

**Perfect for:**
- Testing Slack events locally
- Webhook development
- Showing demos
- Mobile app testing

---

## 📥 Installation

### Option 1: Download Binary (Recommended)

1. **Go to:** https://ngrok.com/download

2. **Select your OS:**
   - Windows
   - macOS  
   - Linux

3. **Download** the zip file

4. **Extract** to a folder (e.g., `C:\ngrok` on Windows)

5. **Add to PATH** (optional):
   - Windows: Add folder to System PATH
   - Mac/Linux: Move to `/usr/local/bin`

---

### Option 2: Install via npm

```bash
npm install -g ngrok
```

---

### Option 3: Install via Chocolatey (Windows)

```bash
choco install ngrok
```

---

## 🔐 Sign Up (Optional but Recommended)

**Why sign up:**
- Longer session times
- Better URLs
- Custom subdomains (paid)
- More concurrent tunnels

**Steps:**
1. Go to: https://dashboard.ngrok.com/signup
2. Sign up (free)
3. Get your authtoken
4. Run: `ngrok authtoken YOUR_AUTHTOKEN`

---

## 🚀 Basic Usage

### Start a Tunnel

**Expose port 8000:**
```bash
ngrok http 8000
```

**You'll see:**
```
ngrok                                              

Session Status: online
Account: Your Name (Plan: Free)
Version: 3.x.x
Region: United States (us)
Latency: 50ms
Web Interface: http://127.0.0.1:4040

Forwarding: https://abc123xyz.ngrok.io -> http://localhost:8000
Forwarding: http://abc123xyz.ngrok.io -> http://localhost:8000

Connections                ttl     opn     rt1     rt5     p50     p90
                           0       0       0.00    0.00    0.00    0.00
```

**Your public URL:** `https://abc123xyz.ngrok.io`

---

## 🎯 Using ngrok with Your App

### For Slack Events:

**After starting ngrok:**

1. **Copy the HTTPS URL** (e.g., `https://abc123xyz.ngrok.io`)

2. **Go to Slack App Settings:**
   - https://api.slack.com/apps → Your App
   - Event Subscriptions
   - Request URL: `https://abc123xyz.ngrok.io/api/slack/events`

3. **Test it:**
   - Slack verifies the endpoint
   - Send message in Slack
   - Bot responds!

---

## 🔍 ngrok Web Interface

**Access the inspector:**
- Open: http://127.0.0.1:4040
- See all requests in real-time
- Inspect request/response details
- Replay requests
- Great for debugging!

---

## ⚙️ Advanced Options

### Custom Subdomain (Paid Plans)

```bash
ngrok http 8000 --subdomain=mybot
# URL: https://mybot.ngrok.io
```

### Specific Region

```bash
ngrok http 8000 --region=eu
# Regions: us, eu, ap, au, sa, jp, in
```

### Basic Auth

```bash
ngrok http 8000 --auth="username:password"
```

### Config File

**Create:** `~/.ngrok2/ngrok.yml`
```yaml
authtoken: YOUR_AUTHTOKEN
tunnels:
  slack-bot:
    addr: 8000
    proto: http
    subdomain: mybot  # Requires paid plan
```

**Start:**
```bash
ngrok start slack-bot
```

---

## 🐛 Troubleshooting

### Issue: "command not found: ngrok"

**Solution:**
- Not in PATH
- Use full path: `C:\ngrok\ngrok.exe http 8000` (Windows)
- Or add to PATH

---

### Issue: "Failed to listen on port"

**Solution:**
- Port 8000 already in use
- Stop backend and restart
- Or use different port: `ngrok http 8001`

---

### Issue: "Session expired"

**Solution:**
- Free tier has time limits
- Sign up and authenticate: `ngrok authtoken YOUR_TOKEN`

---

### Issue: "Too many connections"

**Solution:**
- Free tier limits concurrent tunnels
- Stop other ngrok instances
- Or upgrade to paid plan

---

## 🔄 Workflow

### Development Workflow:

```
Terminal 1: Backend
  cd backend
  python main.py

Terminal 2: ngrok
  ngrok http 8000

Terminal 3: Frontend
  cd frontend
  npm run dev

Browser:
  Slack App Settings (configure webhook URL)
  Your App (use the features)
  Slack (test bot responses)
```

---

## 💡 Tips

**Keep ngrok running:**
- Don't close the ngrok terminal
- URL changes if you restart (free tier)
- Update Slack webhook URL after restart

**View requests:**
- ngrok web interface: http://127.0.0.1:4040
- See all Slack events
- Debug issues

**Save the URL:**
- Write it down temporarily
- Update Slack settings
- Valid until you stop ngrok

**For production:**
- Deploy to cloud
- Use real domain
- No ngrok needed

---

## 📊 What You Get

With ngrok running:
- ✅ Public HTTPS URL
- ✅ Automatic SSL
- ✅ Request inspection
- ✅ Works with webhooks
- ✅ Perfect for development

---

## 🎯 Quick Commands

**Start tunnel:**
```bash
ngrok http 8000
```

**Start with auth:**
```bash
ngrok authtoken YOUR_TOKEN
ngrok http 8000
```

**Check status:**
```bash
curl http://localhost:4040/api/tunnels
```

**Stop:**
```bash
# Press CTRL+C in ngrok terminal
```

---

## 🚀 For Your Slack Bot

**Complete setup:**

```bash
# Terminal 1
cd backend
python main.py

# Terminal 2  
ngrok http 8000
# Copy the HTTPS URL

# Configure in Slack:
# https://YOUR_URL.ngrok.io/api/slack/events

# Test in Slack!
```

---

## 📚 More Info

**ngrok Docs:** https://ngrok.com/docs
**Dashboard:** https://dashboard.ngrok.com/

---

**Ready to expose your local server? Just run `ngrok http 8000`!** 🚀
