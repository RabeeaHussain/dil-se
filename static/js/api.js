/* ==================== API Helper Functions ==================== */

/**
 * Safe fetch wrapper (prevents silent failures)
 */
async function safeFetch(url, options = {}) {
    const res = await fetch(url, options);

    let data;
    try {
        data = await res.json();
    } catch (e) {
        throw new Error("Invalid JSON response from server");
    }

    if (!res.ok) {
        throw new Error(data.error || `API Error: ${res.status}`);
    }

    return data;
}

/* ==================== API ==================== */

const API = {

    // ================= USER =================

    createUser: (username = null) => {
        return safeFetch('/api/user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username,
                language: userLanguage
            })
        });
    },

    getUser: (userId) => {
        return safeFetch(`/api/user/${userId}`);
    },

    updateLanguage: (userId, language) => {
        return safeFetch(`/api/user/${userId}/language`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ language })
        });
    },


    // ================= MOOD =================

    createMood: (userId, mood, note = '') => {
        return safeFetch(`/api/user/${userId}/mood`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mood, note })
        });
    },

    getMoodHistory: (userId, days = 7) => {
        return safeFetch(`/api/user/${userId}/mood?days=${days}`);
    },

    getStreak: (userId) => {
        return safeFetch(`/api/user/${userId}/streak`);
    },


    // ================= CHAT =================

    sendMessage: (userId, message) => {
        return safeFetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                message: message
            })
        });
    },

    getQuickReplies: (userId, language = 'english') => {
        return safeFetch(
            `/api/chat/quick-replies?user_id=${userId}&language=${language}`
        );
    },


    // ================= EXERCISES =================

    getExercises: (userId, language = 'english') => {
        return safeFetch(`/api/exercises?user_id=${userId}&language=${language}`);
    },

    getExercise: (exerciseId, language = 'english') => {
        return safeFetch(`/api/exercises/${exerciseId}?language=${language}`);
    },

    logExerciseCompletion: (userId, exerciseName, duration = 0) => {
        return safeFetch(`/api/user/${userId}/exercise-completion`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                exercise_name: exerciseName,
                duration_seconds: duration
            })
        });
    },

    getExerciseHistory: (userId, days = 30) => {
        return safeFetch(`/api/user/${userId}/exercise-history?days=${days}`);
    },


    // ================= JOURNAL =================

    createJournalEntry: (userId, content, mood = null, prompt = null) => {
        return safeFetch(`/api/user/${userId}/journal`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                content,
                mood,
                prompt_used: prompt
            })
        });
    },

    getJournalEntries: (userId, days = 90) => {
        return safeFetch(`/api/user/${userId}/journal?days=${days}`);
    },

    getJournalEntry: (entryId) => {
        return safeFetch(`/api/journal/${entryId}`);
    },

    updateJournalEntry: (entryId, content, mood = null) => {
        return safeFetch(`/api/journal/${entryId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content, mood })
        });
    },

    deleteJournalEntry: (entryId) => {
        return safeFetch(`/api/journal/${entryId}`, {
            method: 'DELETE'
        });
    },

    getJournalPrompts: (language = 'english') => {
        return safeFetch(`/api/journal/prompts?language=${language}`);
    }
};


/* ==================== ERROR HANDLER ==================== */

function handleApiError(error) {
    console.error('API Error:', error.message || error);
    showNotification(
        error.message || 'Something went wrong. Please try again.',
        'error'
    );
}