(function() {
    'use strict';
    
    // Store original console methods
    const originalLog = console.log;
    const originalWarn = console.warn;
    const originalError = console.error;
    
    // Get the script tag to find the server URL
    const scriptTag = document.currentScript || (function() {
        const scripts = document.getElementsByTagName('script');
        for (let i = scripts.length - 1; i >= 0; i--) {
            if (scripts[i].src.includes('console-quill.js')) {
                return scripts[i];
            }
        }
        return null;
    })();
    
    // Extract server URL from script src
    let serverUrl = 'http://localhost:9876';
    if (scriptTag && scriptTag.src) {
        try {
            const url = new URL(scriptTag.src);
            serverUrl = `${url.protocol}//${url.host}`;
        } catch (e) {
            console.warn('Could not parse console-quill.js URL, using default server URL');
        }
    }
    
    // Function to send log data to server
    function sendToServer(level, args) {
        const message = args.map(arg => {
            if (typeof arg === 'object') {
                try {
                    return JSON.stringify(arg);
                } catch (e) {
                    return String(arg);
                }
            }
            return String(arg);
        }).join(' ');
        
        const logData = {
            level: level,
            message: message,
            timestamp: new Date().toISOString()
        };
        
        // Send to server (fire and forget)
        fetch(`${serverUrl}/log`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(logData)
        }).catch(err => {
            // Silently ignore network errors to avoid infinite loops
        });
    }
    
    // Override console.log
    console.log = function(...args) {
        originalLog.apply(console, args);
        sendToServer('log', args);
    };
    
    // Override console.warn
    console.warn = function(...args) {
        originalWarn.apply(console, args);
        sendToServer('warn', args);
    };
    
    // Override console.error
    console.error = function(...args) {
        originalError.apply(console, args);
        sendToServer('error', args);
    };
    
    // Initialize message
    console.log('Console Quill initialized - console messages will be logged to server');
    
})();