# 🧪 Slack Real-Time Bot Testing

## Quick Setup Summary

1. ✅ Backend updated with event handler
2. ⚠️ Need to restart backend
3. ⚠️ Need ngrok for public URL
4. ⚠️ Need to configure Slack events

---

## 🔧 Prerequisites

Before testing:

### Backend Services Configured:
- ✅ **Slack** credentials in Settings
- ✅ **Azure OpenAI** credentials in Settings
- ✅ Both connections tested successfully

### Tools Installed:
- ✅ ngrok (for exposing localhost)

---

## 📋 Complete Setup (Step-by-Step)

### Step 1: Restart Backend

```bash
cd backend
python main.py
```

**Verify:**
```
INFO: Application startup complete.
```

---

### Step 2: Start ngrok

**In a NEW terminal:**

```bash
ngrok http 8000
```

**You'll see:**
```
ngrok

Session Status: online
Forwarding: https://abc123.ngrok.io -> http://localhost:8000
Forwarding: http://abc123.ngrok.io -> http://localhost:8000

Connections: 0
```

**📋 Copy the HTTPS URL:** `https://abc123.ngrok.io`

**Keep this terminal open!**

---

### Step 3: Configure Slack App

#### 3.1 Open Slack App Settings
- Go to: https://api.slack.com/apps
- Select your app

#### 3.2 Enable Event Subscriptions

**Navigate:** "Event Subscriptions" in sidebar

**Enable Events:**
- Toggle to **ON**

**Request URL:**
- Enter: `https://abc123.ngrok.io/api/slack/events`
- Replace `abc123` with your actual ngrok subdomain
- Wait for ✅ **"Verified"**

**If you see ✅ "Verified":**
- Great! Slack successfully connected to your backend

**If verification fails:**
- Check backend is running
- Check ngrok is running
- Try accessing: `https://your-ngrok.url/health` in browser
- Check backend logs for errors

#### 3.3 Subscribe to Bot Events

**Scroll to "Subscribe to bot events"**

**Click "Add Bot User Event"** and add:

Required events:
- ✅ `message.channels` - Messages in public channels
- ✅ `message.groups` - Messages in private channels  
- ✅ `message.im` - Direct messages
- ✅ `app_mention` - When @bot is mentioned

Optional events:
- `message.mpim` - Multi-person DMs
- `channel_created` - New channels
- `team_join` - New members

#### 3.4 Save Changes

**Scroll to bottom:**
- Click **"Save Changes"**

**You'll see a yellow banner:**
- "You've changed the permissions..."
- Click **"reinstall your app"**
- Click **"Allow"**

**✅ Events are now configured!**

---

### Step 4: Update Bot Scopes (If Needed)

**Navigate:** "OAuth & Permissions" in sidebar

**Bot Token Scopes** - Ensure you have:
- ✅ `chat:write`
- ✅ `chat:write.public`
- ✅ `channels:history`
- ✅ `channels:read`
- ✅ `groups:history`
- ✅ `im:history`
- ✅ `im:write`
- ✅ `users:read`
- ✅ `app_mentions:read`

**If you added scopes:**
- Click "Reinstall to Workspace" at top
- Click "Allow"

---

## 🧪 Testing Scenarios

### Test 1: Message in Channel (Auto-Response)

**Setup:**
1. In Slack, create a test channel: `#bot-test`
2. Add the bot: Type `/invite @YourBot` in the channel

**Test:**
1. Send message: `Hello bot!`
2. **Expected:** Bot responds within 2-3 seconds ✅

**Backend Logs:**
```
INFO: POST /api/slack/events → 200 OK
INFO: Processing message from user U123 in channel C456
INFO: Successfully responded to message in channel C456
```

**In Slack:**
```
You: Hello bot!
Bot: Hello! I'm an AI assistant. How can I help you today?
```

---

### Test 2: Mention Bot

**Test:**
1. In any channel: `@YourBot what is machine learning?`

**Expected:**
- Bot responds with AI explanation ✅

**Why test this:**
- Different event type (`app_mention`)
- Tests bot can parse mentions
- Tests targeted responses

---

### Test 3: Direct Message

**Test:**
1. Open DM with bot (Apps section in Slack)
2. Send: `Can you summarize this for me?`

**Expected:**
- Bot responds in DM ✅
- Private conversation

---

### Test 4: Multiple Questions

