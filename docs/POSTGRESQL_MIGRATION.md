# PostgreSQL Migration Guide

## Overview
SwasthyaGuide has been upgraded from JSON-based storage to **PostgreSQL database** for:
- ✅ Scalable clinic data storage
- ✅ Conversation history logging
- ✅ User profile management
- ✅ Analytics and metrics tracking

## What's New

### Database Models
1. **Clinics** - Medical facility information with location-based search
2. **Conversations** - Full conversation history with intent detection
3. **Messages** - Individual messages within conversations
4. **UserProfile** - User preferences and activity tracking
5. **Analytics** - Usage metrics and statistics

### Features
- Connection pooling for better performance
- Automatic health checks
- Migration scripts for data import
- Cloud deployment ready (Render/Railway/Heroku)

---

## Setup Instructions

### 1. Install PostgreSQL

#### Local Development (macOS)
```bash
# Install PostgreSQL using Homebrew
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Create database
createdb swasthyaguide
```

#### Local Development (Linux/Ubuntu)
```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql

# Create database
sudo -u postgres createdb swasthyaguide
```

#### Cloud Deployment
Use one of these platforms (database URL is provided automatically):
- **Render**: Add PostgreSQL service in dashboard
- **Railway**: Add PostgreSQL plugin
- **Heroku**: Add Heroku Postgres add-on

---

### 2. Configure Environment Variables

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and set your database URL:

**For local development:**
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/swasthyaguide
```

**For cloud deployment:**
```bash
# Render/Railway/Heroku will auto-set DATABASE_URL
# No manual configuration needed!
```

---

### 3. Install Python Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install updated requirements
pip install -r requirements.txt
```

New packages installed:
- `psycopg2-binary` - PostgreSQL adapter
- `SQLAlchemy` - ORM for database operations
- `alembic` - Database migrations (future use)

---

### 4. Initialize Database

Create tables in PostgreSQL:

```bash
# Option 1: Using initialization script (Recommended)
python scripts/init_database.py

# Option 2: Drop existing tables and recreate
python scripts/init_database.py --drop-existing
```

Expected output:
```
✅ DATABASE INITIALIZATION SUCCESSFUL!
```

---

### 5. Migrate Clinic Data

Import existing clinic data from JSON to PostgreSQL:

```bash
# Migrate all clinics from data/clinics.json
python scripts/migrate_to_postgres.py

# Verify migration
python scripts/migrate_to_postgres.py --verify-only
```

Expected output:
```
✅ MIGRATION SUCCESSFUL!
Total Locations: 8
Total Clinics: 467
Successfully Inserted: 467
```

---

### 6. Test the Application

#### Test locally:
```bash
python app.py
```

Visit: http://localhost:5000/health

Expected response:
```json
{
  "status": "healthy",
  "database": {
    "status": "healthy",
    "database": "connected",
    "pool_size": 10
  }
}
```

#### Test CLI:
```bash
python main.py
```

---

## Deployment to Cloud

### Render.com Deployment

1. **Create PostgreSQL Database**
   - In Render dashboard, click "New +" → "PostgreSQL"
   - Name: `swasthyaguide-db`
   - Copy the "Internal Database URL"

2. **Update Web Service**
   - Go to your web service settings
   - Add environment variable: `DATABASE_URL` (use Internal Database URL)
   - Render will auto-detect and use this URL

3. **Initialize Database**
   ```bash
   # Run via Render shell or locally with production DATABASE_URL
   python scripts/init_database.py
   python scripts/migrate_to_postgres.py
   ```

4. **Deploy**
   - Push changes to GitHub
   - Render will auto-deploy

### Railway Deployment

1. **Add PostgreSQL Plugin**
   - In Railway project, click "New" → "Database" → "Add PostgreSQL"
   - DATABASE_URL is automatically set

2. **Deploy**
   - Push changes to GitHub
   - Railway auto-deploys

3. **Initialize Database**
   ```bash
   # Run one-time initialization
   railway run python scripts/init_database.py
   railway run python scripts/migrate_to_postgres.py
   ```

### Heroku Deployment

