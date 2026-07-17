/* ==================== Exercises Page JS ==================== */

let currentExercise = null;
let exerciseStartTime = null;

document.addEventListener('DOMContentLoaded', function() {
    loadExercises();
});

function loadExercises() {
    API.getExercises(userId, userLanguage)
        .then(data => {
            const container = document.getElementById('exercisesList');
            if (!container) return;
            
            container.innerHTML = '';
            data.exercises.forEach(exercise => {
                const card = createExerciseCard(exercise);
                container.appendChild(card);
            });
        })
        .catch(handleApiError);
}

function createExerciseCard(exercise) {
    const card = document.createElement('div');
    card.className = 'exercise-card';
    
    card.innerHTML = `
        <div class="exercise-name">${exercise.name}</div>
        <div class="exercise-duration">⏱ ${exercise.duration} minutes</div>
        <div class="exercise-description">${exercise.description}</div>
        <button class="btn btn-secondary btn-small" onclick="openExerciseModal('${exercise.id}')">Learn More</button>
    `;
    
    return card;
}

function openExerciseModal(exerciseId) {
    API.getExercise(exerciseId, userLanguage)
        .then(exercise => {
            currentExercise = exercise;
            
            const modal = document.getElementById('exerciseModal');
            document.getElementById('exerciseTitle').textContent = exercise.name;
            
            let detailsHtml = `
                <div style="margin-bottom: 1.5rem;">
                    <p style="color: var(--dark-gray); line-height: 1.6;">${exercise.description}</p>
                </div>
                
                <h3 style="color: var(--deep-blue); margin-bottom: 1rem;">How It Works</h3>
                <p style="color: var(--dark-gray); margin-bottom: 1.5rem;">${exercise.how_it_works}</p>
                
                <h3 style="color: var(--deep-blue); margin-bottom: 1rem;">Steps</h3>
                <ol style="color: var(--dark-gray); margin-bottom: 1.5rem; padding-left: 1.5rem;">
            `;
            
            exercise.steps.forEach(step => {
                detailsHtml += `<li style="margin-bottom: 0.75rem;">${step}</li>`;
            });
            
            detailsHtml += `
                </ol>
                
                <h3 style="color: var(--deep-blue); margin-bottom: 0.5rem;">When to Use</h3>
                <p style="color: var(--dark-gray); margin-bottom: 1.5rem;">${exercise.when_to_use}</p>
                
                <h3 style="color: var(--deep-blue); margin-bottom: 0.5rem;">💡 Tip</h3>
                <p style="color: var(--dark-gray);">${exercise.tips}</p>
            `;
            
            document.getElementById('exerciseDetails').innerHTML = detailsHtml;
            
            modal.classList.add('active');
        })
        .catch(handleApiError);
}

function closeExerciseModal() {
    document.getElementById('exerciseModal').classList.remove('active');
    currentExercise = null;
}

document.getElementById('startExerciseBtn').addEventListener('click', function() {
    if (currentExercise) {
        startExercise(currentExercise);
    }
});

function startExercise(exercise) {
    closeExerciseModal();
    
    exerciseStartTime = Date.now();
    const modal = document.getElementById('exerciseProgressModal');
    document.getElementById('exerciseProgressTitle').textContent = exercise.name;
    
    let contentHtml = '';
    
    // Different UI for different exercises
    if (exercise.id === 'breathing_478') {
        contentHtml = createBreathingExercise(exercise);
    } else if (exercise.id === 'grounding_5432') {
        contentHtml = createGroundingExercise(exercise);
    } else if (exercise.id === 'body_scan') {
        contentHtml = createBodyScanExercise(exercise);
    } else if (exercise.id === 'gratitude_practice') {
        contentHtml = createGratitudeExercise(exercise);
    } else if (exercise.id === 'progressive_relax') {
        contentHtml = createProgressiveRelaxExercise(exercise);
    } else {
        contentHtml = `<p style="margin-bottom: 2rem;">${exercise.description}</p>`;
    }
    
    document.getElementById('exerciseProgressContent').innerHTML = contentHtml;
    modal.classList.add('active');
}

function createBreathingExercise(exercise) {
    return `
        <div style="margin-bottom: 2rem;">
            <p style="color: var(--dark-gray); margin-bottom: 1.5rem;">Follow the circle. When it expands, inhale. When it contracts, exhale.</p>
            
            <div style="
                width: 150px;
                height: 150px;
                margin: 2rem auto;
                background: linear-gradient(135deg, var(--deep-blue) 0%, var(--primary-blue) 100%);
                border-radius: 50%;
                animation: breathingCircle 36s ease-in-out infinite;
            "></div>
            
            <div id="breathingCounter" style="
                font-size: 1.2rem;
                color: var(--deep-blue);
                font-weight: 600;
                margin: 2rem 0;
            ">Cycle 1 of 5</div>
        </div>
        
        <style>
            @keyframes breathingCircle {
                0%, 100% { transform: scale(0.8); }
                25% { transform: scale(1); }
                50% { transform: scale(1.2); }
                75% { transform: scale(1); }
            }
        </style>
    `;
}

