/**
 * Realtime Attendance Client
 * Handles employee shift tracking with GPS location and photo capture
 * Compatible with Flask-SocketIO and eventlet backend
 */

class RealtimeAttendanceClient {
    constructor(config = {}) {
        this.config = {
            socketUrl: config.socketUrl || 'http://localhost:5001',
            apiUrl: config.apiUrl || 'http://localhost:5001',
            updateInterval: config.updateInterval || 5000, // 5 seconds
            ...config
        };
        
        this.socket = null;
        this.watchId = null;
        this.updateTimer = null;
        this.isShiftActive = false;
        this.employeeId = null;
        this.currentLocation = null;
        this.photoUrl = null;
        
        // Callbacks
        this.onShiftStarted = config.onShiftStarted || (() => {});
        this.onShiftStopped = config.onShiftStopped || (() => {});
        this.onLocationUpdate = config.onLocationUpdate || (() => {});
        this.onError = config.onError || ((error) => console.error(error));
        this.onConnected = config.onConnected || (() => {});
    }
    
    /**
     * Initialize socket connection
     */
    connect(employeeId) {
        this.employeeId = employeeId;
        
        // Load Socket.IO from CDN if not already loaded
        if (typeof io === 'undefined') {
            const script = document.createElement('script');
            script.src = 'https://cdn.socket.io/4.5.4/socket.io.min.js';
            script.onload = () => this._initSocket();
            document.head.appendChild(script);
        } else {
            this._initSocket();
        }
    }
    
    _initSocket() {
        this.socket = io(this.config.socketUrl, {
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionAttempts: 5
        });
        
        this.socket.on('connect', () => {
            console.log('✅ Socket connected');
            this.socket.emit('employee:join', { employee_id: this.employeeId });
        });
        
        this.socket.on('employee:joined', (data) => {
            console.log('✅ Joined employee room:', data);
            this.onConnected(data);
        });
        
        this.socket.on('shift:started', (data) => {
            console.log('✅ Shift started:', data);
            this.isShiftActive = true;
            this.onShiftStarted(data);
        });
        
        this.socket.on('shift:stopped', (data) => {
            console.log('✅ Shift stopped:', data);
            this.isShiftActive = false;
            this.onShiftStopped(data);
        });
        
        this.socket.on('error', (error) => {
            console.error('❌ Socket error:', error);
            this.onError(error);
        });
        
        this.socket.on('disconnect', () => {
            console.log('⚠️ Socket disconnected');
        });
    }
    
    /**
     * Capture photo from camera or file input
     */
    async capturePhoto(inputElement) {
        return new Promise((resolve, reject) => {
            if (inputElement.files && inputElement.files[0]) {
                const file = inputElement.files[0];
                
                // Validate file type
                if (!file.type.match('image.*')) {
                    reject(new Error('Please select an image file'));
                    return;
                }
                
                // Validate file size (5MB max)
                if (file.size > 5 * 1024 * 1024) {
                    reject(new Error('Image too large. Maximum size: 5MB'));
                    return;
                }
                
                resolve(file);
            } else {
                reject(new Error('No file selected'));
            }
        });
    }
    
