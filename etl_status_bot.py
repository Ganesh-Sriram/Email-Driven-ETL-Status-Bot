import imaplib
import email
import smtplib
from email.message import EmailMessage
import psycopg2
from datetime import date, datetime
from email.utils import make_msgid
import time
import sys

# -----------------------------
# CONFIG
# -----------------------------
EMAIL_ID = "abcde@gmail.com"
APP_PASSWORD = "*****"

DB_CONFIG = {
    "host": "localhost",
    "database": "etl_details",
    "user": "postgres",
    "password": "1234",
    "port": 5432
}

ETL_NAME = "DAILY_REPORT_ETL"
POLL_INTERVAL = 10  # seconds

# -----------------------------
# DB CONNECTION (ONCE)
# -----------------------------
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("✅ Database connected")
except Exception as e:
    print("❌ DB connection failed:", e)
    sys.exit(1)

# -----------------------------
# MAIN LOOP
# -----------------------------
print(f"🚀 ETL Status Bot started. Polling every {POLL_INTERVAL} seconds...\n")

try:
    while True:
        try:
            # -----------------------------
            # FETCH ETL STATUS (fresh each loop)
            # -----------------------------
            cursor.execute("""
                SELECT last_success_date
                FROM etl_status
                WHERE etl_name = %s
            """, (ETL_NAME,))
            last_success_date = cursor.fetchone()[0]

            cursor.execute("""
                SELECT expected_completion_time
                FROM etl_expected_time
                WHERE etl_name = %s
            """, (ETL_NAME,))
            expected_time = cursor.fetchone()[0]

            today = date.today()

            # -----------------------------
            # CONNECT TO GMAIL
            # -----------------------------
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(EMAIL_ID, APP_PASSWORD)
            mail.select("inbox")

            status, messages = mail.search(None, 'UNSEEN')
            email_ids = messages[0].split()

            if email_ids:
                print(f"📨 {len(email_ids)} new email(s) detected")

            for e_id in email_ids:
                _, msg_data = mail.fetch(e_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                sender = email.utils.parseaddr(msg["From"])[1]
                subject = msg.get("Subject", "")

                # -----------------------------
                # SKIP REPLIES / FORWARDS
                # -----------------------------
                if subject.lower().startswith(("re:", "fwd:")):
                    print(f"⏭️ Skipping reply/forward email: {subject}")
                    mail.store(e_id, '+FLAGS', '\\Seen')
                    continue

                print("📩 Email from:", sender)

                timestamp = datetime.now().strftime("%H:%M:%S")

                reply = EmailMessage()
                reply["From"] = EMAIL_ID
                reply["To"] = sender
                reply["Subject"] = f"ETL Status | {today} @ {timestamp}"
                reply["Message-ID"] = make_msgid()
                reply["Precedence"] = "bulk"
                reply["Auto-Submitted"] = "auto-generated"

                # -----------------------------
                # BUSINESS LOGIC
                # -----------------------------
                if last_success_date < today:
                    body = f"""Greetings, 

Our daily ETL process has not yet completed today. The team is actively monitoring the process.

Expected completion time (24-hour format): {expected_time}. You will receive the reports shortly after completion.

This is an automatically generated email - please do not reply to it.

Thanks, 
BI & Analytics Team
"""
                else:
                    body = """Greetings,

The ETL process for today has completed successfully. If you have not yet received the reports, they may be in the final stages of processing. 

Please allow some additional time. If this is urgent, please reach out to the BI & Analytics team.

This is an automatically generated email - please do not reply to it.

Thanks, 
BI & Analytics Team
"""

                reply.set_content(body)

                # -----------------------------
                # SEND EMAIL
                # -----------------------------
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(EMAIL_ID, APP_PASSWORD)
                    server.send_message(reply)

                mail.store(e_id, '+FLAGS', '\\Seen')
                print("📤 Reply sent\n")

            mail.logout()

        except Exception as loop_error:
            print("⚠️ Error during processing:", loop_error)

        # -----------------------------
        # WAIT BEFORE NEXT POLL
        # -----------------------------
        time.sleep(POLL_INTERVAL)

except KeyboardInterrupt:
    print("\n🛑 ETL Status Bot stopped by user")

finally:
    cursor.close()
    conn.close()

    print("🔒 DB connection closed")
