# Agentic AI Slack Bot with Cloud Services Integration

A comprehensive agentic AI application integrated with Slack, Azure OpenAI, and Google Workspace. Features a modern web portal with user and admin personas, secure credential management, AI-powered conversations, and automatic summary generation.

## Features

### Core Functionality
- **Slack Integration**: Bot responds to messages with AI-generated responses
- **Azure OpenAI Integration**: Powered by Azure's GPT models for intelligent responses
- **Google Workspace Integration**: Automatic summary storage in Google Drive as documents
- **Secure Credential Storage**: All service credentials encrypted and stored in SQLite
- **OAuth Authentication**: Seamless Google Workspace connection via OAuth 2.0
- **Connection Testing**: Verify credentials before use without manual configuration

### User Features
- Interactive chat interface with AI agent
- Message history and conversation tracking
- Summary generation from any content
- Automatic Google Drive document creation
- Token usage and cost tracking
- Service configuration management

### Admin Features
- **Dashboard**: System-wide statistics and metrics
- **User Management**: View, activate/deactivate users
- **Audit Logs**: Complete activity trail with filtering
- **Usage Statistics**: Token usage, costs, and performance metrics
- **Charts & Analytics**: Visual representations of usage patterns

## Technology Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database for credential storage
- **JWT**: Secure authentication tokens
- **Cryptography**: Encrypted credential storage

### Frontend
- **React 18**: Modern UI library
- **Vite**: Fast build tool
- **TailwindCSS**: Utility-first CSS framework
- **Recharts**: Beautiful data visualization
- **Lucide React**: Modern icon library

### Integrations
- **Slack SDK**: Official Slack API integration
- **Azure OpenAI**: GPT-powered AI responses
- **Google APIs**: Drive and Docs integration
- **OAuth 2.0**: Secure authorization flow

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r ../requirements.txt
```

3. Create `.env` file from example:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration (or configure via portal after signup)

5. Run the backend server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Configuration

### Initial Setup

1. **Signup**: Create your account at `http://localhost:3000/signup`
   - First user automatically becomes admin
   - Subsequent users have standard user role

2. **Login**: Access the portal at `http://localhost:3000/login`

3. **Configure Services** (via Settings page):

   **Slack Configuration:**
   - Create a Slack app at https://api.slack.com/apps
   - Add Bot Token Scopes: `chat:write`, `channels:history`, `users:read`
   - Install app to workspace
   - Copy Bot Token, App Token, and Signing Secret
   - Enter credentials in Settings → Slack Configuration
   - Test connection

   **Azure OpenAI Configuration:**
   - Create Azure OpenAI resource
   - Deploy a GPT model
   - Copy endpoint, API key, and deployment name
   - Enter credentials in Settings → Azure OpenAI Configuration
   - Test connection

   **Google Workspace Configuration:**
   - Create Google Cloud project
   - Enable Google Drive API and Google Docs API
   - Create OAuth 2.0 credentials
   - Add redirect URI: `http://localhost:8000/api/oauth/google/callback`
   - Click "Connect Google Workspace" button
   - Authorize the application
   - Test connection

## Usage

### User Persona

#### Chat with AI Agent
1. Navigate to **Messages**
2. Type your message in the input field
3. AI responds with intelligent answers
4. View conversation history and token usage

#### Generate Summaries
1. Navigate to **Summaries**
2. Click "Create Summary"
3. Enter title and content to summarize
4. Choose whether to save to Google Drive
5. AI generates summary and saves to database/Drive

#### Manage Settings
1. Navigate to **Settings**
2. Configure service credentials
3. Test connections
4. Update credentials as needed

### Admin Persona

#### Dashboard
- View system-wide statistics
- Monitor active users
- Track total messages and summaries
- Review costs and token usage
- View recent activity logs

#### User Management
- View all users
- Activate/deactivate accounts
- View user details and activity
- Monitor user creation dates

#### Audit Logs
- View complete activity trail
- Filter by action or user
- Track system events
- Monitor security events

#### Usage Statistics
- View detailed usage metrics
- Filter by user, service, or time period
- Visualize data with charts
- Monitor costs and token consumption
- Track performance metrics

## API Documentation

Once the backend is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

**Authentication:**
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout user

**Credentials:**
- `POST /api/credentials/` - Create/update credentials
- `GET /api/credentials/` - Get all credentials
- `POST /api/credentials/{service_type}/test` - Test connection
- `DELETE /api/credentials/{service_type}` - Delete credentials

