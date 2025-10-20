# 🚀 Slack Real-Time Bot Setup Guide

## What You're Adding

Your bot will now:
- ✅ **Listen to messages** in Slack channels
- ✅ **Respond automatically** with AI-generated answers
- ✅ **Reply when mentioned** with @bot
- ✅ **Work in real-time** in your Slack workspace

---

## 🔄 Step 1: Restart Backend

The event handler is already added to the code!

```bash
# In your backend terminal:
# Press CTRL+C

# Restart:
python main.py
```

**Verify it started:**
```
INFO: Application startup complete.
```

---

## 🌐 Step 2: Expose Your Local Server

Slack needs a **public URL** to send events to your local backend.

### Option A: Using ngrok (Recommended for Testing)

#### Install ngrok:
**Download from:** https://ngrok.com/download

**Or install via npm:**
```bash
npm install -g ngrok
```

#### Start ngrok:
```bash
ngrok http 8000
```

**You'll see:**
```
Session Status: online
Forwarding: https://abc123xyz.ngrok.io -> http://localhost:8000
```

**📋 Copy the HTTPS URL:** `https://abc123xyz.ngrok.io`

**⚠️ Important:**
- Keep ngrok running while testing
- The URL changes each time you restart ngrok (free tier)
- For permanent URL, upgrade to ngrok paid plan

---

### Option B: Using serveo (Alternative)

```bash
ssh -R 80:localhost:8000 serveo.net
```

Copy the provided URL.

---

### Option C: Deploy to Cloud (Production)

For permanent deployment:
- Heroku: `https://your-app.herokuapp.com`
- AWS/GCP/Azure: Your domain
- See `DEPLOYMENT.md` for details

---

## 🔧 Step 3: Configure Slack App for Events

### 3.1 Go to Your Slack App

1. Visit: https://api.slack.com/apps
2. Select your app (or create new one if needed)

---

### 3.2 Enable Event Subscriptions

1. **Click "Event Subscriptions"** in sidebar

2. **Toggle "Enable Events" to ON**

3. **Request URL:**
   - Enter: `https://your-ngrok-url.ngrok.io/api/slack/events`
   - Example: `https://abc123xyz.ngrok.io/api/slack/events`
   - Wait for ✅ "Verified" checkmark

**If verification fails:**
- Check your backend is running
- Check ngrok is running
- Check the URL is correct (no trailing slash)
- Check backend logs for errors

4. **Scroll to "Subscribe to bot events"**

5. **Click "Add Bot User Event"** and add:
   - ✅ `message.channels` - Messages in public channels
   - ✅ `message.groups` - Messages in private channels
   - ✅ `message.im` - Direct messages to bot
   - ✅ `app_mention` - When bot is @mentioned

6. **Click "Save Changes"** at bottom

7. **Slack will prompt:** "Reinstall your app"
   - Click **"reinstall your app"** link
   - Click **"Allow"**

---

### 3.3 Update OAuth Scopes (If Needed)

1. **Click "OAuth & Permissions"** in sidebar

2. **Bot Token Scopes** - Make sure you have:
   - ✅ `chat:write` - Send messages
   - ✅ `chat:write.public` - Send to channels bot isn't in
   - ✅ `channels:history` - Read channel messages
   - ✅ `channels:read` - View channels
   - ✅ `groups:history` - Read private channel messages
   - ✅ `im:history` - Read DMs
   - ✅ `im:write` - Send DMs
   - ✅ `users:read` - Read user info
   - ✅ `app_mentions:read` - See mentions

3. **If you added scopes:**
   - Click **"Reinstall to Workspace"** at top
   - Click **"Allow"**

4. **Copy your Bot Token** (starts with `xoxb-`)

---

### 3.4 Update Credentials in Your App

1. **Go to:** http://localhost:3000/settings

2. **Slack Configuration:**
   - Bot Token: `xoxb-your-token`
   - Signing Secret: From Slack app "Basic Information"
   - Click "Save Credentials"
   - Click "Test Connection"

---

## 🧪 Step 4: Test Real-Time Bot

### Test 1: Message in Channel

1. **In Slack:**
   - Go to any channel where bot is added
   - Type: `Hello bot!`
   - Press Enter

2. **Expected:**
   - Bot responds automatically with AI-generated message ✅
   - Response appears in same channel
   - Conversation is logged in database

3. **Backend Logs:**
   ```
   INFO: POST /api/slack/events → 200 OK
   INFO: Processing message from user U123 in channel C456
   INFO: Successfully responded to message in channel C456
   ```

---

### Test 2: Mention the Bot

1. **In Slack:**
   - In any channel, type: `@YourBot can you help me with Python?`
   - Press Enter

2. **Expected:**
   - Bot responds with AI answer ✅
   - Tagged you in the response

---

### Test 3: Direct Message

1. **In Slack:**
   - Click on your bot in Apps section
   - Send a DM: `What can you do?`

2. **Expected:**
   - Bot responds in DM ✅
   - Private conversation tracked

---

## 📊 What Gets Logged

Every Slack interaction logs:
- Message content
- AI response
- Channel/User info
- Token usage
- Response time
- Stored in database

**View in:**
- Messages page (web portal)
- Admin Dashboard (statistics)
- Admin Logs (audit trail)

---

## 🎯 Testing Checklist

