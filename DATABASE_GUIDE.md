# Database Guide: Creating and Viewing Tables in PostgreSQL on Render

This guide explains how to create new tables and view existing tables in your PostgreSQL database hosted on Render.

## Prerequisites

1. Make sure your `DATABASE_URL` environment variable is set (either locally or on Render)
2. For local development, set it using:
   ```powershell
   $env:DATABASE_URL="postgresql://username:password@host:port/database_name"
   ```
   (Use the **External Database URL** from your Render dashboard for local access)

---

## Creating New Tables in Django

In Django, tables are created through **models** and **migrations**. Here's the process:

### Step 1: Create a Django App (if you don't have one)

```bash
python manage.py startapp your_app_name
```

### Step 2: Define Models in `your_app_name/models.py`

Models define your database schema. For example:

```python
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

### Step 3: Add Your App to `INSTALLED_APPS`

In `ai_event_scheduler/settings.py`, add your app:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    # ... other apps ...
    'your_app_name',  # Add this
]
```

### Step 4: Create Migrations

Migrations are Django's way of tracking database schema changes:

```bash
python manage.py makemigrations
```

This creates migration files in `your_app_name/migrations/`.

### Step 5: Apply Migrations to Create Tables

```bash
python manage.py migrate
```

This creates the actual tables in your PostgreSQL database.

---

## Viewing Existing Tables

There are several ways to view tables in your database:

### Method 1: Using Django's `dbshell` Command

This opens a PostgreSQL shell connected to your database:

```bash
python manage.py dbshell
```

Once in the PostgreSQL shell, you can run:

```sql
-- List all tables
\dt

-- List all tables with more details
\dt+

-- Describe a specific table
\d table_name

-- Exit the shell
\q
```

### Method 2: Using Django Shell with Python

```bash
python manage.py shell
```

Then in the Python shell:

```python
from django.db import connection

# Get all table names
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])
```

### Method 3: Using `inspectdb` to See Table Structure

Django can inspect your database and show you the models:

```bash
python manage.py inspectdb
```

This shows all tables and their structure as Django models.

### Method 4: Direct PostgreSQL Connection (psql)

If you have `psql` installed locally, you can connect directly:

```bash
psql "your_database_url_here"
```

Or extract the connection details and connect:

```bash
psql -h hostname -p port -U username -d database_name
```

Then use SQL commands:
```sql
-- List all tables
\dt

-- Show table structure
\d table_name

-- Query table data
SELECT * FROM table_name LIMIT 10;
```

### Method 5: Using Django Admin (for registered models)

If you register your models in `admin.py`, you can view them in the Django admin interface:

1. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

2. Start the server:
   ```bash
   python manage.py runserver
   ```

3. Visit `http://127.0.0.1:8000/admin/` and log in

---

## Quick Reference Commands

```bash
# Create migrations from model changes
python manage.py makemigrations

# Apply migrations to create/update tables
python manage.py migrate

# View migration status
python manage.py showmigrations

# Open database shell
python manage.py dbshell

# Inspect database structure
python manage.py inspectdb

# Open Django Python shell
python manage.py shell
```

---

## Common SQL Queries for Viewing Tables

When in `dbshell` or connected via `psql`:

```sql
-- List all tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Get table columns and types
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'your_table_name';

-- Count rows in a table
SELECT COUNT(*) FROM your_table_name;

-- View all data in a table (limit to 10 rows)
SELECT * FROM your_table_name LIMIT 10;
```

---

## Notes

- **Always use migrations** - Never create tables directly in PostgreSQL when using Django. Use models and migrations instead.
- **Migration files are version controlled** - Commit your migration files to git so your team can apply the same schema changes.
- **Render automatically runs migrations** - If you have a build script, you can add `python manage.py migrate` to it so migrations run on deployment.



