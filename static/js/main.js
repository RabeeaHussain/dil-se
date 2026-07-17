/* ==================== Main JS ==================== */

let userId = null;
let userLanguage = 'english';

// Initialize app on page load
document.addEventListener('DOMContentLoaded', function() {
    window.userReadyPromise = initializeApp();
});

async function initializeApp() {
    // Read either key format (main.js uses 'userId', auth.html uses 'user_id')
    let storedUserId = localStorage.getItem('userId') || localStorage.getItem('user_id');
    let storedLanguage = localStorage.getItem('userLanguage') || localStorage.getItem('language') || 'english';

    if (storedUserId) {
        try {
            await API.getUser(storedUserId);
            userId = storedUserId;
            userLanguage = storedLanguage;
            // Normalize to one key format
            localStorage.setItem('userId', userId);
            localStorage.setItem('userLanguage', userLanguage);
            const toggle = document.getElementById('languageToggle');
            if (toggle) toggle.value = userLanguage;
        } catch (error) {
            localStorage.removeItem('userId');
            localStorage.removeItem('user_id');
            localStorage.removeItem('userLanguage');
            localStorage.removeItem('language');
            await createUser();
        }
    } else {
        await createUser();
    }

    const languageToggle = document.getElementById('languageToggle');
    if (languageToggle) {
        languageToggle.addEventListener('change', function(e) {
            updateLanguage(e.target.value);
        });
    }
}

function createUser() {
    const data = {
        language: 'english'
    };
    
    return fetch('/api/user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            userId = data.user_id;
            userLanguage = data.language;
            localStorage.setItem('userId', userId);
            localStorage.setItem('userLanguage', userLanguage);
            console.log('User created:', userId);
        }
    })
    .catch(error => console.error('Error creating user:', error));
}

function updateLanguage(language) {
    userLanguage = language;
    localStorage.setItem('userLanguage', language);
    
    fetch(`/api/user/${userId}/language`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ language: language })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Language updated to:', language);
            // Reload page to update all content
            location.reload();
        }
    })
    .catch(error => console.error('Error updating language:', error));
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric' 
    });
}

function getMoodEmoji(mood) {
    const emojis = {
        1: '😢',
        2: '😞',
        3: '😐',
        4: '🙂',
        5: '😊'
    };
    return emojis[mood] || '😐';
}

function getMoodLabel(mood, lang = 'english') {
    if (lang === 'hinglish') {
        const labels = {
            1: 'Bilkul Bura',
            2: 'Bura',
            3: 'Theek Hai',
            4: 'Accha',
            5: 'Bahut Accha'
        };
        return labels[mood] || 'Theek Hai';
    } else {
        const labels = {
            1: 'Terrible',
            2: 'Bad',
            3: 'Okay',
            4: 'Good',
            5: 'Great'
        };
        return labels[mood] || 'Okay';
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#A8D5BA' : '#E8A9A9'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Scroll to bottom of chat
function scrollToBottom(element) {
    if (element) {
        element.scrollTop = element.scrollHeight;
    }
}

// Debounce function
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), delay);
    };
}