1. **Add PostgreSQL Add-on**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

2. **Deploy**
   ```bash
   git push heroku main
   ```

3. **Initialize Database**
   ```bash
   heroku run python scripts/init_database.py
   heroku run python scripts/migrate_to_postgres.py
   ```

---

## Database Management

### View Clinic Data
```bash
# Start Python shell
python

# Query clinics
from database import db_session, Clinic
with db_session() as session:
    clinics = session.query(Clinic).filter_by(city='Lucknow').limit(5).all()
    for c in clinics:
        print(f"{c.name} - {c.address}")
```

### View Conversation History
```python
from database import db_session, Conversation

with db_session() as session:
    recent = session.query(Conversation).order_by(
        Conversation.created_at.desc()
    ).limit(10).all()
    
    for conv in recent:
        print(f"{conv.created_at}: {conv.user_message[:50]}...")
```

### Analytics
```python
from database import db_session, Conversation, UserProfile
from sqlalchemy import func

with db_session() as session:
    # Total conversations
    total = session.query(func.count(Conversation.id)).scalar()
    print(f"Total conversations: {total}")
    
    # Conversations by language
    by_lang = session.query(
        Conversation.language, 
        func.count(Conversation.id)
    ).group_by(Conversation.language).all()
    print(f"By language: {by_lang}")
    
    # Total users
    users = session.query(func.count(UserProfile.id)).scalar()
    print(f"Total users: {users}")
```

---

## Troubleshooting

### Connection Errors

**Error:** `could not connect to server`
```bash
# Check if PostgreSQL is running
# macOS:
brew services list

# Linux:
sudo systemctl status postgresql

# Restart if needed
brew services restart postgresql@15
# or
sudo systemctl restart postgresql
```

**Error:** `database "swasthyaguide" does not exist`
```bash
createdb swasthyaguide
```

### Migration Issues

**Error:** `Table already exists`
```bash
# Drop and recreate tables
python scripts/init_database.py --drop-existing
```

**Error:** `No module named 'psycopg2'`
```bash
pip install psycopg2-binary
```

### Cloud Deployment Issues

**Error:** `DATABASE_URL not set`
- Check environment variables in cloud platform dashboard
- Verify PostgreSQL service is running
- Restart web service

---

## Rollback to JSON (if needed)

If you need to temporarily rollback to JSON:

1. **Restore old files**
   ```bash
   git checkout HEAD~1 -- clinic_finder.py chatbot.py app.py
   ```

2. **Remove database imports**
   - Comment out database initialization in `app.py`

3. **Use JSON file**
   - Clinics will be read from `data/clinics.json` as before

---

## Benefits of PostgreSQL Upgrade

### Performance
- ✅ Fast location-based search with database indexing
- ✅ Connection pooling reduces database overhead
- ✅ Scalable to millions of records

### Features
- ✅ Full conversation history for every user
- ✅ User profiles with preferences
- ✅ Analytics for usage insights
- ✅ Search by city, area, or specialty

### Reliability
- ✅ ACID compliance (data integrity)
- ✅ Automatic backups (cloud platforms)
- ✅ High availability with replication

---

## Next Steps

### Future Enhancements
1. **Database Migrations** - Use Alembic for schema changes
2. **Advanced Analytics** - Dashboard for metrics visualization
3. **Geospatial Search** - Location-based clinic recommendations
4. **Full-Text Search** - Better clinic and symptom search
5. **Data Export** - API endpoints for data extraction

### Monitoring
- Set up database monitoring alerts
- Track query performance
- Monitor connection pool usage
- Set up automated backups

---

## Support

Issues? Check:
1. PostgreSQL service is running
2. DATABASE_URL is correctly set
3. Tables are created (`python scripts/init_database.py`)
4. Data is migrated (`python scripts/migrate_to_postgres.py --verify-only`)

For more help, check application logs:
```bash
# View logs
tail -f logs/swasthyaguide.log

# Or on cloud platforms:
render logs              # Render
railway logs             # Railway
heroku logs --tail       # Heroku
```

---

**Version:** 2.0.0  
**Last Updated:** February 2026