**Test conversation:**
```
You: What is Python?
Bot: [Explains Python]

You: Can you give me an example?
Bot: [Provides code example]

You: Thanks!
Bot: [Friendly response]
```

**Check:**
- Each message logged
- Token usage tracked
- Responses make sense
- Conversation flows naturally

---

### Test 5: Request Summary

**Test:**
```
You: Can you summarize this article: [paste long text]
Bot: [Generates summary]
```

**Enhanced test:**
1. Ask for summary
2. Go to Summaries page in portal
3. Should see the summary saved
4. If Google Drive configured, should have Drive link

---

## 📊 Monitoring Tests

### Check Message History:

1. **Portal:** http://localhost:3000/messages
2. **Should see:** All Slack conversations
3. **Details:** Tokens used, response times

### Check Dashboard:

1. **Portal:** http://localhost:3000/dashboard
2. **Should see:** 
   - Message count increased
   - Token usage updated
   - Integration status

### Check Admin Logs:

1. **Portal:** http://localhost:3000/admin/logs
2. **Should see:**
   - `slack_message` actions
   - Success status
   - Timestamps

---

## 🎯 Performance Testing

### Test Response Time:

**Send message in Slack, measure:**
- Time from send to bot response
- Should be 1-3 seconds typically
- Depends on Azure OpenAI latency

**Check in logs:**
```
execution_time_ms: 1500  (1.5 seconds)
```

### Test Multiple Users:

**Have team members:**
1. Send messages in same channel
2. Bot responds to all
3. Tracks each separately
4. Check admin dashboard for stats

---

## 🔍 Debugging

### Enable Detailed Logging:

**Check backend logs for:**
```
INFO: Processing message from user...
INFO: Successfully responded to message...
ERROR: Failed to respond... (if issues)
```

### Check Slack Event Logs:

**In Slack App:**
1. Go to "Event Subscriptions"
2. Scroll down to "Event History"
3. See all events sent to your app
4. Check delivery status

### Test Endpoint Manually:

**Using curl:**
```bash
curl -X POST https://your-ngrok.ngrok.io/api/slack/events \
  -H "Content-Type: application/json" \
  -d '{"type":"url_verification","challenge":"test123"}'
```

**Should return:**
```json
{"challenge":"test123"}
```

---

## 🎨 Advanced Testing

### Test with Images:

**In Slack:**
- Upload image with text: `@YourBot what's in this image?`
- Bot responds (can analyze based on text, not image yet)

### Test with Links:

**In Slack:**
- Send: `@YourBot summarize this article: https://example.com/article`
- Bot can acknowledge (full web scraping would need additional code)

### Test Long Conversations:

**Send 10+ messages:**
- Build conversation context
- See how AI maintains context
- Check token usage accumulation

---

## 📈 Success Metrics

### After successful setup:

**In Slack:**
- ✅ Bot responds to messages
- ✅ Response time < 5 seconds
- ✅ Answers are relevant
- ✅ No duplicate responses
- ✅ No infinite loops

**In Portal:**
- ✅ Messages logged
- ✅ Token usage tracked
- ✅ Statistics updated
- ✅ Audit trail complete

**In Backend Logs:**
- ✅ Events received
- ✅ Messages processed
- ✅ Responses sent
- ✅ No errors

---

## 🎊 You Did It!

Your bot now:
- 🤖 Responds in real-time in Slack
- 💬 Handles direct messages
- 🏷️ Responds when mentioned
- 📊 Tracks all interactions
- 💾 Stores conversation history
- 📈 Monitors usage and costs

---

## 🚀 Next Steps

### Enhance the Bot:

1. **Add context awareness:**
   - Use previous messages in thread
   - Remember conversation history

2. **Add special commands:**
   - `/ai-summarize` - Quick summaries
   - `/ai-help` - Show capabilities

3. **Add rich formatting:**
   - Use Slack blocks
   - Add buttons
   - Include images

4. **Add integrations:**
   - Trigger workflows
   - Create Google Docs on command
   - Search capabilities

**Want me to add any of these? Let me know!** 🎉

---

## 📝 Quick Reference

**ngrok command:**
```bash
ngrok http 8000
```

**Slack Event URL:**
```
https://YOUR_NGROK_URL.ngrok.io/api/slack/events
```

**Test in Slack:**
```
Send: "Hello @YourBot!"
```

**View logs:**
```
Portal → Messages
Portal → Admin → Logs
Backend terminal
```

---

**Your Slack bot is now live and responding in real-time!** 🎉🤖
