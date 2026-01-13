# 📧 Email-Driven ETL Status Bot

An automated Python service that monitors the daily ETL execution status from a PostgreSQL database and responds to user email queries with real-time ETL updates.  
Users can simply send a blank or short email to a configured inbox and receive an instant, automated status response—eliminating manual follow-ups and unnecessary email escalations.

---

## 📂 Project Structure

ETL_Status_Bot/

│

├── etl_status_bot.py

├── etl_status_bot_queries.sql

└── README.md

---

## 🧠 How It Works

1. The service continuously listens to a Gmail inbox using **IMAP**.
2. When a **new, unread email** is received:
   - Replies and forwarded emails are ignored.
   - Only fresh email requests are processed.
3. The bot queries PostgreSQL to determine:
   - Whether today’s ETL has completed.
   - The expected completion time (if delayed).
4. An automated, professional response is sent back to the sender via **SMTP**.
5. The service runs continuously and polls for new emails at a fixed interval.

---

## 🗄️ Database Design

The system relies on two PostgreSQL tables:

### 1️⃣ `etl_status`
Stores the latest successful ETL execution date.

| Column Name        | Description |
|--------------------|-------------|
| etl_name           | Unique ETL identifier |
| last_success_date  | Last successful ETL run date |

### 2️⃣ `etl_expected_time`
Stores manually maintained expected delivery times.

| Column Name               | Description |
|---------------------------|-------------|
| etl_name                  | Unique ETL identifier |
| expected_completion_time  | Expected ETL completion time |

All ready-to-use SQL queries for viewing and updating these tables are available in: **etl_status_bot_queries.sql**

---

## ⚙️ Configuration

Update the following values in `etl_status_bot.py`:

```
EMAIL_ID = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"

DB_CONFIG = {
    "host": "localhost",
    "database": "etl_details",
    "user": "postgres",
    "password": "your_password",
    "port": 5432
}

ETL_NAME = "DAILY_REPORT_ETL"
POLL_INTERVAL = 10  #seconds
```

**⚠️ Gmail requires App Passwords (2FA enabled).**

---

▶️ Running the Service

1️⃣ Install dependencies

   - pip install psycopg2

   - imaplib, email, smtplib, and time are part of Python’s standard library.

2️⃣ Start the bot

   - python etl_status_bot.py


**The service will:**

   - Connect to PostgreSQL

   - Poll the Gmail inbox every configured interval

   - Auto-respond to new ETL status requests


**📬 Email Behavior**

   - ✔ Responds only to new, unread emails

   - ✔ Ignores replies and forwards (Re: / Fwd:)

   - ✔ Sends non-threaded, standalone responses

   - ✔ Marks processed emails as Seen

   - ✔ Prevents auto-reply loops using email headers

**🛡️ Safety & Controls**

   - Auto-generated emails include safeguards to prevent recursive replies

   - Reply chains are skipped to avoid repeated triggers

   - Database connection is reused for efficiency

   - Gracefully shuts down on keyboard interruption

**🚀 Use Cases**

   - ETL status transparency for business users

   - Reduced manual follow-ups to BI teams

   - Centralized ETL communication channel

   - Lightweight alternative to dashboards or ticket systems

**🏷️ System Name**

   - Email-Driven ETL Status Bot

👤 Owner

   - Ganesh Sriram


***This service is intended for internal use to improve operational efficiency and communication around ETL delivery timelines.***
