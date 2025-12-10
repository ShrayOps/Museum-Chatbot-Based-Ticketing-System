$(document).ready(function() {
    // Cache DOM elements
    const $chatMessages = $('#chat-messages');
    const $chatForm = $('#chat-form');
    const $userInput = $('#user-input');
    const $languageSelect = $('#language-select');

    // Current language
    let currentLanguage = 'en';

    // Function to add a message to chat
    function addMessage(message, type) {
        const timestamp = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        const messageElement = $(`
            <div class="message ${type}-message">
                <div class="message-content">${message}</div>
                <div class="message-timestamp">${timestamp}</div>
            </div>
        `);
        
        $chatMessages.append(messageElement);
        $chatMessages.scrollTop($chatMessages[0].scrollHeight);
    }

    // Typing indicator functions
    function showTypingIndicator() {
        const typingIndicator = $(`
            <div class="typing-indicator message bot-message">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `);
        $chatMessages.append(typingIndicator);
        $chatMessages.scrollTop($chatMessages[0].scrollHeight);
    }

    function removeTypingIndicator() {
        $('.typing-indicator').remove();
    }

    // Language name mapping
    function getLanguageName(code) {
        const languages = {
            'en': 'English',
            'hi': 'Hindi',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'ta': 'Tamil',
        };
        
        return languages[code] || code;
    }

    // Handle form submission
    $chatForm.on('submit', function(e) {
        e.preventDefault();
        const userMessage = $userInput.val().trim();
        
        if (userMessage) {
            // Add user message
            addMessage(userMessage, 'user');
            $userInput.val('');

            // Show typing indicator
            showTypingIndicator();

            // Get current language
            currentLanguage = $languageSelect.val();

            // Send message to server (AJAX)
            $.ajax({
                url: '/chat',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    message: userMessage,
                    language: currentLanguage
                }),
                success: function(data) {
                    // Remove typing indicator
                    removeTypingIndicator();

                    // Add bot response
                    addMessage(data.response, 'bot');
                    
                    // Check for payment trigger
                    if (data.response.toLowerCase().includes('credit card')) {
                        // Placeholder for payment modal logic
                    }
                },
                error: function(xhr, status, error) {
                    // Remove typing indicator
                    removeTypingIndicator();

                    console.error('Error:', error);
                    addMessage('Sorry, there was an error processing your request.', 'bot');
                }
            });
        }
    });

    // Handle language change
    $languageSelect.on('change', function() {
        currentLanguage = $(this).val();
        addMessage(`Language changed to ${getLanguageName(currentLanguage)}`, 'bot');
    });
});
