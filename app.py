# -*- coding: utf-8 -*-
"""
SwasthyaGuide - Flask Web Application
Twilio WhatsApp webhook integration for healthcare assistance
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import SwasthyaGuide

# Initialize Flask app
app = Flask(__name__)

# Initialize SwasthyaGuide bot instance globally
bot = SwasthyaGuide()


@app.route('/')
def home():
    """Root route - health check"""
    return "SwasthyaGuide is Running! 🏥"


@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    WhatsApp webhook endpoint
    Receives messages from Twilio and responds with health guidance
    """
    # Extract incoming message from Twilio request
    incoming_msg = request.values.get('Body', '').strip()
    
    # Get sender's phone number (optional, for logging)
    sender = request.values.get('From', '')
    
    # Process message through SwasthyaGuide bot
    bot_response = bot.process_message(incoming_msg)
    
    # Create Twilio response
    resp = MessagingResponse()
    resp.message(bot_response)
    
    return str(resp)


if __name__ == '__main__':
    # Run Flask app locally for testing
    app.run(debug=True, host='0.0.0.0', port=5000)
