import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    # פרטי החשבון שלך לשם שליחת המייל
    sender_email = "yanir7575@gmail.com"
    receiver_email = "yanir7575@gmail.com.com"
    password = "yanir3149"
    
    # יצירת אובייקט MIME למייל
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    # גוף המייל
    message.attach(MIMEText(body, "plain"))
    
    # חיבור לשרת ה-SMTP של גוגל
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # הצפנה
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("מייל נשלח בהצלחה.")
    except Exception as e:
        print(f"⚠️ שגיאה בשליחת המייל: {e}")

# קריאה לפונקציה למשל בסיום המשימה:
send_email("המשימה הושלמה", "המשימה שלך הושלמה בהצלחה.")
