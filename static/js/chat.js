/* ==================== Chat Page JS ==================== */

document.addEventListener('DOMContentLoaded', function() {
    loadQuickReplies();
    setupChatForm();
});

function setupChatForm() {
    const form = document.getElementById('chatForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        addMessageToChat(message, 'user');
        input.value = '';
        
        // Show loading indicator
        showLoadingMessage();
        
        // Send to API
        API.sendMessage(userId, message, userLanguage)
            .then(data => {
                if (data.success) {
                    // Remove loading indicator
                    removeLoadingMessage();
                    
                    // Add bot response
                    addMessageToChat(data.response, 'bot');
                }
            })
            .catch(error => {
                removeLoadingMessage();
                handleApiError(error);
            });
    });
}

function addMessageToChat(message, role) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = message;
    
    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom(messagesContainer);
}

function showLoadingMessage() {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.id = 'loadingMessage';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.innerHTML = '<div class="loading"></div>';
    
    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);
    
    scrollToBottom(messagesContainer);
}

function removeLoadingMessage() {
    const loading = document.getElementById('loadingMessage');
    if (loading) {
        loading.remove();
    }
}

function loadQuickReplies() {
    API.getQuickReplies(userId, userLanguage)
        .then(data => {
            const container = document.getElementById('quickReplies');
            if (!container) return;
            
            container.innerHTML = '';
            data.quick_replies.forEach(reply => {
                const button = document.createElement('button');
                button.className = 'quick-reply';
                button.textContent = reply;
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    // Get the input field
                    const input = document.getElementById('chatInput');
                    input.value = reply;
                    
                    // Submit the form
                    document.getElementById('chatForm').dispatchEvent(new Event('submit'));
                });
                
                container.appendChild(button);
            });
        })
        .catch(handleApiError);
}