function createGroundingExercise(exercise) {
    const steps = [
        '5 things you can SEE',
        '4 things you can TOUCH',
        '3 things you can HEAR',
        '2 things you can SMELL',
        '1 thing you can TASTE'
    ];
    
    let html = '<div style="text-align: left; margin-bottom: 2rem;">';
    steps.forEach((step, index) => {
        html += `
            <div style="
                padding: 1rem;
                background: var(--primary-blue);
                border-radius: 8px;
                margin-bottom: 1rem;
                cursor: pointer;
                transition: var(--transition);
            " onmouseover="this.style.background='var(--primary-purple)'" onmouseout="this.style.background='var(--primary-blue)'">
                <strong style="font-size: 1.1rem; color: var(--deep-blue);">${step}</strong>
                <p style="color: var(--dark-gray); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Take your time noticing each one</p>
            </div>
        `;
    });
    html += '</div>';
    
    return html;
}

function createBodyScanExercise(exercise) {
    return `
        <p style="color: var(--dark-gray); margin-bottom: 2rem;">Follow along as we scan your body from head to toe:</p>
        <div style="margin-bottom: 2rem;">
            <div style="
                display: flex;
                flex-direction: column;
                gap: 1rem;
            ">
                <div class="body-part" style="padding: 1rem; background: var(--primary-blue); border-radius: 8px;">
                    <strong style="color: var(--deep-blue);">Head & Face</strong>
                    <p style="color: var(--dark-gray); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Relax your forehead, eyes, and jaw</p>
                </div>
                <div class="body-part" style="padding: 1rem; background: var(--primary-purple); border-radius: 8px;">
                    <strong style="color: var(--deep-blue);">Neck & Shoulders</strong>
                    <p style="color: var(--dark-gray); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Let them drop. Feel the release.</p>
                </div>
                <div class="body-part" style="padding: 1rem; background: var(--primary-blue); border-radius: 8px;">
                    <strong style="color: var(--deep-blue);">Chest & Arms</strong>
                    <p style="color: var(--dark-gray); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Let your arms feel heavy and relaxed</p>
                </div>
                <div class="body-part" style="padding: 1rem; background: var(--primary-purple); border-radius: 8px;">
                    <strong style="color: var(--deep-blue);">Stomach & Legs</strong>
                    <p style="color: var(--dark-gray); margin: 0.5rem 0 0 0; font-size: 0.9rem;">Soften your belly. Your legs are heavy.</p>
                </div>
            </div>
        </div>
    `;
}

function createGratitudeExercise(exercise) {
    return `
        <p style="color: var(--dark-gray); margin-bottom: 2rem;">Think about one thing for each:</p>
        <div style="margin-bottom: 2rem;">
            <div style="padding: 1rem; background: var(--primary-blue); border-radius: 8px; margin-bottom: 1rem;">
                <p style="margin: 0; color: var(--deep-blue); font-weight: 600;">Something bigger you're grateful for</p>
                <p style="margin: 0.5rem 0 0 0; color: var(--dark-gray); font-size: 0.9rem;">A person, achievement, or opportunity</p>
            </div>
            <div style="padding: 1rem; background: var(--primary-purple); border-radius: 8px; margin-bottom: 1rem;">
                <p style="margin: 0; color: var(--deep-blue); font-weight: 600;">Something small you're grateful for</p>
                <p style="margin: 0.5rem 0 0 0; color: var(--dark-gray); font-size: 0.9rem;">A good meal, sunshine, a song</p>
            </div>
            <div style="padding: 1rem; background: var(--primary-blue); border-radius: 8px;">
                <p style="margin: 0; color: var(--deep-blue); font-weight: 600;">Something about yourself you're grateful for</p>
                <p style="margin: 0.5rem 0 0 0; color: var(--dark-gray); font-size: 0.9rem;">A quality or how you handled something</p>
            </div>
        </div>
    `;
}

function createProgressiveRelaxExercise(exercise) {
    const groups = [
        'Hands & Fists',
        'Arms',
        'Shoulders',
        'Face & Jaw',
        'Stomach',
        'Legs'
    ];
    
    let html = '<p style="color: var(--dark-gray); margin-bottom: 1.5rem;">Tense each group for 5 seconds, then release.</p>';
    html += '<div style="margin-bottom: 2rem;">';
    
    groups.forEach(group => {
        html += `
            <div style="
                padding: 0.75rem;
                background: var(--light-gray);
                border-radius: 6px;
                margin-bottom: 0.75rem;
                color: var(--deep-blue);
                font-weight: 500;
            ">${group}</div>
        `;
    });
    
    html += '</div>';
    return html;
}

function closeExerciseProgress() {
    document.getElementById('exerciseProgressModal').classList.remove('active');
}

document.getElementById('completeExerciseBtn').addEventListener('click', function() {
    if (currentExercise) {
        const duration = Math.floor((Date.now() - exerciseStartTime) / 1000);
        
        API.logExerciseCompletion(userId, currentExercise.name, duration)
            .then(data => {
                closeExerciseProgress();
                showNotification(`Great job! You completed ${currentExercise.name} 🎉`, 'success');
            })
            .catch(handleApiError);
    }
});
