/* ==================== Journal Page JS ==================== */

document.addEventListener('DOMContentLoaded', async function () {
    if (window.userReadyPromise) {
        await window.userReadyPromise;
    }

    console.log("Journal User ID:", userId);

    loadJournalPrompts();
    loadJournalEntries();
    setupJournalForm();
});

function setupJournalForm() {
    const form = document.getElementById('journalForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const content = document.getElementById('journalContent').value.trim();
        const mood = document.getElementById('journalMood').value;
        
        if (!content) {
            showNotification('Please write something first', 'error');
            return;
        }
        
        const moodInt = mood ? parseInt(mood) : null;
        
        if (!userId) {
            showNotification("Please log in again.", "error");
            return;
        }
        console.log("Journal page userId:", userId);
        console.log("localStorage userId:", localStorage.getItem("userId"));
        console.log("localStorage user_id:", localStorage.getItem("user_id"));


        API.createJournalEntry(userId, content, moodInt)
            .then(data => {
                if (data.success) {
                    // Show success
                    document.getElementById('journalSuccess').classList.remove('hidden');
                    
                    // Reset form
                    form.reset();
                    
                    // Reload entries
                    setTimeout(() => {
                        document.getElementById('journalSuccess').classList.add('hidden');
                        loadJournalEntries();
                    }, 2000);
                }
            })
            .catch(handleApiError);
    });
}

function loadJournalPrompts() {
    API.getJournalPrompts(userLanguage)
        .then(data => {
            const container = document.getElementById('journalPrompts');
            if (!container) return;
            
            container.innerHTML = '';
            data.prompts.forEach((prompt, index) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'quick-reply';
                button.style.background = 'var(--primary-blue)';
                button.style.color = 'var(--deep-blue)';
                button.textContent = prompt;
                
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    document.getElementById('journalContent').value = prompt + '\n\n';
                    document.getElementById('journalContent').focus();
                });
                
                container.appendChild(button);
            });
        })
        .catch(handleApiError);
}

function loadJournalEntries() {
    if (!userId) {
        console.error("User ID is null");
        return;
    }

    API.getJournalEntries(userId, 90)
        .then(data => {
            const container = document.getElementById('journalEntries');
            if (!container) return;
            
            if (!data.entries || data.entries.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📚</div>
                        <p>No entries yet. Start by writing one today!</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = '';
            data.entries.forEach(entry => {
                const card = createEntryCard(entry);
                container.appendChild(card);
            });
        })
        .catch(handleApiError);
}

function createEntryCard(entry) {
    const card = document.createElement('div');
    card.className = 'journal-entry-card';
    
    const date = new Date(entry.date);
    const formattedDate = date.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    
    const moodEmoji = entry.mood_at_time ? getMoodEmoji(entry.mood_at_time) : '';
    
    // Truncate content for preview
    const preview = entry.content.length > 300 
        ? entry.content.substring(0, 300) + '...' 
        : entry.content;
    
    card.innerHTML = `
        <div class="entry-date">${formattedDate}</div>
        ${moodEmoji ? `<div class="entry-mood">${moodEmoji}</div>` : ''}
        <div class="entry-content">${escapeHtml(preview)}</div>
        <div class="entry-actions">
            <button class="btn-edit" onclick="editEntry(${entry.id})">Edit</button>
            <button class="btn-delete" onclick="deleteEntry(${entry.id})">Delete</button>
        </div>
    `;
    
    return card;
}

function editEntry(entryId) {
    API.getJournalEntry(entryId)
        .then(entry => {
            document.getElementById('editEntryId').value = entryId;
            document.getElementById('editJournalContent').value = entry.content;
            document.getElementById('editJournalMood').value = entry.mood_at_time || '';
            
            document.getElementById('editJournalModal').classList.add('active');
        })
        .catch(handleApiError);
}

function closeEditModal() {
    document.getElementById('editJournalModal').classList.remove('active');
}

function deleteEntry(entryId) {
    if (confirm('Are you sure you want to delete this entry? This cannot be undone.')) {
        API.deleteJournalEntry(entryId)
            .then(data => {
                if (data.success) {
                    showNotification('Entry deleted', 'success');
                    loadJournalEntries();
                }
            })
            .catch(handleApiError);
    }
}

// Handle edit form submission
document.addEventListener('DOMContentLoaded', function() {
    const editForm = document.getElementById('editJournalForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const entryId = parseInt(document.getElementById('editEntryId').value);
            const content = document.getElementById('editJournalContent').value.trim();
            const mood = document.getElementById('editJournalMood').value;
            
            if (!content) {
                showNotification('Please write something', 'error');
                return;
            }
            
            const moodInt = mood ? parseInt(mood) : null;
            
            API.updateJournalEntry(entryId, content, moodInt)
                .then(data => {
                    if (data.success) {
                        closeEditModal();
                        showNotification('Entry updated', 'success');
                        loadJournalEntries();
                    }
                })
                .catch(handleApiError);
        });
    }
});

// Utility to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
