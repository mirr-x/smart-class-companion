// Smart Class Companion - Enhanced JavaScript

/**
 * DOM Content Loaded - Initialize all features
 */
document.addEventListener('DOMContentLoaded', function () {
    initializeMessages();
    initializeThemeToggle();
    initializeAnimations();
    initializeFormEnhancements();
    initializeRippleEffects();
    initializeSmoothScroll();
});

/**
 * Auto-hide messages with smooth animation
 */
function initializeMessages() {
    const messages = document.querySelectorAll('.alert');
    messages.forEach((message, index) => {
        // Stagger animation
        message.style.animationDelay = `${index * 100}ms`;

        // Auto-hide after 5 seconds
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s, transform 0.5s';
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
}

/**
 * Enhanced theme toggle with smooth transitions
 */
function initializeThemeToggle() {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;

    toggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        // Add transition class to body for smooth color changes
        document.body.style.transition = 'background 0.5s, color 0.5s';

        // Update theme
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        toggleBtn.textContent = newTheme === 'dark' ? '☀️' : '🌙';

        // Remove transition after animation completes
        setTimeout(() => {
            document.body.style.transition = '';
        }, 500);
    });
}

/**
 * Intersection Observer for scroll-triggered animations
 */
function initializeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe cards and sections
    const animatedElements = document.querySelectorAll(
        '.stat-card, .class-card, .lesson-item, .assignment-item, .member-card'
    );

    animatedElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.animationDelay = `${index * 50}ms`;
        observer.observe(element);
    });
}

/**
 * Enhanced form validation and interactions
 */
function initializeFormEnhancements() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');

        inputs.forEach(input => {
            // Add floating label effect
            addFloatingLabelEffect(input);

            // Real-time validation
            input.addEventListener('blur', () => validateInput(input));
            input.addEventListener('input', () => clearError(input));
        });

        // Form submission
        form.addEventListener('submit', (e) => {
            let isValid = true;
            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                showFormError(form);
            }
        });
    });
}

/**
 * Floating label effect for inputs
 */
function addFloatingLabelEffect(input) {
    const parent = input.closest('.form-group');
    if (!parent) return;

    const label = parent.querySelector('label');
    if (!label) return;

    // Check if input has value on load
    if (input.value) {
        label.classList.add('floating');
    }

    input.addEventListener('focus', () => {
        label.classList.add('floating');
    });

    input.addEventListener('blur', () => {
        if (!input.value) {
            label.classList.remove('floating');
        }
    });
}

/**
 * Validate individual input
 */
function validateInput(input) {
    const parent = input.closest('.form-group');
    if (!parent) return true;

    // Remove existing errors
    const existingError = parent.querySelector('.error');
    if (existingError) {
        existingError.remove();
    }

    // Check if required and empty
    if (input.hasAttribute('required') && !input.value.trim()) {
        showError(input, 'This field is required');
        return false;
    }

    // Email validation
    if (input.type === 'email' && input.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(input.value)) {
            showError(input, 'Please enter a valid email address');
            return false;
        }
    }

    // Password validation (if present)
    if (input.type === 'password' && input.value && input.value.length < 8) {
        showError(input, 'Password must be at least 8 characters');
        return false;
    }

    // Success state
    input.style.borderColor = 'var(--success)';
    setTimeout(() => {
        input.style.borderColor = '';
    }, 2000);

    return true;
}

/**
 * Show error message for input
 */
function showError(input, message) {
    const parent = input.closest('.form-group');
    if (!parent) return;

    input.style.borderColor = 'var(--danger)';

    const errorDiv = document.createElement('span');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    errorDiv.style.animation = 'slideDown 0.3s';

    parent.appendChild(errorDiv);
}

/**
 * Clear error state
 */
function clearError(input) {
    const parent = input.closest('.form-group');
    if (!parent) return;

    const existingError = parent.querySelector('.error');
    if (existingError) {
        existingError.style.animation = 'fadeOut 0.3s';
        setTimeout(() => existingError.remove(), 300);
    }

    input.style.borderColor = '';
}

/**
 * Show form-level error
 */
function showFormError(form) {
    const firstError = form.querySelector('.error');
    if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

/**
 * Ripple effect for buttons
 */
function initializeRippleEffects() {
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
}

/**
 * Smooth scroll for anchor links
 */
function initializeSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Animate stat numbers (count-up effect)
 */
function animateStatNumbers() {
    const statNumbers = document.querySelectorAll('.stat-number, .stat-card h3');

    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        if (isNaN(finalValue)) return;

        let currentValue = 0;
        const increment = Math.ceil(finalValue / 30);
        const duration = 1000;
        const stepTime = duration / 30;

        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                stat.textContent = finalValue;
                clearInterval(timer);
            } else {
                stat.textContent = currentValue;
            }
        }, stepTime);
    });
}

// Run stat animation when stats are visible
if (document.querySelector('.stat-number, .stat-card h3')) {
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateStatNumbers();
                statsObserver.disconnect();
            }
        });
    }, { threshold: 0.5 });

    const statsGrid = document.querySelector('.stats-grid');
    if (statsGrid) {
        statsObserver.observe(statsGrid);
    }
}

/**
 * Save form state to localStorage (for long forms)
 */
function initializeFormAutosave() {
    const longForms = document.querySelectorAll('form[data-autosave]');

    longForms.forEach(form => {
        const formId = form.getAttribute('id') || 'autosave-form';

        // Load saved data
        const savedData = localStorage.getItem(formId);
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(key => {
                    const input = form.querySelector(`[name="${key}"]`);
                    if (input) input.value = data[key];
                });
            } catch (e) {
                console.error('Error loading form data:', e);
            }
        }

        // Save on input
        form.addEventListener('input', () => {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            localStorage.setItem(formId, JSON.stringify(data));
        });

        // Clear on submit
        form.addEventListener('submit', () => {
            localStorage.removeItem(formId);
        });
    });
}

/**
 * Add loading state to buttons on form submit
 */
document.addEventListener('submit', function (e) {
    const submitBtn = e.target.querySelector('button[type="submit"]');
    if (submitBtn && !submitBtn.classList.contains('no-loading')) {
        submitBtn.disabled = true;
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Loading...';
        submitBtn.style.opacity = '0.7';

        // Re-enable after 3 seconds as failsafe
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
            submitBtn.style.opacity = '';
        }, 3000);
    }
});

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + K for theme toggle
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const themeBtn = document.getElementById('theme-toggle');
        if (themeBtn) themeBtn.click();
    }
});

/**
 * Add copy functionality for class codes
 */
document.addEventListener('click', function (e) {
    const codeElement = e.target.closest('.code-badge, .class-code strong');
    if (codeElement) {
        const text = codeElement.textContent.trim();
        navigator.clipboard.writeText(text).then(() => {
            // Show temporary tooltip
            const tooltip = document.createElement('div');
            tooltip.textContent = 'Copied!';
            tooltip.style.cssText = `
                position: absolute;
                background: var(--success);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                font-size: 0.875rem;
                font-weight: 600;
                z-index: 10000;
                animation: fadeIn 0.3s;
                pointer-events: none;
            `;

            const rect = codeElement.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.bottom + 10) + 'px';

            document.body.appendChild(tooltip);

            setTimeout(() => {
                tooltip.style.animation = 'fadeOut 0.3s';
                setTimeout(() => tooltip.remove(), 300);
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    }
});

// Add fadeOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
