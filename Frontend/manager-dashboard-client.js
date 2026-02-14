/**
 * Manager Dashboard Client
 * Displays realtime employee locations on a map
 * Compatible with Flask-SocketIO and eventlet backend
 */

class ManagerDashboardClient {
    constructor(config = {}) {
        this.config = {
            socketUrl: config.socketUrl || 'http://localhost:5001',
            mapElementId: config.mapElementId || 'map',
            ...config
        };
        
        this.socket = null;
        this.managerId = null;
        this.employees = new Map(); // employee_id -> employee data
        this.markers = new Map(); // employee_id -> map marker
        this.map = null;
        
        // Callbacks
        this.onEmployeeUpdate = config.onEmployeeUpdate || (() => {});
        this.onError = config.onError || ((error) => console.error(error));
        this.onConnected = config.onConnected || (() => {});
    }
    
    /**
     * Initialize socket connection and map
     */
    connect(managerId) {
        this.managerId = managerId;
        
        // Load Socket.IO from CDN if not already loaded
        if (typeof io === 'undefined') {
            const script = document.createElement('script');
            script.src = 'https://cdn.socket.io/4.5.4/socket.io.min.js';
            script.onload = () => this._initSocket();
            document.head.appendChild(script);
        } else {
            this._initSocket();
        }
        
        // Initialize map (using Leaflet as example)
        this._initMap();
    }
    
    _initSocket() {
        this.socket = io(this.config.socketUrl, {
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionAttempts: 5
        });
        
        this.socket.on('connect', () => {
            console.log('✅ Manager socket connected');
            this.socket.emit('manager:join', { manager_id: this.managerId });
        });
        
        this.socket.on('manager:joined', (data) => {
            console.log('✅ Joined managers room:', data);
            
            // Load initial active employees
            if (data.active_employees) {
                data.active_employees.forEach(emp => {
                    this._updateEmployee(emp);
                });
            }
            
            this.onConnected(data);
        });
        
        this.socket.on('employee:location', (data) => {
            console.log('📍 Employee location update:', data);
            this._updateEmployee(data);
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
     * Initialize map (using Leaflet.js)
     */
    _initMap() {
        // Load Leaflet if not already loaded
        if (typeof L === 'undefined') {
            // Load CSS
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
            document.head.appendChild(link);
            
            // Load JS
            const script = document.createElement('script');
            script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
            script.onload = () => this._createMap();
            document.head.appendChild(script);
        } else {
            this._createMap();
        }
    }
    
    _createMap() {
        // Center on office location (adjust coordinates)
        const officeLocation = [11.5564, 104.9282]; // Phnom Penh example
        
        this.map = L.map(this.config.mapElementId).setView(officeLocation, 15);
        
        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);
        
        // Add office marker
        L.marker(officeLocation, {
            icon: L.divIcon({
                className: 'office-marker',
                html: '<div style="background: #4CAF50; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>',
                iconSize: [30, 30]
            })
        }).addTo(this.map).bindPopup('<b>Office</b>');
        
        // Add geofence circle (150m radius)
        L.circle(officeLocation, {
            color: '#4CAF50',
            fillColor: '#4CAF50',
            fillOpacity: 0.1,
            radius: 150
        }).addTo(this.map);
    }
    
    /**
     * Update employee location on map
     */
    _updateEmployee(data) {
        const employeeId = data.employee_id;
        
        // Update employee data
        this.employees.set(employeeId, data);
        
        // Update or create marker
        if (this.markers.has(employeeId)) {
            // Update existing marker
            const marker = this.markers.get(employeeId);
            marker.setLatLng([data.lat, data.lng]);
            
            // Update popup
            marker.setPopupContent(this._createPopupContent(data));
            
            // Update marker style based on status
            if (data.status === 'inactive') {
                marker.setOpacity(0.5);
            } else {
                marker.setOpacity(1.0);
            }
        } else {
            // Create new marker
            const marker = L.marker([data.lat, data.lng], {
                icon: this._createEmployeeIcon(data)
            }).addTo(this.map);
            
            marker.bindPopup(this._createPopupContent(data));
            this.markers.set(employeeId, marker);
        }
        
        // Remove marker if inactive
        if (data.status === 'inactive') {
            setTimeout(() => {
                const marker = this.markers.get(employeeId);
                if (marker && this.employees.get(employeeId)?.status === 'inactive') {
                    this.map.removeLayer(marker);
                    this.markers.delete(employeeId);
                    this.employees.delete(employeeId);
                }
            }, 30000); // Remove after 30 seconds
        }
        
        // Callback
        this.onEmployeeUpdate(data);
    }
    
    /**
     * Create custom employee marker icon
     */
    _createEmployeeIcon(data) {
        const color = data.status === 'active' ? '#2196F3' : '#9E9E9E';
        
        return L.divIcon({
            className: 'employee-marker',
            html: `
                <div style="position: relative;">
                    <div style="
                        background: ${color};
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        border: 3px solid white;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-weight: bold;
                        font-size: 14px;
                    ">
                        ${(data.employee_name || 'E').charAt(0).toUpperCase()}
                    </div>
                    ${data.status === 'active' ? '<div style="position: absolute; top: 0; right: 0; width: 12px; height: 12px; background: #4CAF50; border: 2px solid white; border-radius: 50%;"></div>' : ''}
                </div>
            `,
            iconSize: [40, 40],
            iconAnchor: [20, 40]
        });
    }
    
    /**
     * Create popup content for employee marker
     */
    _createPopupContent(data) {
        const lastSeen = data.last_seen_at ? new Date(data.last_seen_at).toLocaleTimeString() : 'Unknown';
        const shiftStarted = data.shift_started_at ? new Date(data.shift_started_at).toLocaleTimeString() : 'N/A';
        
        return `
            <div style="min-width: 200px;">
                <h3 style="margin: 0 0 10px 0;">${data.employee_name || 'Unknown'}</h3>
                ${data.photo_url ? `<img src="${data.photo_url}" style="width: 100%; max-width: 200px; border-radius: 8px; margin-bottom: 10px;">` : ''}
                <p style="margin: 5px 0;"><strong>Code:</strong> ${data.employee_code || 'N/A'}</p>
                <p style="margin: 5px 0;"><strong>Department:</strong> ${data.department || 'N/A'}</p>
                <p style="margin: 5px 0;"><strong>Position:</strong> ${data.position || 'N/A'}</p>
                <p style="margin: 5px 0;"><strong>Status:</strong> <span style="color: ${data.status === 'active' ? '#4CAF50' : '#9E9E9E'};">${data.status}</span></p>
                <p style="margin: 5px 0;"><strong>Shift Started:</strong> ${shiftStarted}</p>
                <p style="margin: 5px 0;"><strong>Last Seen:</strong> ${lastSeen}</p>
                <p style="margin: 5px 0;"><strong>Accuracy:</strong> ${data.accuracy?.toFixed(0)}m</p>
                <p style="margin: 5px 0;"><strong>Distance from Office:</strong> ${data.distance_from_office_m?.toFixed(0)}m</p>
            </div>
        `;
    }
    
    /**
     * Get all active employees
     */
    getActiveEmployees() {
        return Array.from(this.employees.values()).filter(emp => emp.status === 'active');
    }
    
    /**
     * Focus map on specific employee
     */
    focusEmployee(employeeId) {
        const employee = this.employees.get(employeeId);
        if (employee && this.markers.has(employeeId)) {
            this.map.setView([employee.lat, employee.lng], 17);
            this.markers.get(employeeId).openPopup();
        }
    }
    
    /**
     * Disconnect socket
     */
    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
        }
    }
}

