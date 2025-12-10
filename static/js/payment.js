$(document).ready(function() {
    // Simple credit card validation
    function validateCreditCard(cardNumber) {
        // Remove spaces and dashes
        cardNumber = cardNumber.replace(/[\s-]/g, '');
        
        // Check if card number contains only digits
        if (!/^\d+$/.test(cardNumber)) {
            return false;
        }
        
        // Check length (13-19 digits)
        if (cardNumber.length < 13 || cardNumber.length > 19) {
            return false;
        }
        
        // Luhn algorithm
        let sum = 0;
        let doubleUp = false;
        
        // Process each digit
        for (let i = cardNumber.length - 1; i >= 0; i--) {
            let digit = parseInt(cardNumber.charAt(i));
            
            if (doubleUp) {
                digit *= 2;
                if (digit > 9) {
                    digit -= 9;
                }
            }
            
            sum += digit;
            doubleUp = !doubleUp;
        }
        
        // If sum is divisible by 10, the card number is valid
        return sum % 10 === 0;
    }
    
    // Function to format card number with spaces
    function formatCardNumber(cardNumber) {
        // Remove existing spaces
        cardNumber = cardNumber.replace(/\s/g, '');
        // Add a space after every 4 characters
        return cardNumber.replace(/(\d{4})(?=\d)/g, '$1 ');
    }
    
    // Card number input event handler
    $('#card-number').on('input', function() {
        let cardNumber = $(this).val();
        
        // Format the card number
        cardNumber = formatCardNumber(cardNumber);
        
        // Update the input value
        $(this).val(cardNumber);
        
        // Validate the card number
        if (validateCreditCard(cardNumber)) {
            $(this).removeClass('is-invalid').addClass('is-valid');
        } else {
            $(this).removeClass('is-valid').addClass('is-invalid');
        }
    });
    
    // Expiry date validation
    $('#expiry-date').on('input', function() {
        let value = $(this).val();
        
        // Remove non-digits
        value = value.replace(/\D/g, '');
        
        // Format as MM/YY
        if (value.length > 2) {
            value = value.substring(0, 2) + '/' + value.substring(2, 4);
        }
        
        $(this).val(value);
        
        // Basic validation: Must be MM/YY format
        const isValid = /^\d{2}\/\d{2}$/.test(value);
        
        if (isValid) {
            $(this).removeClass('is-invalid').addClass('is-valid');
        } else {
            $(this).removeClass('is-valid').addClass('is-invalid');
        }
    });
    
    // CVV validation
    $('#cvv').on('input', function() {
        const cvv = $(this).val();
        
        // CVV must be 3 or 4 digits
        const isValid = /^\d{3,4}$/.test(cvv);
        
        if (isValid) {
            $(this).removeClass('is-invalid').addClass('is-valid');
        } else {
            $(this).removeClass('is-valid').addClass('is-invalid');
        }
    });
    
    // Payment form submission
    $('#payment-form').on('submit', function(e) {
        e.preventDefault();
        
        const cardNumber = $('#card-number').val().replace(/\s/g, '');
        const expiryDate = $('#expiry-date').val();
        const cvv = $('#cvv').val();
        
        // Validate all fields
        if (validateCreditCard(cardNumber) && 
            /^\d{2}\/\d{2}$/.test(expiryDate) && 
            /^\d{3,4}$/.test(cvv)) {
            
            // In a real application, send this to server for processing
            // For demo purposes, just show success message
            $('#payment-status').html('<div class="alert alert-success">Payment successful!</div>');
            
            // Close modal after payment
            setTimeout(function() {
                $('#payment-modal').modal('hide');
                
                // Add confirmation message to chat
                $('#chat-messages').append(
                    $('<div>').addClass('message bot-message')
                        .append($('<div>').addClass('message-content')
                            .text('Payment successful! Your tickets are confirmed.'))
                );
            }, 1500);
        } else {
            $('#payment-status').html('<div class="alert alert-danger">Please check your card details.</div>');
        }
    });
});
