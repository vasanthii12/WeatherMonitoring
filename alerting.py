import smtplib
from email.message import EmailMessage
from config import TEMP_THRESHOLD, CONSECUTIVE_ALERTS, CITIES, EMAIL_CONFIG


class AlertSystem:
    def __init__(self):
        self.alert_count = {city: 0 for city in CITIES}

    def check_temperature_threshold(self, city, temp):
        if temp > TEMP_THRESHOLD:
            self.alert_count[city] += 1
            if self.alert_count[city] >= CONSECUTIVE_ALERTS:
                self.trigger_alert(city, temp)
        else:
            self.alert_count[city] = 0


    def trigger_alert(self, city, temp):
        message = f"ALERT: Temperature in {city} has exceeded {TEMP_THRESHOLD}°C for {CONSECUTIVE_ALERTS} consecutive updates. Current temperature: {temp}°C"
        print(message)
        self.send_email_alert(message)

    def send_email_alert(self, message):
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = 'Temperature Alert'
        msg['From'] = EMAIL_CONFIG['sender']
        msg['To'] = EMAIL_CONFIG['recipient']

        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
            server.send_message(msg)