**Agent:**
- `POST /api/agent/message` - Send message to AI
- `POST /api/agent/summary` - Generate summary
- `GET /api/agent/messages` - Get message history
- `GET /api/agent/summaries` - Get summaries

**Admin:**
- `GET /api/admin/dashboard` - Get dashboard stats
- `GET /api/admin/users` - Get all users
- `PATCH /api/admin/users/{user_id}` - Update user
- `GET /api/admin/logs` - Get audit logs
- `GET /api/admin/usage` - Get usage statistics

## Testing

### Backend Tests

Run the test suite:
```bash
cd backend
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

### Test Coverage
- Authentication flow (signup, login, logout)
- Credential management (create, read, update, delete)
- Connection testing for all services
- User authorization and permissions
- Admin functionalities

## Security Features

1. **Password Hashing**: Bcrypt for secure password storage
2. **JWT Tokens**: Secure authentication with access and refresh tokens
3. **Credential Encryption**: Fernet symmetric encryption for stored credentials
4. **OAuth 2.0**: Secure authorization for Google services
5. **CORS Protection**: Configured allowed origins
6. **SQL Injection Prevention**: SQLAlchemy ORM protection
7. **Input Validation**: Pydantic models for request validation

## Database Schema

### Users
- User accounts with roles (user/admin)
- Password hashing
- Activity tracking

### Credentials
- Encrypted service credentials
- Connection test results
- Last tested timestamps

### Audit Logs
- Complete activity trail
- User actions
- System events

### Usage Stats
- Token consumption
- Cost tracking
- Performance metrics

### Messages
- Conversation history
- AI responses
- Token usage per message

### Summaries
- Generated summaries
- Google Drive links
- Source content references

## Project Structure

```
/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database setup
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── security.py            # Authentication & encryption
│   ├── routes/                # API routes
│   │   ├── auth.py
│   │   ├── credentials.py
│   │   ├── agent.py
│   │   ├── admin.py
│   │   └── oauth.py
│   ├── services/              # Service integrations
│   │   ├── slack_service.py
│   │   ├── azure_ai_service.py
│   │   ├── google_service.py
│   │   ├── credential_service.py
│   │   └── agent_service.py
│   └── tests/                 # Test suite
│       ├── test_auth.py
│       └── test_credentials.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main app component
│   │   ├── main.jsx           # Entry point
│   │   ├── components/        # Reusable components
│   │   │   └── Layout.jsx
│   │   ├── pages/             # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Signup.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Settings.jsx
│   │   │   ├── Messages.jsx
│   │   │   ├── Summaries.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── AdminUsers.jsx
│   │   │   ├── AdminLogs.jsx
│   │   │   └── AdminUsage.jsx
│   │   ├── context/           # React context
│   │   │   └── AuthContext.jsx
│   │   └── services/          # API services
│   │       └── api.js
│   ├── package.json
│   └── vite.config.js
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Troubleshooting

### Backend Issues

**Database errors:**
```bash
# Delete and recreate database
rm slack_ai_bot.db
python main.py
```

**Import errors:**
```bash
# Ensure you're in the backend directory
cd backend
# Reinstall dependencies
pip install -r ../requirements.txt
```

### Frontend Issues

**Build errors:**
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Ensure backend ALLOWED_ORIGINS includes frontend URL
- Check that frontend is running on expected port

### Integration Issues

**Slack connection fails:**
- Verify bot token starts with `xoxb-`
- Check bot has required scopes
- Ensure signing secret is correct

**Azure OpenAI connection fails:**
- Verify endpoint URL format
- Check API key is valid
- Ensure deployment name matches

**Google OAuth fails:**
- Verify redirect URI matches exactly
- Check OAuth consent screen is configured
- Ensure required APIs are enabled

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please:
1. Check existing documentation
2. Search closed issues
3. Open a new issue with details

## Roadmap

Future enhancements:
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Webhook support for Slack events
- [ ] Additional AI model providers
- [ ] Team collaboration features
- [ ] Custom AI agent personalities
- [ ] Scheduled summary generation
- [ ] Export data functionality
- [ ] Mobile responsive improvements
- [ ] Dark mode support

## Acknowledgments

- FastAPI for the excellent web framework
- React team for the UI library
- Slack, Microsoft, and Google for their APIs
- Open source community for various libraries
