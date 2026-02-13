# Quick Start: PostgreSQL Setup

## For Local Development (5 minutes)

### 1. Install & Setup PostgreSQL
```bash
# macOS
brew install postgresql@15
brew services start postgresql@15
createdb swasthyaguide

# Linux
sudo apt-get install postgresql
sudo systemctl start postgresql
sudo -u postgres createdb swasthyaguide
```

### 2. Configure Environment
```bash
# Create .env file
cp .env.example .env

# Edit .env and set:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/swasthyaguide
```

### 3. Install Dependencies
```bash
source .venv/bin/activate  # or: .venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
# Create tables
python scripts/init_database.py

# Import clinic data
python scripts/migrate_to_postgres.py
```

### 5. Test
```bash
# Start app
python app.py

# Or test CLI
python main.py
```

Visit: http://localhost:5000/health

---

## For Cloud Deployment (Render/Railway/Heroku)

### On Render
1. Add PostgreSQL database in dashboard
2. Add `DATABASE_URL` environment variable (use Internal URL)
3. Deploy
4. Run in shell:
   ```bash
   python scripts/init_database.py
   python scripts/migrate_to_postgres.py
   ```

### On Railway
1. Add PostgreSQL plugin (DATABASE_URL auto-set)
2. Deploy
3. Run:
   ```bash
   railway run python scripts/init_database.py
   railway run python scripts/migrate_to_postgres.py
   ```

### On Heroku
1. Add PostgreSQL:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```
2. Deploy:
   ```bash
   git push heroku main
   ```
3. Initialize:
   ```bash
   heroku run python scripts/init_database.py
   heroku run python scripts/migrate_to_postgres.py
   ```

---

## Verification

Check everything works:
```bash
# Verify database
python scripts/migrate_to_postgres.py --verify-only

# Test health endpoint
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": {
    "status": "healthy",
    "database": "connected"
  }
}
```

---

## Troubleshooting

**Can't connect?**
```bash
# Check PostgreSQL is running
brew services list  # macOS
systemctl status postgresql  # Linux
```

**Tables not found?**
```bash
python scripts/init_database.py
```

**No clinic data?**
```bash
python scripts/migrate_to_postgres.py
```

---

For detailed instructions, see [POSTGRESQL_MIGRATION.md](POSTGRESQL_MIGRATION.md)
