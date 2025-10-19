# Bug Fixes

## SQLAlchemy Reserved Name Error

**Issue**: `sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved when using the Declarative API.`

**Root Cause**: The `UsageStats` model had a column named `metadata`, which is a reserved attribute name in SQLAlchemy's Declarative API.

**Fix Applied**:
1. Renamed `metadata` column to `meta_info` in `backend/models.py` (line 72)
2. Updated reference in `backend/services/agent_service.py` (line 121)

**Files Modified**:
- `backend/models.py`
- `backend/services/agent_service.py`

**Testing**: 
After this fix, the backend should start without errors:
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Note**: This change only affects the database schema. No existing data migration is needed since this is a fresh installation.
