(elements,arg)=>{
    // Define the showAlert function globally on the window object
    window.showAlert = function(type, message, title, timeout, direction, position, showCountdown = false) {
        // Create a unique ID for each alert container based on the position
        const containerId = 'alert-container-' + position;
        let alertContainer = document.querySelector('#' + containerId);

        // Initialize the alert container if it does not exist
        if (!alertContainer) {
            alertContainer = document.createElement('div');
            alertContainer.id = containerId;
            alertContainer.style.position = 'fixed';
            alertContainer.style.zIndex = '9999';
            alertContainer.style.display = 'flex';
            alertContainer.style.flexDirection = 'column';
            alertContainer.style.gap = '12px';
            alertContainer.style.pointerEvents = 'none';
            alertContainer.style.overflowY = 'auto';
            alertContainer.style.maxHeight = '80vh'; // Use viewport height for better responsiveness
            alertContainer.style.scrollBehavior = 'smooth';

            // Accessibility improvements
            alertContainer.setAttribute('role', 'log');
            alertContainer.setAttribute('aria-live', 'polite');
            alertContainer.setAttribute('aria-relevant', 'additions');

            // Hide the scroll bar
            alertContainer.style.msOverflowStyle = 'none';
            alertContainer.style.scrollbarWidth = 'none';
            alertContainer.style.overflowX = 'hidden';

            // Add WebKit-specific scroll bar hiding style
            const styleElement = document.createElement('style');
            styleElement.innerHTML = `
            #${containerId}::-webkit-scrollbar {
                display: none;
            }

            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }

            @media (max-width: 768px) {
                .custom-alert {
                    max-width: 85vw !important;
                    padding: 14px 16px !important;
                    font-size: 14px !important;
                }

                #${containerId} {
                    max-width: 90vw;
                    margin: 0 10px;
                }
            }
            `;
            document.head.appendChild(styleElement);

            // Define positions with responsive margins
            const positions = {
                'top-left': { top: '20px', left: '20px', alignItems: 'flex-start' },
                'top-middle': { top: '20px', left: '50%', transform: 'translateX(-50%)', alignItems: 'center' },
                'top-right': { top: '20px', right: '20px', alignItems: 'flex-end' },
                'bottom-left': { bottom: '20px', left: '20px', alignItems: 'flex-start' },
                'bottom-middle': { bottom: '20px', left: '50%', transform: 'translateX(-50%)', alignItems: 'center' },
                'bottom-right': { bottom: '20px', right: '20px', alignItems: 'flex-end' }
            };

            // Apply position styles
            const positionStyles = positions[position] || positions['bottom-right'];
            Object.assign(alertContainer.style, positionStyles);

            document.body.insertAdjacentElement('beforeend', alertContainer);

            // Add global keyboard listener for ESC key (if not already added)
            if (!window.alertEscapeKeyListener) {
                window.alertEscapeKeyListener = function(e) {
                    if (e.key === 'Escape') {
                        // Close the most recent alert
                        document.querySelectorAll('.custom-alert').forEach(alert => {
                            alert.dispatchEvent(new Event('alertClose'));
                        });
                    }
                };
                document.addEventListener('keydown', window.alertEscapeKeyListener);
            }
        }

        // Limit the number of alerts to prevent performance issues
        const maxAlerts = 5;
        const currentAlerts = alertContainer.querySelectorAll('.custom-alert');
        if (currentAlerts.length >= maxAlerts) {
            // Remove the oldest alert
            currentAlerts[0].remove();
        }

        // Create an alert element with the unpacked arguments
        const alert = document.createElement('div');
        alert.className = 'custom-alert wield-alert';
        alert.style.maxWidth = '400px';
        alert.style.width = 'calc(100% - 40px)';
        alert.style.padding = '16px 20px';
        alert.style.borderRadius = '8px';
        alert.style.fontSize = '15px';
        alert.style.fontFamily = "'Roboto', 'Segoe UI', 'Arial', sans-serif";
        alert.style.display = 'flex';
        alert.style.alignItems = 'center';
        alert.style.justifyContent = 'space-between';
        alert.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.15)';
        alert.style.opacity = '0';
        alert.style.pointerEvents = 'auto';
        alert.style.transition = 'opacity 0.4s ease-out, transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)'; // Added bounce effect
        alert.style.position = 'relative';
        alert.style.transform = direction === 'ltr' ? 'translateX(100%)' : 'translateX(-100%)';

        // Accessibility attributes
        alert.setAttribute('role', 'alert');
        alert.setAttribute('aria-atomic', 'true');

        // Enhanced color schemes object with improved contrast (meets WCAG AA standards)
        const colorSchemes = {
            success: {
                bg: '#1E8E3E', // Richer green
                color: '#ffffff',
                iconBg: '#34A853',
                progressColor: '#81C995',
                gradient: 'linear-gradient(135deg, #1E8E3E, #34A853)'
            },
            error: {
                bg: '#D93025', // Deeper red
                color: '#ffffff',
                iconBg: '#EA4335',
                progressColor: '#F28B82',
                gradient: 'linear-gradient(135deg, #D93025, #EA4335)'
            },
            info: {
                bg: '#1A73E8', // Google blue
                color: '#ffffff',
                iconBg: '#4285F4',
                progressColor: '#8AB4F8',
                gradient: 'linear-gradient(135deg, #1A73E8, #4285F4)'
            },
            warning: {
                bg: '#E37400', // Warmer orange
                color: '#ffffff',
                iconBg: '#FBBC04',
                progressColor: '#FDE293',
                gradient: 'linear-gradient(135deg, #E37400, #FBBC04)'
            },
            waiting: {
                bg: '#9C27B0', // Purple
                color: '#ffffff',
                iconBg: '#AB47BC',
                progressColor: '#CE93D8',
                gradient: 'linear-gradient(135deg, #9C27B0, #AB47BC)'
            },
            critical: {
                bg: '#B31412', // Deeper critical red
                color: '#ffffff',
                iconBg: '#C5221F',
                progressColor: '#F6AEA9',
                gradient: 'linear-gradient(135deg, #B31412, #C5221F)'
            },
            debug: {
                bg: '#3C4043', // Refined dark gray
                color: '#ffffff',
                iconBg: '#5F6368',
                progressColor: '#9AA0A6',
                gradient: 'linear-gradient(135deg, #3C4043, #5F6368)'
            },
            default: {
                bg: '#202124', // Near black
                color: '#ffffff',
                iconBg: '#5F6368',
                progressColor: '#9AA0A6',
                gradient: 'linear-gradient(135deg, #202124, #5F6368)'
            }
        };

        // Get the color scheme or default to 'default'
        const scheme = colorSchemes[type] || colorSchemes.default;

        alert.style.backgroundColor = scheme.bg;
        alert.style.background = scheme.gradient;
        alert.style.color = scheme.color;
        alert.style.direction = direction;

        // Enhanced SVG icons with built-in animations
        const svgIcons = {
            success: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <style>
                    @keyframes successCircle {
                        0% { stroke-dasharray: 0 100; stroke-dashoffset: 0; }
                        100% { stroke-dasharray: 100 100; stroke-dashoffset: 0; }
                    }
                    @keyframes successCheck {
                        0% { stroke-dasharray: 0 100; stroke-dashoffset: 0; opacity: 0; }
                        30% { opacity: 1; }
                        100% { stroke-dasharray: 100 100; stroke-dashoffset: 0; opacity: 1; }
                    }
                    .success-circle { animation: successCircle 0.8s ease-in-out forwards; }
                    .success-check { animation: successCheck 0.5s ease-in-out 0.6s forwards; }
                </style>
                <circle class="success-circle" cx="12" cy="12" r="10" stroke-width="2" fill="none" />
                <polyline class="success-check" points="7,13 10,16 17,9" stroke-width="2.5" fill="none" opacity="0" />
            </svg>`,

            error: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <style>
                    @keyframes errorCircle {
                        0% { transform: scale(0.5); opacity: 0; }
                        30% { transform: scale(1.2); }
                        100% { transform: scale(1); opacity: 1; }
                    }
                    @keyframes errorX {
                        0% { transform: scale(0); opacity: 0; }
                        50% { transform: scale(1.4); }
                        100% { transform: scale(1); opacity: 1; }
                    }
                    .error-circle { animation: errorCircle 0.5s cubic-bezier(0.36, 0.66, 0.04, 1) forwards; }
                    .error-x { animation: errorX 0.5s cubic-bezier(0.36, 0.66, 0.04, 1) 0.3s forwards; }
                </style>
                <circle class="error-circle" cx="12" cy="12" r="10" stroke-width="2" fill="none" />
                <g class="error-x" opacity="0">
                    <line x1="15" y1="9" x2="9" y2="15" stroke-width="2"></line>
                    <line x1="9" y1="9" x2="15" y2="15" stroke-width="2"></line>
                </g>
            </svg>`,

            info: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <style>
                    @keyframes infoCircle {
                        0% { transform: scale(0) rotate(-180deg); opacity: 0; }
                        100% { transform: scale(1) rotate(0deg); opacity: 1; }
                    }
                    @keyframes infoDot {
                        0% { transform: scale(0); opacity: 0; }
                        100% { transform: scale(1); opacity: 1; }
                    }
                    @keyframes infoLine {
                        0% { transform: scaleY(0); transform-origin: top; }
                        100% { transform: scaleY(1); transform-origin: top; }
                    }
                    .info-circle { animation: infoCircle 0.6s cubic-bezier(0.36, 0.66, 0.04, 1) forwards; }
                    .info-dot { animation: infoDot 0.3s ease 0.6s forwards; }
                    .info-line { animation: infoLine 0.4s ease 0.8s forwards; }
                </style>
                <circle class="info-circle" cx="12" cy="12" r="10" opacity="0" />
                <line class="info-line" x1="12" y1="16" x2="12" y2="12" transform="scaleY(0)" />
                <circle class="info-dot" cx="12" cy="8" r="1" opacity="0" />
            </svg>`,

            warning: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <style>
                    @keyframes warningTriangle {
                        0% { transform: translateY(-10px); opacity: 0; }
                        40% { transform: translateY(5px); }
                        70% { transform: translateY(-2px); }
                        100% { transform: translateY(0); opacity: 1; }
                    }
                    @keyframes warningBlink {
                        0%, 20%, 40% { opacity: 0; }
                        10%, 30%, 50%, 100% { opacity: 1; }
                    }
                    .warning-triangle { animation: warningTriangle 0.7s cubic-bezier(0.36, 0.66, 0.04, 1) forwards; }
                    .warning-line { animation: warningBlink 1s ease 0.7s forwards; }
                    .warning-dot { animation: warningBlink 0.5s ease 1.2s forwards; }
                </style>
                <path class="warning-triangle" d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" opacity="0" />
                <line class="warning-line" x1="12" y1="9" x2="12" y2="13" opacity="0" />
                <line class="warning-dot" x1="12" y1="17" x2="12.01" y2="17" opacity="0" />
            </svg>`,

            waiting: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <style>
                    @keyframes waitingCircle {
                        0% { stroke-dasharray: 0 100; }
                        100% { stroke-dasharray: 100 100; }
                    }
                    @keyframes waitingHand {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    @keyframes waitingPulse {
                        0%, 100% { transform: scale(1); }
                        50% { transform: scale(1.05); }
                    }
                    .waiting-circle { animation: waitingCircle 1s linear forwards, waitingPulse 2s ease infinite; }
                    .waiting-hand { animation: waitingHand 8s linear infinite; transform-origin: center; }
                </style>
                <circle class="waiting-circle" cx="12" cy="12" r="10" stroke-dasharray="0 100" />
                <g class="waiting-hand" transform-origin="12 12">
                    <line x1="12" y1="12" x2="12" y2="6" />
                    <line x1="12" y1="12" x2="16" y2="14" />
                </g>
            </svg>`,

            critical: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <style>
                    @keyframes criticalOctagon {
                        0% { transform: scale(0); opacity: 0; }
                        60% { transform: scale(1.2); }
                        80% { transform: scale(0.9); }
                        100% { transform: scale(1); opacity: 1; }
                    }
                    @keyframes criticalPulse {
                        0%, 100% { transform: scale(1); opacity: 1; }
                        50% { transform: scale(1.1); opacity: 0.8; }
                    }
                    @keyframes criticalExclamation {
                        0%, 40% { opacity: 0; transform: translateY(-5px); }
                        100% { opacity: 1; transform: translateY(0); }
                    }
                    .critical-octagon { animation: criticalOctagon 0.6s cubic-bezier(0.36, 0.66, 0.04, 1) forwards, criticalPulse 2s linear 0.6s infinite; }
                    .critical-exclamation { animation: criticalExclamation 0.4s ease 0.6s forwards; }
                    .critical-dot { animation: criticalExclamation 0.4s ease 0.9s forwards; }
                </style>
                <polygon class="critical-octagon" points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2" opacity="0" />
                <line class="critical-exclamation" x1="12" y1="8" x2="12" y2="12" opacity="0" />
                <line class="critical-dot" x1="12" y1="16" x2="12.01" y2="16" opacity="0" />
            </svg>`,

            debug: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <style>
                    @keyframes debugShield {
                        0% { opacity: 0; clip-path: polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%, 50% 50%, 50% 50%); }
                        60% { opacity: 1; clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%); }
                        80% { transform: scale(1.1); }
                        100% { transform: scale(1); }
                    }
                    @keyframes debugLines {
                        0%, 40% { opacity: 0; stroke-dasharray: 0 100; }
                        100% { opacity: 1; stroke-dasharray: 100 100; }
                    }
                    .debug-shield { animation: debugShield 0.8s cubic-bezier(0.36, 0.66, 0.04, 1) forwards; }
                    .debug-lines { animation: debugLines 0.6s ease 0.8s forwards; }
                </style>
                <path class="debug-shield" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                <path class="debug-lines" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="none" opacity="0" stroke-dasharray="0 100" />
            </svg>`
        };

        // Create the inner HTML structure dynamically
        const iconContainer = document.createElement('div');
        iconContainer.style.display = 'flex';
        iconContainer.style.alignItems = 'center';
        iconContainer.style.justifyContent = 'center';
        iconContainer.style.width = '38px';
        iconContainer.style.height = '38px';
        iconContainer.style.borderRadius = '50%';
        iconContainer.style.backgroundColor = scheme.iconBg;
        iconContainer.style.color = '#ffffff';
        iconContainer.style.fontSize = '18px';
        iconContainer.style.fontWeight = 'bold';
        iconContainer.style.marginRight = direction === 'ltr' ? '15px' : '0';
        iconContainer.style.marginLeft = direction === 'rtl' ? '15px' : '0';
        iconContainer.style.flexShrink = '0';
        iconContainer.innerHTML = svgIcons[type] || svgIcons.info;

        // Special animation for waiting icon (rotating)
        if (type === 'waiting') {
            // Waiting already has animation built into SVG
            iconContainer.style.animation = 'none';
        } else {
            // Default pulse animation for other icons
            iconContainer.style.animation = 'pulse 2s infinite';
        }

        const contentContainer = document.createElement('div');
        contentContainer.style.flex = '1';
        contentContainer.style.marginRight = direction === 'ltr' ? '10px' : '0';
        contentContainer.style.marginLeft = direction === 'rtl' ? '10px' : '0';
        contentContainer.style.textAlign = direction === 'ltr' ? 'left' : 'right';

        if (title) {
            const titleElement = document.createElement('div');
            titleElement.style.fontSize = '16px';
            titleElement.style.fontWeight = 'bold';
            titleElement.style.marginBottom = '4px';
            titleElement.style.textAlign = 'inherit';
            titleElement.textContent = title;
            titleElement.setAttribute('data-alert-title', '');
            contentContainer.appendChild(titleElement);
        }

        const messageElement = document.createElement('div');
        messageElement.style.fontSize = '14px';
        messageElement.style.lineHeight = '1.4';
        messageElement.style.textAlign = 'inherit';
        messageElement.textContent = message;
        messageElement.setAttribute('data-alert-message', '');
        contentContainer.appendChild(messageElement);

        // Add countdown timer if requested
        let countdownElement = null;
        if (showCountdown && timeout > 0) {
            countdownElement = document.createElement('div');
            countdownElement.style.fontSize = '22px';         // Big and visible
            countdownElement.style.fontWeight = 'bold';
            countdownElement.style.textAlign = 'center';
            countdownElement.style.marginTop = '12px';
            countdownElement.style.opacity = '0.95';
            countdownElement.style.color = '#fff';             // White for contrast
            countdownElement.setAttribute('data-countdown-timer', '');
            contentContainer.appendChild(countdownElement);

            let remainingTime = Math.ceil(timeout / 1000);
            countdownElement.textContent = remainingTime;      // Initial display

            let countdownInterval = setInterval(() => {
                remainingTime -= 1;
                countdownElement.textContent = remainingTime > 0 ? remainingTime : '';
                if (remainingTime <= 0) {
                    clearInterval(countdownInterval);
                }
            }, 1000);
        }

        const closeButton = document.createElement('button');
        closeButton.style.background = 'none';
        closeButton.style.border = 'none';
        closeButton.style.fontSize = '22px';
        closeButton.style.fontWeight = 'bold';
        closeButton.style.cursor = 'pointer';
        closeButton.style.color = scheme.color;
        closeButton.style.opacity = '0.8';
        closeButton.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        closeButton.style.marginLeft = direction === 'ltr' ? '15px' : '0';
        closeButton.style.marginRight = direction === 'rtl' ? '15px' : '0';
        closeButton.style.padding = '8px'; // Larger padding for better touch targets
        closeButton.style.borderRadius = '50%'; // Makes it circular for better UX
        closeButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`;
        closeButton.setAttribute('aria-label', 'Close alert');

        // Hover effect for close button
        closeButton.onmouseover = function() {
            this.style.opacity = '1';
            this.style.transform = 'scale(1.1)';
        };
        closeButton.onmouseout = function() {
            this.style.opacity = '0.8';
            this.style.transform = 'scale(1)';
        };

        // Add progress bar if timeout is set
//        if (timeout > 0) {
//            const progressContainer = document.createElement('div');
//            progressContainer.style.position = 'absolute';
//            progressContainer.style.bottom = '0';
//            progressContainer.style.left = '0';
//            progressContainer.style.width = '100%';
//            progressContainer.style.height = '3px';
//            progressContainer.style.overflow = 'hidden';
//            progressContainer.style.borderBottomLeftRadius = '8px';
//            progressContainer.style.borderBottomRightRadius = '8px';
//
//            const progressBar = document.createElement('div');
//            progressBar.style.height = '100%';
//            progressBar.style.width = '100%';
//            progressBar.style.backgroundColor = scheme.progressColor;
//            progressBar.style.transition = `width ${timeout}ms linear`;
//            progressBar.setAttribute('data-progress-bar', '');
//
//            progressContainer.appendChild(progressBar);
//            alert.appendChild(progressContainer);
//
//            // Start the progress animation after a small delay
//            setTimeout(() => {
//                progressBar.style.width = '0%';
//            }, 10);
//        }

        // Append elements to the alert container
        alert.appendChild(iconContainer);
        alert.appendChild(contentContainer);
        alert.appendChild(closeButton);

        // Calculate the delay for staggered animation
        const delay = Math.min(currentAlerts.length * 100, 300);
        alert.style.transitionDelay = `${delay}ms`;

        // Add the alert to the container
        alertContainer.appendChild(alert);

        // Function to handle alert closing
        const closeAlert = function() {
            alert.style.opacity = '0';
            alert.style.transform = direction === 'ltr' ? 'translateX(100%)' : 'translateX(-100%)';
            alert.addEventListener('transitionend', function(e) {
                // Only remove if the transition was for opacity (not for progress bar)
                if (e.propertyName === 'opacity') {
                    alert.remove();
                }
            });
        };

        // Add custom event listener for closing
        alert.addEventListener('alertClose', closeAlert);

        // Animate the alert to make it appear
        requestAnimationFrame(() => {
            setTimeout(() => {
                alert.style.opacity = '1';
                alert.style.transform = 'translateX(0)';
            }, 10); // Small delay for the animation to work properly
        });

        // Add close button functionality
        closeButton.addEventListener('click', function() {
            closeAlert();
        });

        // Initialize countdown timer if enabled
        let countdownInterval = null;
        if (showCountdown && timeout > 0 && countdownElement) {
            let remainingTime = Math.ceil(timeout / 1000);
            countdownElement.textContent = `⏳ ${remainingTime}`;

            countdownInterval = setInterval(() => {
                remainingTime -= 1;
                countdownElement.textContent = remainingTime;
                if (remainingTime <= 0) {
                    clearInterval(countdownInterval);
                }
            }, 1000);

            // Initial value shown immediately
            countdownElement.textContent = remainingTime;
        }

        // Auto-remove the alert after the specified timeout
        if (timeout > 0) {
            setTimeout(() => {
                closeAlert();
                if (countdownInterval) {
                    clearInterval(countdownInterval);
                }
            }, timeout);
        }

        // Return a function that can be used to programmatically close this alert
        return function() {
            closeAlert();
            if (countdownInterval) {
                clearInterval(countdownInterval);
            }
        };
    };

    // Function to group similar alerts
    window.showGroupedAlert = function(type, message, title, timeout, direction, position, showCountdown = true) {
        const containerId = 'alert-container-' + position;
        const container = document.querySelector('#' + containerId);

        if (!container) {
            // If no container exists yet, just show a regular alert
            return window.showAlert(type, message, title, timeout, direction, position, showCountdown);
        }

        // Check for similar alerts
        const similarAlerts = Array.from(container.querySelectorAll('.custom-alert')).filter(alert => {
            const alertTitle = alert.querySelector('[data-alert-title]');
            const alertMessage = alert.querySelector('[data-alert-message]');

            return (alertTitle && alertTitle.textContent === title) ||
                   (alertMessage && alertMessage.textContent === message);
        });

        if (similarAlerts.length > 0) {
            // Update existing alert
            const existingAlert = similarAlerts[0];
            const counter = existingAlert.querySelector('[data-alert-counter]');

            if (counter) {
                // Increment counter
                const count = parseInt(counter.getAttribute('data-count')) + 1;
                counter.setAttribute('data-count', count);
                counter.textContent = `(${count})`;

                // Reset timeout if applicable
                if (timeout > 0) {
                    const progressBar = existingAlert.querySelector('[data-progress-bar]');
                    if (progressBar) {
                        progressBar.style.transition = 'none';
                        progressBar.style.width = '100%';

                        setTimeout(() => {
                            progressBar.style.transition = `width ${timeout}ms linear`;
                            progressBar.style.width = '0%';
                        }, 10);
                    }

                    // Clear existing timeout and set a new one
                    const timeoutId = parseInt(existingAlert.getAttribute('data-timeout-id'));
                    if (timeoutId) {
                        clearTimeout(timeoutId);
                    }

                    // Update countdown timer if it exists
                    const countdownElement = existingAlert.querySelector('[data-countdown-timer]');
                    if (countdownElement && showCountdown) {
                        const endTime = Date.now() + timeout;
                        const countdownIntervalId = parseInt(existingAlert.getAttribute('data-countdown-interval-id')) || 0;

                        if (countdownIntervalId) {
                            clearInterval(countdownIntervalId);
                        }

                        const newIntervalId = setInterval(() => {
                            const remainingTime = Math.max(0, Math.floor((endTime - Date.now()) / 1000));
                            countdownElement.textContent = `Closing in ${remainingTime} seconds`;

                            if (remainingTime <= 0) {
                                clearInterval(newIntervalId);
                            }
                        }, 1000);

                        existingAlert.setAttribute('data-countdown-interval-id', newIntervalId);
                        countdownElement.textContent = `Closing in ${Math.floor(timeout / 1000)} seconds`;
                    }

                    const newTimeoutId = setTimeout(() => {
                        existingAlert.dispatchEvent(new Event('alertClose'));
                        const intervalId = parseInt(existingAlert.getAttribute('data-countdown-interval-id')) || 0;
                        if (intervalId) {
                            clearInterval(intervalId);
                        }
                    }, timeout);

                    existingAlert.setAttribute('data-timeout-id', newTimeoutId);
                }

                // Flash effect to indicate update
                existingAlert.style.boxShadow = '0 0 0 3px rgba(255, 255, 255, 0.5)';
                setTimeout(() => {
                    existingAlert.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.15)';
                }, 300);

                return function() {
                    existingAlert.dispatchEvent(new Event('alertClose'));
                    const intervalId = parseInt(existingAlert.getAttribute('data-countdown-interval-id')) || 0;
                    if (intervalId) {
                        clearInterval(intervalId);
                    }
                };
            }

            return window.showAlert(type, message, title, timeout, direction, position, showCountdown);
        } else {
            // Show new alert with counter
            const alert = window.showAlert(type, message, title, timeout, direction, position, showCountdown);
            const alertElement = container.lastChild;

            // Add counter
            const counterElement = document.createElement('span');
            counterElement.setAttribute('data-alert-counter', '');
            counterElement.setAttribute('data-count', '1');
            counterElement.style.marginLeft = '8px';
            counterElement.style.fontSize = '14px';
            counterElement.style.opacity = '0.8';

            // Store timeout ID for later use
            if (timeout > 0) {
                const timeoutId = setTimeout(() => {
                    alertElement.dispatchEvent(new Event('alertClose'));
                    const intervalId = parseInt(alertElement.getAttribute('data-countdown-interval-id')) || 0;
                    if (intervalId) {
                        clearInterval(intervalId);
                    }
                }, timeout);

                alertElement.setAttribute('data-timeout-id', timeoutId);
            }

            return alert;
        }
    };

    // Set a flag that this has been loaded
    window.alertSystemLoaded = true;
    return true;
}
