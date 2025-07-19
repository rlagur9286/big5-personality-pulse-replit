// Global application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations and interactions
    initializeAnimations();
    initializeTooltips();
    
    // Add smooth scrolling to navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            // Skip empty or just '#' hrefs (like dropdown toggles)
            if (href === '#' || href === '') {
                return;
            }
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Initialize animations
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.6s ease-out forwards';
                entry.target.style.opacity = '1';
            }
        });
    }, observerOptions);

    // Observe elements with fade-in class
    document.querySelectorAll('.feature-card, .factor-card').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Keyboard navigation for test questions
function handleKeyboardNavigation() {
    document.addEventListener('keydown', function(e) {
        // Number keys (1-5) for answer selection
        if (e.key >= '1' && e.key <= '5') {
            const radioButton = document.querySelector(`input[name="answer"][value="${e.key}"]`);
            if (radioButton) {
                radioButton.checked = true;
                radioButton.dispatchEvent(new Event('change'));
                
                // Visual feedback
                const option = radioButton.closest('.answer-option');
                if (option) {
                    document.querySelectorAll('.answer-option').forEach(opt => 
                        opt.classList.remove('selected'));
                    option.classList.add('selected');
                }
            }
        }
        
        // Enter key for next question
        if (e.key === 'Enter') {
            const nextButton = document.getElementById('nextBtn');
            if (nextButton && !nextButton.disabled) {
                e.preventDefault();
                nextButton.click();
            }
        }
        
        // Escape key to go back
        if (e.key === 'Escape') {
            const backButton = document.querySelector('.btn-back');
            if (backButton) {
                backButton.click();
            }
        }
    });
}

// Progress bar animation
function animateProgressBar(targetPercentage) {
    const progressBar = document.querySelector('.progress-bar');
    if (!progressBar) return;
    
    let currentPercentage = 0;
    const increment = targetPercentage / 50; // 50 steps for smooth animation
    
    const timer = setInterval(() => {
        currentPercentage += increment;
        progressBar.style.width = currentPercentage + '%';
        
        if (currentPercentage >= targetPercentage) {
            clearInterval(timer);
            progressBar.style.width = targetPercentage + '%';
        }
    }, 20);
}

// Share functionality
function shareResults() {
    const shareData = {
        title: 'Big5 성격 테스트 결과',
        text: '나의 성격 분석 결과를 확인해보세요! 과학적으로 검증된 Big5 모델로 분석했습니다.',
        url: window.location.href
    };

    if (navigator.share && navigator.canShare && navigator.canShare(shareData)) {
        navigator.share(shareData)
            .then(() => console.log('Share successful'))
            .catch((error) => console.log('Error sharing:', error));
    } else {
        // Fallback: copy to clipboard
        const url = window.location.href;
        if (navigator.clipboard) {
            navigator.clipboard.writeText(url)
                .then(() => {
                    showNotification('결과 링크가 클립보드에 복사되었습니다!', 'success');
                })
                .catch(() => {
                    showShareModal(url);
                });
        } else {
            showShareModal(url);
        }
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification fade show`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Show share modal as fallback
function showShareModal(url) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">결과 공유하기</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>아래 링크를 복사하여 공유하세요:</p>
                    <div class="input-group">
                        <input type="text" class="form-control" value="${url}" readonly id="shareUrl">
                        <button class="btn btn-primary" onclick="copyShareUrl()">복사</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    modal.addEventListener('hidden.bs.modal', () => {
        document.body.removeChild(modal);
    });
}

// Copy share URL
function copyShareUrl() {
    const input = document.getElementById('shareUrl');
    input.select();
    document.execCommand('copy');
    showNotification('링크가 복사되었습니다!', 'success');
}

// Animate score circles (for results page)
function animateScoreCircles() {
    const scoreCircles = document.querySelectorAll('.score-circle');
    
    scoreCircles.forEach((circle, index) => {
        const score = parseFloat(circle.dataset.score);
        const circumference = 2 * Math.PI * 30; // radius = 30
        
        // Create SVG circle if not exists
        if (!circle.querySelector('svg')) {
            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('width', '80');
            svg.setAttribute('height', '80');
            svg.style.position = 'absolute';
            svg.style.top = '0';
            svg.style.left = '0';
            
            const bgCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            bgCircle.setAttribute('cx', '40');
            bgCircle.setAttribute('cy', '40');
            bgCircle.setAttribute('r', '30');
            bgCircle.setAttribute('fill', 'none');
            bgCircle.setAttribute('stroke', '#e2e8f0');
            bgCircle.setAttribute('stroke-width', '4');
            
            const progressCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            progressCircle.setAttribute('cx', '40');
            progressCircle.setAttribute('cy', '40');
            progressCircle.setAttribute('r', '30');
            progressCircle.setAttribute('fill', 'none');
            progressCircle.setAttribute('stroke', '#6366f1');
            progressCircle.setAttribute('stroke-width', '4');
            progressCircle.setAttribute('stroke-dasharray', circumference);
            progressCircle.setAttribute('stroke-dashoffset', circumference);
            progressCircle.setAttribute('transform', 'rotate(-90 40 40)');
            progressCircle.style.transition = 'stroke-dashoffset 1s ease-in-out';
            
            svg.appendChild(bgCircle);
            svg.appendChild(progressCircle);
            circle.appendChild(svg);
            
            // Animate after a delay
            setTimeout(() => {
                const offset = circumference - (score / 100) * circumference;
                progressCircle.setAttribute('stroke-dashoffset', offset);
            }, index * 200 + 500);
        }
    });
}

// Initialize score animations when results page loads
if (window.location.pathname.includes('results')) {
    document.addEventListener('DOMContentLoaded', animateScoreCircles);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: none;
        border-radius: 8px;
    }
`;
document.head.appendChild(style);

// Initialize keyboard navigation if on test page
if (window.location.pathname.includes('test')) {
    handleKeyboardNavigation();
}

// Auto-save test progress (if needed)
function saveTestProgress() {
    const answers = {};
    document.querySelectorAll('input[name="answer"]:checked').forEach(input => {
        const questionId = input.closest('form').dataset.questionId;
        if (questionId) {
            answers[questionId] = input.value;
        }
    });
    
    localStorage.setItem('big5_test_progress', JSON.stringify({
        answers: answers,
        timestamp: Date.now()
    }));
}

// Load test progress (if needed)
function loadTestProgress() {
    const saved = localStorage.getItem('big5_test_progress');
    if (saved) {
        try {
            const progress = JSON.parse(saved);
            // Check if progress is less than 1 hour old
            if (Date.now() - progress.timestamp < 3600000) {
                return progress.answers;
            }
        } catch (e) {
            console.error('Error loading test progress:', e);
        }
    }
    return {};
}

// Clear test progress
function clearTestProgress() {
    localStorage.removeItem('big5_test_progress');
}

// Export functions for global use
window.shareResults = shareResults;
window.copyShareUrl = copyShareUrl;
window.showNotification = showNotification;
