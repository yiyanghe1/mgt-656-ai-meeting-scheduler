# How to Insert Fake User Data into PostgreSQL

## Prerequisites

1. **Set up your database connection** (if not already done):
   
   For Windows PowerShell:
   ```powershell
   $env:DATABASE_URL="postgresql://username:password@host:port/database_name"
   ```
   
   For Command Prompt:
   ```cmd
   set DATABASE_URL=postgresql://username:password@host:port/database_name
   ```
   
   Use the **External Database URL** from your Render dashboard for local access.

2. **Ensure migrations are applied**:
   ```bash
   python manage.py migrate
   ```
   
   This ensures the `user_details` table exists in your database.

## Inserting the Fake User Data

You have two options to run the script:

### Option 1: Run the script directly (Recommended)
```bash
python create_fake_users.py
```

### Option 2: Run via Django shell
```bash
python manage.py shell < create_fake_users.py
```

## Verify the Data

After running the script, you can verify the data was inserted:

### Using Django Shell
```bash
python manage.py shell
```

Then in the shell:
```python
from homepage.models import UserDetails
users = UserDetails.objects.all()
for user in users:
    print(f"{user.userID}: {user.firstname} {user.lastname} - {user.google_account}")
    print(f"  First auth: {user.first_auth_ts}, Last auth: {user.last_auth_ts}")
```

### Using PostgreSQL directly
```bash
python manage.py dbshell
```

Then in the PostgreSQL shell:
```sql
SELECT * FROM user_details;
```

Or to see just the count:
```sql
SELECT COUNT(*) FROM user_details;
```

## Expected Output

The script will create 5 users:
- John Doe (john.doe@gmail.com)
- Jane Smith (jane.smith@gmail.com)
- Bob Johnson (bob.johnson@gmail.com)
- Alice Williams (alice.williams@gmail.com)
- Charlie Brown (charlie.brown@gmail.com)

All users will have the same timestamp for both `first_auth_ts` and `last_auth_ts`.

