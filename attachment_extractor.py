BASE_FOLDER = "Attachments"
import imaplib
import email
import os
from datetime import datetime

# ---------- CONFIG ----------
EMAIL = ""
PASSWORD = ""
BASE_FOLDER = "Attachments"

os.makedirs(BASE_FOLDER, exist_ok=True)

# ---------- CONNECT ----------
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# ---------- FETCH EMAILS ----------
_, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

# ---------- PROCESS ----------
for email_id in email_ids:
    _, msg_data = mail.fetch(email_id, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])

    sender = msg.get("From")
    sender = sender.split("<")[-1].replace(">", "").replace("@", "_")

    date = msg.get("Date")
    try:
        date_obj = datetime.strptime(date[:16], "%a, %d %b %Y")
        date_folder = date_obj.strftime("%Y-%m-%d")
    except:
        date_folder = "Unknown_Date"

    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = part.get_filename()

            if filename:
                file_type = filename.split(".")[-1]

                folder_path = f"{BASE_FOLDER}/{date_folder}/{sender}/{file_type}"
                os.makedirs(folder_path, exist_ok=True)

                file_path = f"{folder_path}/{filename}"

                with open(file_path, "wb") as f:
                    f.write(part.get_payload(decode=True))

                print("Saved:", file_path)
mail.logout()
print("files added to attachment folder successfully!")
