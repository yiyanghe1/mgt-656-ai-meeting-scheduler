# mgt-656-ai-meeting-scheduler
Code base for an AI event scheduling app that syncs with Google calendar to find available meeting times between contacts.

## Django Hello World App

For the first sprint, we've set up a simple Django application that connects to a PostgreSQL database.

### Setup Instructions

1. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```
   
   **Note for Windows users:** If `pip` is not recognized, use `python -m pip` instead. Alternatively, you can use `py -m pip` (Python launcher).

2. **Set up PostgreSQL database:**
   - Connect to our database (name: `ai-event-scheduler-db`) locally using the external database URL in .env file
   - In your terminal, run the command in the comment below, replacing external_db_url with the actual database URL:
   **$env:DATABASE_URL="external_db_url"**

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Visit the app:**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - You should see "Hello world" displayed