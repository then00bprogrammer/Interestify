from datetime import datetime
import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .database.database import App  
import dotenv
import os

dotenv.load_dotenv()

uri = os.getenv("DATABASE_URL")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")

def send_email(recipient_email, subject, html_template, articles):
    try:
        # Email configuration
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT")

        # Create an SMTP connection
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            for article in articles:
                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = sender_email
                message["To"] = recipient_email

                # Fill in the HTML template with article data
                filled_template = html_template.format(
                    title=article['title'],
                    author=article['author'],
                    category=article['category'],
                    url=article['url']
                )

                # Create a MIME text part for the filled HTML content
                html_part = MIMEText(filled_template, "html")

                # Attach the HTML part to the message
                message.attach(html_part)

                # Send the email for each article
                server.sendmail(sender_email, recipient_email, message.as_string())

    except Exception as e:
        print("An error occurred in send_email:", e)

def automate_mail():
    try:
        subject = 'Interestify Weekly mail!'
        html_template = """
<html>
  <head>
    <title>Blog Cards</title>
    <style>
      body {{
        background-color: #f2f2f2;
      }}

      .blog-card {{
        background-color: #ececec;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
      }}

      .blog-title {{
        font-size: 24px;
        font-weight: bold;
        color: #333;
      }}

      .blog-author {{
        font-size: 16px;
        color: #555;
      }}

      .blog-category {{
        font-size: 16px;
        color: #555;
        margin-bottom: 10px;
      }}

      .break {{
        height: 2px;
        background-color: #999;
        margin: 20px 0;
      }}

      .read-link {{
        font-size: 16px;
        color: #007bff;
        text-decoration: none;
      }}
    </style>
  </head>
  <body>
  Here are the recommended research papers from your top 5 categories:
  {content}
  </body>
</html>
"""


        database = App(uri, user, password)
        user_books = database.get_all_users()
        database.close()

        # Iterate over each user's books and send the email
        for email, books in user_books.items():
            # Generate the content for the HTML template
            content = ""
            if books == []:
                continue
            for i, book in enumerate(books):
                content += """
                <div class="blog-card">
                   <h2 class="blog-title">{title}</h2>
                    <p class="blog-author">Author: {author}</p>
                    <p class="blog-category">Category: {category}</p>
                    <p class="blog-summary">{summary}</p>
                    <a href="{url}" class="read-link">Read about this</a>
                </div>
                """

            if i != len(books) - 1:  # Exclude the last book
                content += "<hr class='break' />"

            filled_template = html_template.replace("{content}", content)
            # Send the email
            send_email(email, subject, filled_template, books)

    except Exception as e:
        print("An error occurred in automate_mail:", e)

def schedule_task():
    try:
        # Define the time of execution in IST
        execution_time = '12:00'

        # Schedule the task to run every Saturday at the specified time
        schedule.every().saturday.at(execution_time).do(automate_mail).tag('send_email')

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        print("An error occurred in schedule_task:", e)
