import smtplib
import random
import time

OTP_STORE = {}

def send_otp_email(receiver_email, receiver_name=None):
    otp = str(random.randint(100000, 999999))
    sender_email = "guzz9777@gmail.com"
    sender_password = "bnnq qnlk jbwt rgil"

    subject = "ยืนยัน OTP"
    
    if receiver_name:
        message_text = f"สวัสดี {receiver_name},\n\nรหัส OTP ของคุณคือ: {otp} (หมดอายุใน 5 นาที)"
    else:
        message_text = f"รหัส OTP ของคุณคือ: {otp} (หมดอายุใน 5 นาที)"

    message = f"Subject: {subject}\n\n{message_text}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.encode('utf-8'))

        OTP_STORE[receiver_email] = {"otp": otp, "timestamp": time.time(), "name": receiver_name}
        return True
    except Exception as e:
        print(f"ไม่สามารถส่ง OTP ได้: {e}")
        return False

def verify_otp(email, otp_input):
    record = OTP_STORE.get(email)
    if not record:
        return False, "ไม่มี OTP สำหรับอีเมลนี้"

    current_time = time.time()
    if current_time - record["timestamp"] > 300:
        return False, "OTP หมดอายุ (เกิน 5 นาที)"

    if record["otp"] != otp_input:
        return False, "OTP ไม่ถูกต้อง"

    return True, "ยืนยัน OTP สำเร็จ"
