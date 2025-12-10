import nltk
import re
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from database import save_booking, check_availability
from payment import validate_credit_card

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Initialize stopwords
stop_words = set(stopwords.words('english'))

# Intent patterns
patterns = {
    'greeting': r'(hello|hi|hey|greetings|howdy)',
    'farewell': r'(bye|goodbye|see you|farewell|thank you|thanks)',
    'booking': r'(book|reserve|entry)',
    'payment': r'(pay|payment|credit|card|transaction)',
    'info': r'(info|information|cost|price|hour|time|open|exhibit)',
    'cancel': r'(cancel|refund|return)',
    'help': r'(help|assist|support)'
}

# Responses
responses = {
    'greeting': [
        "Welcome to Museum Booking Assistant! How can I help you today?",
        "Hello! I'm here to help with museum tickets and information."
    ],
    'farewell': [
        "Thank you for using Museum Booking Assistant. Have a great day!",
        "Goodbye! We hope to see you at the museum soon."
    ],
    'booking_start': [
        "I can help you book tickets. What date are you planning to visit? (DD/MM/YYYY)",
        "Sure, let's book your tickets. When would you like to visit? (DD/MM/YYYY)"
    ],
    'booking_date': [
        "Great! How many tickets would you like to book?",
        "Excellent choice! How many people will be visiting?"
    ],
    'booking_tickets': [
        "Would you like regular admission or a special exhibition?",
        "Do you want to add any special shows or exhibitions to your visit?"
    ],
    'booking_confirmation': [
        "Your booking is confirmed! Total: ${price}. Your booking ID is {booking_id}.",
        "Tickets booked successfully! Total: ${price}. Booking reference: {booking_id}."
    ],
    'payment': [
        "Please enter your credit card details to complete the payment.",
        "To finalize your booking, I'll need your credit card information."
    ],
    'payment_success': [
        "Payment successful! Your tickets will be sent to your email.",
        "Thank you for your payment! Your booking is now confirmed."
    ],
    'info': [
        "The museum is open from 9 AM to 5 PM. Regular tickets are $15, children $8.",
        "We have various exhibits currently running. Entry fees start at $15."
    ],
    'cancel': [
        "I can help you cancel a booking. Please provide your booking ID.",
        "To process a refund, I'll need your booking reference number."
    ],
    'help': [
        "I can help with bookings, provide information, or assist with cancellations.",
        "How can I assist you? I can book tickets, provide information, or help with other queries."
    ],
    'fallback': [
        "I'm not sure I understand. Could you rephrase that?",
        "I didn't quite catch that. How else can I help you with museum tickets?"
    ]
}

# Booking state machine
def process_message(message, session):
    # Tokenize and preprocess
    tokens = word_tokenize(message.lower())
    filtered_tokens = [w for w in tokens if w not in stop_words]
    
    # Get current state
    state = session.get('state', 'init')
    
    # Detect intent
    intent = detect_intent(message)
    
    # State machine logic
    if intent == 'greeting' or state == 'init':
        session['state'] = 'ready'
        return random.choice(responses['greeting'])
    
    elif intent == 'farewell':
        session['state'] = 'init'
        return random.choice(responses['farewell'])
    
    elif intent == 'help':
        return random.choice(responses['help'])
    
    elif intent == 'info':
        return random.choice(responses['info'])
    
    elif intent == 'booking' and state in ['init', 'ready']:
        session['state'] = 'booking_date'
        return random.choice(responses['booking_start'])
    
    elif state == 'booking_date':
        # Extract date with regex
        date_pattern = r'\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}'
        dates = re.findall(date_pattern, message)
        
        if dates:
            session['booking_date'] = dates[0]
            session['state'] = 'booking_tickets'
            return random.choice(responses['booking_date'])
        else:
            return "Please provide a valid date (DD/MM/YYYY)."
    
    elif state == 'booking_tickets':
        # Extract number with regex
        num_pattern = r'\d+'
        nums = re.findall(num_pattern, message)
        
        if nums:
            session['num_tickets'] = int(nums[0])
            session['state'] = 'booking_type'
            return random.choice(responses['booking_tickets'])
        else:
            return "Please specify the number of tickets you need."
    
    elif state == 'booking_type':
        session['booking_type'] = 'regular' if 'regular' in message.lower() else 'special'
        
        # Calculate price
        price = session['num_tickets'] * (15 if session['booking_type'] == 'regular' else 25)
        session['price'] = price
        
        # Check availability
        if check_availability(session['booking_date'], session['num_tickets'], session['booking_type']):
            session['state'] = 'payment'
            return f"Total price: ${price}. " + random.choice(responses['payment'])
        else:
            return "Sorry, we don't have enough tickets available for that date. Please choose another date."
    
    elif state == 'payment':
        # Extract credit card with regex
        card_pattern = r'\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}'
        cards = re.findall(card_pattern, message)
        
        if cards:
            card_number = cards[0].replace('-', '').replace(' ', '')
            if validate_credit_card(card_number):
                # Save booking to database
                booking_id = save_booking(
                    session['booking_date'], 
                    session['num_tickets'], 
                    session['booking_type'],
                    session['price']
                )
                
                session['state'] = 'ready'
                return random.choice(responses['booking_confirmation']).format(
                    price=session['price'],
                    booking_id=booking_id
                )
            else:
                return "Invalid credit card. Please provide a valid card number."
        else:
            return "Please provide a valid credit card number to complete the booking."
    
    else:
        return random.choice(responses['fallback'])

def detect_intent(message):
    message = message.lower()
    
    for intent, pattern in patterns.items():
        if re.search(pattern, message):
            return intent
    
    return 'fallback'