    /**
     * Upload photo to backend
     */
    async uploadPhoto(file) {
        const formData = new FormData();
        formData.append('photo', file);
        formData.append('employee_id', this.employeeId);
        
        try {
            const response = await fetch(`${this.config.apiUrl}/api/uploads/photo`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.getAuthToken()}`
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Upload failed');
            }
            
            return data.photo_url;
        } catch (error) {
            throw new Error(`Photo upload failed: ${error.message}`);
        }
    }
    
    /**
     * Get current GPS location
     */
    async getCurrentLocation() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Geolocation not supported by your browser'));
                return;
            }
            
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    });
                },
                (error) => {
                    let message = 'Unable to get location';
                    switch (error.code) {
                        case error.PERMISSION_DENIED:
                            message = 'Location permission denied. Please enable location access.';
                            break;
                        case error.POSITION_UNAVAILABLE:
                            message = 'Location unavailable. Please try again.';
                            break;
                        case error.TIMEOUT:
                            message = 'Location request timed out. Please try again.';
                            break;
                    }
                    reject(new Error(message));
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        });
    }
    
    /**
     * Start shift with photo and location
     */
    async startShift(photoInputElement) {
        try {
            // 1. Capture photo
            const photoFile = await this.capturePhoto(photoInputElement);
            
            // 2. Get location
            const location = await this.getCurrentLocation();
            this.currentLocation = location;
            
            // 3. Upload photo
            this.photoUrl = await this.uploadPhoto(photoFile);
            
            // 4. Emit shift start event
            this.socket.emit('shift:start', {
                employee_id: this.employeeId,
                lat: location.lat,
                lng: location.lng,
                accuracy: location.accuracy,
                photo_url: this.photoUrl,
                started_at: new Date().toISOString()
            });
            
            // 5. Start watching location
            this._startLocationTracking();
            
        } catch (error) {
            this.onError(error);
            throw error;
        }
    }
    
    /**
     * Start continuous location tracking
     */
    _startLocationTracking() {
        if (!navigator.geolocation) {
            this.onError(new Error('Geolocation not supported'));
            return;
        }
        
        // Use watchPosition for continuous updates
        this.watchId = navigator.geolocation.watchPosition(
            (position) => {
                this.currentLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                    accuracy: position.coords.accuracy
                };
            },
            (error) => {
                console.error('Location watch error:', error);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
        
        // Send updates every 5 seconds
        this.updateTimer = setInterval(() => {
            if (this.isShiftActive && this.currentLocation) {
                this.socket.emit('location:update', {
                    employee_id: this.employeeId,
                    lat: this.currentLocation.lat,
                    lng: this.currentLocation.lng,
                    accuracy: this.currentLocation.accuracy,
                    ts: new Date().toISOString()
                });
                
                this.onLocationUpdate(this.currentLocation);
            }
        }, this.config.updateInterval);
    }
    
    /**
     * Stop shift
     */
    async stopShift() {
        try {
            // Get final location
            const location = await this.getCurrentLocation();
            
            // Emit shift stop event
            this.socket.emit('shift:stop', {
                employee_id: this.employeeId,
                lat: location.lat,
                lng: location.lng,
                accuracy: location.accuracy,
                stopped_at: new Date().toISOString()
            });
            
            // Stop location tracking
            this._stopLocationTracking();
            
        } catch (error) {
            this.onError(error);
            throw error;
        }
    }
    
    /**
     * Stop location tracking
     */
    _stopLocationTracking() {
        if (this.watchId) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
        }
        
        if (this.updateTimer) {
            clearInterval(this.updateTimer);
            this.updateTimer = null;
        }
    }
    
    /**
     * Disconnect socket
     */
    disconnect() {
        this._stopLocationTracking();
        if (this.socket) {
            this.socket.disconnect();
        }
    }
    
    /**
     * Get auth token from localStorage or cookie
     */
    getAuthToken() {
        // Adjust based on your auth implementation
        return localStorage.getItem('auth_token') || '';
    }
}

// ============================================================================
// USAGE EXAMPLE
// ============================================================================

/*
// HTML
<div id="attendance-app">
    <input type="file" id="photo-input" accept="image/*" capture="user">
    <button id="start-shift-btn">Start Shift</button>
    <button id="stop-shift-btn" disabled>Stop Shift</button>
    <div id="status"></div>
    <div id="location"></div>
</div>

// JavaScript
const client = new RealtimeAttendanceClient({
    socketUrl: 'http://localhost:5001',
    apiUrl: 'http://localhost:5001',
    updateInterval: 5000,
    
    onConnected: (data) => {
        document.getElementById('status').textContent = 'Connected';
    },
    
    onShiftStarted: (data) => {
        document.getElementById('status').textContent = 'Shift Active';
        document.getElementById('start-shift-btn').disabled = true;
        document.getElementById('stop-shift-btn').disabled = false;
    },
    
    onShiftStopped: (data) => {
        document.getElementById('status').textContent = 
            `Shift Ended (${data.duration_minutes} minutes)`;
        document.getElementById('start-shift-btn').disabled = false;
        document.getElementById('stop-shift-btn').disabled = true;
    },
    
    onLocationUpdate: (location) => {
        document.getElementById('location').textContent = 
            `Lat: ${location.lat.toFixed(6)}, Lng: ${location.lng.toFixed(6)}, Accuracy: ${location.accuracy.toFixed(0)}m`;
    },
    
    onError: (error) => {
        alert(`Error: ${error.message}`);
    }
});

// Connect with employee ID
const employeeId = 'YOUR_EMPLOYEE_ID';
client.connect(employeeId);

// Start shift button
document.getElementById('start-shift-btn').addEventListener('click', async () => {
    const photoInput = document.getElementById('photo-input');
    
    if (!photoInput.files || !photoInput.files[0]) {
        alert('Please select a photo first');
        return;
    }
    
    try {
        await client.startShift(photoInput);
    } catch (error) {
        console.error('Failed to start shift:', error);
    }
});

// Stop shift button
document.getElementById('stop-shift-btn').addEventListener('click', async () => {
    try {
        await client.stopShift();
    } catch (error) {
        console.error('Failed to stop shift:', error);
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    client.disconnect();
});
*/