- [ ] Backend restarted with new code
- [ ] ngrok running and URL copied
- [ ] Slack app Event Subscriptions configured
- [ ] Request URL verified
- [ ] Bot events subscribed
- [ ] App reinstalled to workspace
- [ ] Slack credentials saved in Settings
- [ ] Azure OpenAI configured (for AI responses)
- [ ] Test connection successful
- [ ] Bot added to test channel
- [ ] Sent message in channel
- [ ] Bot responded automatically

---

## 🐛 Troubleshooting

### Issue: Slack verification fails

**Check:**
- Backend is running
- ngrok is running
- URL is correct: `https://your-ngrok.ngrok.io/api/slack/events`
- No trailing slash
- Backend accessible from internet

**Test manually:**
```bash
curl https://your-ngrok.ngrok.io/health
# Should return: {"status":"healthy"}
```

---

### Issue: Bot doesn't respond to messages

**Check:**
1. **Slack credentials configured:**
   - Settings → Slack → Test Connection → Success ✅

2. **Azure OpenAI configured:**
   - Settings → Azure OpenAI → Test Connection → Success ✅

3. **Bot added to channel:**
   - In Slack, type `/invite @YourBot` in the channel

4. **Event subscriptions active:**
   - Slack app → Event Subscriptions → ON
   - Subscribed to `message.channels`

5. **Check backend logs:**
   - Should see events coming in
   - Look for error messages

---

### Issue: Bot responds to its own messages (loop)

**Solution:**
Already handled! The code ignores bot messages:
```python
if event.get("bot_id") or event.get("subtype") == "bot_message":
    return  # Ignore
```

---

### Issue: "Azure OpenAI not configured" error

**Solution:**
1. Go to Settings
2. Configure Azure OpenAI credentials
3. Test connection
4. Try sending message again

---

### Issue: Multiple bots respond

**Solution:**
If you have multiple users, the current code uses the first active user's credentials. For production:
- Map Slack workspace to specific user
- Or use organization-level credentials

---

## 🎨 Customization Ideas

### Add Custom Responses:

**For specific keywords:**
```python
if "summarize" in text.lower():
    # Trigger summary generation
    pass

if "help" in text.lower():
    # Show help message
    pass
```

### Add Slack Formatting:

**Rich messages with blocks:**
```python
{
    "channel": channel,
    "text": "AI Response",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*AI Assistant Response*\n" + response
            }
        }
    ]
}
```

### Add Buttons:

```python
{
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "Summarize"},
            "action_id": "summarize_action"
        }
    ]
}
```

---

## 📱 Testing Workflow

### Development Testing:

```
1. Start backend (python main.py)
   ↓
2. Start ngrok (ngrok http 8000)
   ↓
3. Configure Slack events with ngrok URL
   ↓
4. Send message in Slack
   ↓
5. Bot responds automatically! ✅
```

### Production:

```
1. Deploy backend to cloud
   ↓
2. Update Slack events URL to production URL
   ↓
3. Bot works 24/7! ✅
```

---

## 🎯 Expected Behavior

### When user sends message in Slack:

```
User in #general: "Hello bot, what's the weather?"
                     ↓
              Slack sends event to your backend
                     ↓
              Backend receives webhook
                     ↓
              Extracts message text
                     ↓
              Calls Azure OpenAI
                     ↓
              Gets AI response
                     ↓
              Posts response back to Slack
                     ↓
Bot in #general: "I'm an AI assistant, but I don't have real-time 
                  weather data. However, I can help you..."
```

**All logged in database!** ✅

---

## 📊 Monitoring

### View Bot Activity:

**Messages Page:**
- See all Slack conversations
- View AI responses
- Check token usage

**Admin Dashboard:**
- Total messages
- Usage statistics
- Cost tracking

**Admin Logs:**
- All Slack events
- Success/failure status
- Detailed audit trail

---

## 🎊 Advanced Features

### Add Slash Commands:

**In Slack App:**
1. Go to "Slash Commands"
2. Click "Create New Command"
3. Command: `/ai-help`
4. Request URL: `https://your-ngrok.ngrok.io/api/slack/slash-commands`
5. Description: "Get AI assistance"
6. Save

**Test:**
- In Slack: `/ai-help What is machine learning?`
- Bot responds!

---

### Add Interactive Buttons:

Already supported via `/api/slack/interactive` endpoint!

Add buttons to responses for:
- "Summarize this conversation"
- "Save to Google Drive"
- "More details"

---

## 🔐 Security Notes

**Request Verification:**
The code includes Slack signature verification to ensure requests are actually from Slack, not attackers.

**What's protected:**
- ✅ Timestamp validation (prevents replay attacks)
- ✅ HMAC signature verification
- ✅ Only processes valid Slack requests

---

## 📚 Summary

**What you added:**
- ✅ Real-time Slack event handler
- ✅ Message event processing
- ✅ App mention handling
- ✅ Interactive component support
- ✅ Slash command support
- ✅ Security verification

**What's needed:**
- ⚠️ Restart backend
- ⚠️ Run ngrok
- ⚠️ Configure Slack events
- ⚠️ Test in Slack channel

**Result:**
- 🎉 Bot responds in real-time in Slack!

---

## 🚀 Quick Start

**5-Minute Setup:**

1. Restart backend: `python main.py`
2. Start ngrok: `ngrok http 8000`
3. Copy ngrok URL
4. Slack app → Event Subscriptions → Enable
5. Request URL: `https://your-url.ngrok.io/api/slack/events`
6. Subscribe to: `message.channels`, `app_mention`
7. Save Changes → Reinstall app
8. Send message in Slack
9. Bot responds! 🎉

---

**Next: See `SLACK_REALTIME_TESTING.md` for detailed testing scenarios!** 🚀
