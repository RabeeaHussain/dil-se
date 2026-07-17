/* ==================== Home Page JS ==================== */


document.addEventListener('DOMContentLoaded', function() {
    const startHomeExperience = () => {
        loadMoodSelector();
        loadMoodHistory();
        loadStreak();
        loadDailyTip();
        loadMoodPrediction();
    };

    const ready = window.userReadyPromise || Promise.resolve();
    ready.then(() => {
        if (!userId) {
            window.location.href = '/auth';
            return;
        }
        startHomeExperience();
    });
});

const moodOptions = [
    { mood: 1, emoji: '😢', label: 'Terrible' },
    { mood: 2, emoji: '😞', label: 'Bad' },
    { mood: 3, emoji: '😐', label: 'Okay' },
    { mood: 4, emoji: '🙂', label: 'Good' },
    { mood: 5, emoji: '😊', label: 'Great' }
];

let selectedMood = null;

function loadMoodSelector() {
    const selector = document.getElementById('moodSelector');
    if (!selector) return;
    
    selector.addEventListener('click', function(e) {
        const option = e.target.closest('.mood-option');
        if (option) {
            selectedMood = parseInt(option.dataset.mood);
            
            // Update UI
            document.querySelectorAll('.mood-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            option.classList.add('selected');
            
            // Show form
            document.getElementById('moodForm').classList.remove('hidden');
        }
    });

    
    // Handle form submission
    document.getElementById('moodForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const note = document.getElementById('moodNote').value;
        
        API.createMood(userId, selectedMood, note)
            .then(data => {
                if (data.success) {
                    // Show success message
                    document.getElementById('moodSuccess').classList.remove('hidden');
                    document.getElementById('moodForm').classList.add('hidden');
                    
                   setTimeout(() => {
                        loadMoodHistory();
                        loadStreak();
                        loadMoodPrediction();
                    }, 2000);
                }
            })
            .catch(handleApiError);
    });
}

function loadMoodPrediction() {
    if (!userId) return;
    fetch(`/api/user/${userId}/mood-prediction`)
        .then(r => r.json())
        .then(data => {
            const card = document.getElementById('predictionCard');
            const text = document.getElementById('predictionText');
            const trend = document.getElementById('predictionTrend');
            if (card && data.predicted_mood) {
                card.style.display = 'block';
                text.textContent = data.message;
                trend.textContent = `Trend: ${data.trend}`;
            } else if (card && data.message) {
                card.style.display = 'block';
                text.textContent = data.message;
            }
        })
        .catch(error => {
            if ((error && error.message && error.message.includes('404')) || error?.status === 404) {
                return;
            }
            handleApiError(error);
        });
}
function loadMoodHistory() {
    API.getMoodHistory(userId, 7)
        .then(data => {
            const container = document.getElementById('moodHistory');
            if (!container) return;

            
            if (data.moods && data.moods.length > 0) {
                let html = '<div style="display: flex; gap: 0.5rem; align-items: flex-end;">';
                
                // Create bars for each day
                for (let i = 6; i >= 0; i--) {
                    const date = new Date();
                    date.setDate(date.getDate() - i);
                    const dateStr = date.toISOString().split('T')[0];
                    
                    const entry = data.moods.find(m => m.date === dateStr);
                    const mood = entry ? entry.mood : 0;
                    const height = mood * 15 + 10; // Scale height based on mood
                    const day = date.toLocaleDateString('en-US', { weekday: 'short' });
                    
                    html += `
                        <div style="text-align: center; flex: 1;">
                            <div style="
                                background: linear-gradient(180deg, var(--deep-blue) 0%, var(--primary-blue) 100%);
                                height: ${height}px;
                                border-radius: 4px;
                                margin-bottom: 0.5rem;
                                ${mood === 0 ? 'opacity: 0.3;' : ''}
                            "></div>
                            <small style="font-size: 0.75rem; color: var(--dark-gray);">${day}</small>
                        </div>
                    `;
                }
                
                html += '</div>';
                container.innerHTML = html;
            }
        })
        .catch(handleApiError);
}

function loadStreak() {
    API.getStreak(userId)
        .then(data => {
            const counter = document.getElementById('streakCounter');
            if (counter) {
                counter.textContent = data.streak;
            }
        })
        .catch(handleApiError);
}

function loadDailyTip() {
    const tips = [
        'Take a deep breath. You\'re doing better than you think.',
        'It\'s okay to not be okay. That\'s what support is for.',
        'Your feelings are valid, even if no one else understands.',
        'Small steps count. Progress isn\'t always visible, but it\'s real.',
        'You don\'t have to have it all figured out. Nobody does.',
        'Being strong doesn\'t mean never being tired or sad.',
        'Asking for help is brave, not weak.',
        'Your worth isn\'t determined by productivity or success.',
        'Healing isn\'t linear. Bad days don\'t erase progress.',
        'You\'re allowed to change your mind, your goals, your path.'
    ];
    
    const tip = tips[Math.floor(Math.random() * tips.length)];
    const tipElement = document.getElementById('dailyTip');
    if (tipElement) {
        tipElement.textContent = tip;
    }
}
