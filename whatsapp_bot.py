import pywhatkit
import datetime

def send_whatsapp_message(phone_no, message):
    """Send a WhatsApp message instantly using PyWhatKit"""
    try:
        # Schedule message 1 minute from now to ensure it sends (pywhatkit requirement)
        now = datetime.datetime.now()
        send_time = now + datetime.timedelta(minutes=1)
        pywhatkit.sendwhatmsg(phone_no, message, send_time.hour, send_time.minute, wait_time=15, tab_close=True)
        print("WhatsApp message scheduled successfully!")
        return True
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
        return False
