import sys
import os

from pathlib import Path

from sparkpost import SparkPost


if len(sys.argv) != 3:
    print("Usage:")
    print("python", __file__, "<file_to_email>", "<comma_separated_emails_list>")

    raise SystemExit(0)


filepath = Path(sys.argv[1])
email_recipients = sys.argv[2].split(",")

print("Sending", filepath, "to", email_recipients)

assert filepath.stat().st_size < 10_000, "File too big to send!"
assert len(email_recipients) < 5, "Too many recipients!"
assert all("@" in email for email in email_recipients), "Invalid emails!"


# Assumes an environment variable SPARKPOST_API_KEY has been set with the SparkPost API key
# And an EMAIL_FROM one with the address to use as sender
sp = SparkPost()
response = sp.transmissions.send(
    recipients=email_recipients,
    text=filepath.read_text("utf8"),
    from_email=os.environ.get("EMAIL_FROM"),
    subject=" ".join(part.capitalize() for part in filepath.stem.split("_")),
)

print("Got response", response)
