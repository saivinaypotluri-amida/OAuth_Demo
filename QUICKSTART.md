# Quick Start Guide

Get your Agentic AI Slack Bot up and running in minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Git (to clone the repository)

## Installation Steps

### Option 1: Automated Setup (Linux/Mac)

1. Run the start script:
```bash
./start.sh
```

This will:
- Install all dependencies
- Create configuration files
- Start both backend and frontend servers

### Option 2: Manual Setup

#### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create environment file:
```bash
cp backend/.env.example backend/.env
```

3. Start backend server:
```bash
cd backend
python main.py
```

Backend will run on http://localhost:8000

#### Frontend Setup

1. Install Node dependencies:
```bash
cd frontend
npm install
```

2. Start frontend server:
```bash
npm run dev
```

Frontend will run on http://localhost:3000

## First Steps

### 1. Create Your Account

1. Open http://localhost:3000 in your browser
2. Click "Create a new account"
3. Fill in your details:
   - Username
   - Email
   - Password
   - Full Name (optional)
4. Click "Create account"

**Note:** The first user automatically becomes an admin!

### 2. Login

1. Go to http://localhost:3000/login
2. Enter your username and password
3. Click "Sign in"

### 3. Configure Services

After logging in, go to **Settings** to configure your integrations:

#### Slack Configuration

1. Create a Slack App:
   - Go to https://api.slack.com/apps
   - Click "Create New App" → "From scratch"
   - Name your app and select workspace
   
2. Configure OAuth & Permissions:
   - Add Bot Token Scopes:
     - `chat:write`
     - `channels:history`
     - `users:read`
   - Install app to workspace
   - Copy the "Bot User OAuth Token"

3. Get Signing Secret:
   - Go to "Basic Information"
   - Copy "Signing Secret"

4. Enter in Settings:
   - Bot Token: `xoxb-...`
   - Signing Secret: Your secret
   - Click "Save Credentials"
   - Click "Test Connection"

#### Azure OpenAI Configuration

1. Create Azure OpenAI Resource:
   - Go to Azure Portal
   - Create "Azure OpenAI" resource
   - Deploy a GPT model (e.g., gpt-35-turbo)

2. Get Credentials:
   - Go to resource "Keys and Endpoint"
   - Copy Endpoint URL
   - Copy API Key
   - Note your deployment name

3. Enter in Settings:
   - Endpoint: `https://your-resource.openai.azure.com/`
   - API Key: Your key
   - Deployment: Your deployment name
   - Click "Save Credentials"
   - Click "Test Connection"

#### Google Workspace Configuration

1. Create Google Cloud Project:
   - Go to https://console.cloud.google.com
   - Create new project

2. Enable APIs:
   - Enable "Google Drive API"
   - Enable "Google Docs API"

3. Create OAuth Credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: Web application
   - Add redirect URI: `http://localhost:8000/api/oauth/google/callback`
   - Copy Client ID and Client Secret

4. Update Backend Configuration:
   - Edit `backend/.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```
   - Restart backend server

5. Connect in Settings:
   - Click "Connect Google Workspace"
   - Authorize the application
   - Click "Test Connection"

## Using the Application

### Chat with AI

1. Go to **Messages**
2. Type your question
3. Click "Send"
4. AI responds using Azure OpenAI
5. View conversation history

### Generate Summaries

1. Go to **Summaries**
2. Click "Create Summary"
3. Enter:
   - Title
   - Content to summarize
   - Check "Save to Google Drive" (optional)
4. Click "Create Summary"
5. View generated summary
6. Access Google Drive link if saved

### Admin Features (Admin Users Only)

1. **Dashboard**: View system statistics
2. **Users**: Manage user accounts
3. **Logs**: View audit trail
4. **Usage**: Monitor API usage and costs

## Testing the Connection

After configuring each service:

1. Go to **Settings**
2. Click "Test Connection" for each service
3. Verify green checkmark appears
4. If test fails:
   - Check credentials are correct
   - Verify API keys are active
   - Check network connectivity
   - Review error message

## Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is available
lsof -i :8000

# If something is running, kill it
kill -9 <PID>

# Restart backend
cd backend
python main.py
```

### Frontend won't start

```bash
# Check if port 3000 is available
lsof -i :3000

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Can't connect to services

**Slack:**
- Verify bot token starts with `xoxb-`
- Check bot is installed in workspace
- Ensure scopes are added

**Azure OpenAI:**
- Verify endpoint URL is correct
- Check API key is active
- Ensure deployment exists

**Google:**
- Verify OAuth credentials in .env
- Check redirect URI matches exactly
- Ensure APIs are enabled

### Database errors

```bash
# Reset database
cd backend
rm slack_ai_bot.db
python main.py
# This will create a fresh database
# You'll need to signup again
```

## Next Steps

- Explore the dashboard
- Chat with your AI agent
- Generate your first summary
- Review usage statistics (admin)
- Customize your configuration

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review API docs at http://localhost:8000/docs
- Check the logs in the console for errors

## Tips

1. **First User is Admin**: The first user created automatically gets admin privileges
2. **Test Connections**: Always test connections after entering credentials
3. **Secure Your Keys**: Never commit `.env` files or share API keys
4. **Monitor Usage**: Keep an eye on token usage and costs in Admin panel
5. **Regular Backups**: Backup your SQLite database periodically

Enjoy your AI-powered Slack bot! 🚀
