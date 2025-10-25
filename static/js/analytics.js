// Analytics Tracking JavaScript
(function() {
    'use strict';
    
    // Configuration
    const ANALYTICS_ENDPOINT = '/analytics/track/';
    const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutes
    const HEARTBEAT_INTERVAL = 30 * 1000; // 30 seconds
    
    // State
    let sessionStartTime = Date.now();
    let pageStartTime = Date.now();
    let isActive = true;
    let heartbeatInterval;
    
    // Initialize analytics
    function init() {
        if (typeof window.analyticsInitialized !== 'undefined') {
            return; // Already initialized
        }
        
        window.analyticsInitialized = true;
        
        // Track page view
        trackPageView();
        
        // Set up event listeners
        setupEventListeners();
        
        // Start heartbeat
        startHeartbeat();
        
        // Track page unload
        window.addEventListener('beforeunload', trackPageUnload);
        
        // Track visibility change
        document.addEventListener('visibilitychange', handleVisibilityChange);
    }
    
    // Track page view
    function trackPageView() {
        const data = {
            url: window.location.href,
            path: window.location.pathname,
            title: document.title,
            referrer: document.referrer,
            screen_resolution: screen.width + 'x' + screen.height,
            viewport_size: window.innerWidth + 'x' + window.innerHeight,
            timestamp: new Date().toISOString()
        };
        
        sendData('page_view', data);
    }
    
    // Track page unload
    function trackPageUnload() {
        const timeSpent = Date.now() - pageStartTime;
        const data = {
            url: window.location.href,
            time_spent: timeSpent,
            timestamp: new Date().toISOString()
        };
        
        sendData('page_unload', data, true); // Synchronous
    }
    
    // Track custom events
    function trackEvent(eventName, eventValue = null, metadata = {}) {
        const data = {
            event_name: eventName,
            event_value: eventValue,
            url: window.location.href,
            metadata: metadata,
            timestamp: new Date().toISOString()
        };
        
        sendData('event', data);
    }
    
    // Track form submissions
    function trackFormSubmission(form) {
        const formData = new FormData(form);
        const data = {
            form_id: form.id || 'unnamed',
            form_action: form.action || window.location.href,
            form_method: form.method || 'GET',
            field_count: form.elements.length,
            timestamp: new Date().toISOString()
        };
        
        // Add form field names (without values for privacy)
        const fieldNames = Array.from(form.elements).map(el => el.name || el.id).filter(Boolean);
        data.field_names = fieldNames;
        
        sendData('form_submit', data);
    }
    
    // Track clicks
    function trackClick(element) {
        const data = {
            element_tag: element.tagName.toLowerCase(),
            element_id: element.id || null,
            element_class: element.className || null,
            element_text: element.textContent ? element.textContent.substring(0, 100) : null,
            url: window.location.href,
            timestamp: new Date().toISOString()
        };
        
        sendData('click', data);
    }
    
    // Track scroll depth
    function trackScrollDepth() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = Math.round((scrollTop / docHeight) * 100);
        
        // Track at 25%, 50%, 75%, 100%
        const milestones = [25, 50, 75, 100];
        const currentMilestone = milestones.find(m => scrollPercent >= m);
        
        if (currentMilestone && !window.scrollMilestones) {
            window.scrollMilestones = new Set();
        }
        
        if (currentMilestone && !window.scrollMilestones.has(currentMilestone)) {
            window.scrollMilestones.add(currentMilestone);
            trackEvent('scroll_depth', currentMilestone + '%');
        }
    }
    
    // Track outbound links
    function trackOutboundLink(link) {
        const data = {
            link_url: link.href,
            link_text: link.textContent ? link.textContent.substring(0, 100) : null,
            source_url: window.location.href,
            timestamp: new Date().toISOString()
        };
        
        sendData('outbound_click', data);
    }
    
    // Track file downloads
    function trackDownload(link) {
        const data = {
            file_url: link.href,
            file_name: link.download || link.href.split('/').pop(),
            file_type: link.href.split('.').pop(),
            source_url: window.location.href,
            timestamp: new Date().toISOString()
        };
        
        sendData('download', data);
    }
    
    // Set up event listeners
    function setupEventListeners() {
        // Form submissions
        document.addEventListener('submit', function(e) {
            trackFormSubmission(e.target);
        });
        
        // Clicks
        document.addEventListener('click', function(e) {
            const element = e.target;
            
            // Track general clicks
            trackClick(element);
            
            // Track outbound links
            if (element.tagName === 'A' && element.href) {
                const url = new URL(element.href, window.location.origin);
                if (url.origin !== window.location.origin) {
                    trackOutboundLink(element);
                }
            }
            
            // Track downloads
            if (element.tagName === 'A' && (element.download || isFileLink(element.href))) {
                trackDownload(element);
            }
        });
        
        // Scroll tracking
        let scrollTimeout;
        window.addEventListener('scroll', function() {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(trackScrollDepth, 100);
        });
        
        // Video tracking
        const videos = document.querySelectorAll('video');
        videos.forEach(video => {
            video.addEventListener('play', () => trackEvent('video_play', video.src));
            video.addEventListener('pause', () => trackEvent('video_pause', video.src));
            video.addEventListener('ended', () => trackEvent('video_ended', video.src));
        });
        
        // Button clicks
        document.addEventListener('click', function(e) {
            if (e.target.tagName === 'BUTTON' || e.target.classList.contains('btn')) {
                trackEvent('button_click', e.target.textContent || e.target.className);
            }
        });
    }
    
    // Check if link is a file
    function isFileLink(href) {
        const fileExtensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.mp4', '.mp3', '.jpg', '.png', '.gif'];
        return fileExtensions.some(ext => href.toLowerCase().includes(ext));
    }
    
    // Handle visibility change
    function handleVisibilityChange() {
        if (document.hidden) {
            isActive = false;
            clearInterval(heartbeatInterval);
        } else {
            isActive = true;
            startHeartbeat();
        }
    }
    
    // Start heartbeat
    function startHeartbeat() {
        clearInterval(heartbeatInterval);
        heartbeatInterval = setInterval(() => {
            if (isActive) {
                const data = {
                    url: window.location.href,
                    time_spent: Date.now() - pageStartTime,
                    session_time: Date.now() - sessionStartTime,
                    timestamp: new Date().toISOString()
                };
                
                sendData('heartbeat', data);
            }
        }, HEARTBEAT_INTERVAL);
    }
    
    // Send data to server
    function sendData(eventType, data, synchronous = false) {
        const payload = {
            event_type: eventType,
            data: data
        };
        
        if (synchronous) {
            // Use sendBeacon for synchronous requests
            if (navigator.sendBeacon) {
                navigator.sendBeacon(ANALYTICS_ENDPOINT, JSON.stringify(payload));
            } else {
                // Fallback to synchronous XMLHttpRequest
                const xhr = new XMLHttpRequest();
                xhr.open('POST', ANALYTICS_ENDPOINT, false);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.send(JSON.stringify(payload));
            }
        } else {
            // Use fetch for asynchronous requests
            fetch(ANALYTICS_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(payload)
            }).catch(error => {
                console.log('Analytics tracking error:', error);
            });
        }
    }
    
    // Get CSRF token
    function getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }
    
    // Public API
    window.Analytics = {
        track: trackEvent,
        trackPageView: trackPageView,
        trackForm: trackFormSubmission,
        trackClick: trackClick,
        trackScroll: trackScrollDepth,
        trackOutbound: trackOutboundLink,
        trackDownload: trackDownload
    };
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