// ============================================================================
// USAGE EXAMPLE
// ============================================================================

/*
// HTML
<div id="manager-dashboard">
    <div id="map" style="height: 600px; width: 100%;"></div>
    <div id="employee-list"></div>
</div>

// JavaScript
const dashboard = new ManagerDashboardClient({
    socketUrl: 'http://localhost:5001',
    mapElementId: 'map',
    
    onConnected: (data) => {
        console.log('Dashboard connected:', data);
        updateEmployeeList();
    },
    
    onEmployeeUpdate: (employee) => {
        console.log('Employee updated:', employee);
        updateEmployeeList();
    },
    
    onError: (error) => {
        alert(`Error: ${error.message}`);
    }
});

// Connect with manager ID
const managerId = 'YOUR_MANAGER_ID';
dashboard.connect(managerId);

// Update employee list
function updateEmployeeList() {
    const employees = dashboard.getActiveEmployees();
    const listEl = document.getElementById('employee-list');
    
    listEl.innerHTML = '<h3>Active Employees (' + employees.length + ')</h3>';
    
    employees.forEach(emp => {
        const div = document.createElement('div');
        div.style.cssText = 'padding: 10px; margin: 5px; border: 1px solid #ddd; cursor: pointer;';
        div.innerHTML = `
            <strong>${emp.employee_name}</strong> (${emp.employee_code})<br>
            <small>Last seen: ${new Date(emp.last_seen_at).toLocaleTimeString()}</small>
        `;
        div.onclick = () => dashboard.focusEmployee(emp.employee_id);
        listEl.appendChild(div);
    });
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    dashboard.disconnect();
});
*/
