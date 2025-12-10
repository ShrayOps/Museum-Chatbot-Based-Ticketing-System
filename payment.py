def validate_credit_card(card_number):
    """
    Validates a credit card number using the Luhn algorithm.
    This is a simple implementation for demonstration purposes.
    """
    # Remove any non-digit characters
    card_number = ''.join(filter(str.isdigit, card_number))
    
    # Check if the card number is of valid length
    if not 13 <= len(card_number) <= 19:
        return False
    
    # Luhn algorithm
    digits = [int(d) for d in card_number]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    
    for digit in even_digits:
        checksum += sum(divmod(digit * 2, 10))
    
    return checksum % 10 == 0

def process_payment(card_number, expiry, cvv, amount):
    """
    Simulate payment processing. 
    In a real application, this would integrate with a payment gateway.
    """
    # Validate card details
    if not validate_credit_card(card_number):
        return False, "Invalid card number"
    
    # Check expiry format (MM/YY)
    if not (len(expiry) == 5 and expiry[2] == '/'):
        return False, "Invalid expiry date format"
    
    # Check CVV (3 or 4 digits)
    if not (len(cvv) in [3, 4] and cvv.isdigit()):
        return False, "Invalid CVV"
    
    return True, "Payment processed successfully"
