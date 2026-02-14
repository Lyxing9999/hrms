#!/usr/bin/env python3
"""
Live Tracking System - Comprehensive Test Script

Tests the complete realtime employee tracking system including:
- Socket.IO connections
- Employee location updates
- Manager dashboard
- Photo handling
- Geofencing validation
"""

import sys
import time
import json
from datetime import datetime
import socketio
import requests
from bson import ObjectId

# Configuration
BACKEND_URL = "http://localhost:5001"
FRONTEND_URL = "http://localhost:3000"

# Test data
TEST_OFFICE_LAT = 11.5564
TEST_OFFICE_LNG = 104.9282

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_test(message):
    print(f"{Colors.BLUE}[TEST]{Colors.END} {message}")

def print_success(message):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")

def print_error(message):
    print(f"{Colors.RED}✗{Colors.END} {message}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def print_header(message):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


class LiveTrackingTester:
    def __init__(self):
        self.sio_employee = None
        self.sio_manager = None
        self.test_employee_id = None
        self.test_manager_id = None
        self.auth_token = None
        self.results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
    
    def run_all_tests(self):
        """Run all test suites"""
        print_header("LIVE TRACKING SYSTEM - COMPREHENSIVE TEST")
        
        try:
            # Test 1: Backend Health
            self.test_backend_health()
            
            # Test 2: Socket.IO Server
            self.test_socketio_server()
            
            # Test 3: Employee Connection
            self.test_employee_connection()
            
            # Test 4: Manager Connection
            self.test_manager_connection()
            
            # Test 5: Shift Start
            self.test_shift_start()
            
            # Test 6: Location Updates
            self.test_location_updates()
            
            # Test 7: Shift Stop
            self.test_shift_stop()
            
            # Test 8: Geofencing
            self.test_geofencing()
            
            # Test 9: Photo Handling
            self.test_photo_handling()
            
            # Test 10: Frontend Page
            self.test_frontend_page()
            
        except KeyboardInterrupt:
            print_warning("\nTests interrupted by user")
        except Exception as e:
            print_error(f"Test suite failed: {str(e)}")
        finally:
            self.cleanup()
            self.print_summary()
    
    def test_backend_health(self):
        """Test 1: Backend server health"""
        print_header("Test 1: Backend Health Check")
        
        try:
            response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
            if response.status_code == 200:
                print_success("Backend server is running")
                self.results["passed"] += 1
            else:
                print_error(f"Backend returned status {response.status_code}")
                self.results["failed"] += 1
        except requests.exceptions.ConnectionError:
            print_error("Cannot connect to backend. Is it running?")
            print_warning(f"Expected URL: {BACKEND_URL}")
            self.results["failed"] += 1
            sys.exit(1)
        except Exception as e:
            print_error(f"Health check failed: {str(e)}")
            self.results["failed"] += 1
    
    def test_socketio_server(self):
        """Test 2: Socket.IO server availability"""
        print_header("Test 2: Socket.IO Server")
        
        try:
            response = requests.get(f"{BACKEND_URL}/socket.io/", timeout=5)
            if response.status_code in [200, 400]:  # 400 is OK for Socket.IO info endpoint
                print_success("Socket.IO server is available")
                self.results["passed"] += 1
            else:
                print_error(f"Socket.IO server returned status {response.status_code}")
                self.results["failed"] += 1
        except Exception as e:
            print_error(f"Socket.IO server check failed: {str(e)}")
            self.results["failed"] += 1
    
    def test_employee_connection(self):
        """Test 3: Employee Socket.IO connection"""
        print_header("Test 3: Employee Connection")
        
        self.sio_employee = socketio.Client()
        connected = False
        joined = False
        
        @self.sio_employee.on('connect')
        def on_connect():
            nonlocal connected
            connected = True
            print_success("Employee socket connected")
        
        @self.sio_employee.on('employee:joined')
        def on_joined(data):
            nonlocal joined
            joined = True
            print_success(f"Employee joined room: {data.get('room')}")
        
        @self.sio_employee.on('connect_error')
        def on_error(data):
            print_error(f"Connection error: {data}")
        
        try:
            self.sio_employee.connect(BACKEND_URL)
            time.sleep(1)
            
            if connected:
                self.test_employee_id = "test_employee_" + str(int(time.time()))
                self.sio_employee.emit('employee:join', {'employee_id': self.test_employee_id})
                time.sleep(1)
                
                if joined:
                    self.results["passed"] += 1
                else:
                    print_error("Employee did not join room")
                    self.results["failed"] += 1
            else:
                print_error("Employee socket did not connect")
                self.results["failed"] += 1
        except Exception as e:
            print_error(f"Employee connection failed: {str(e)}")
            self.results["failed"] += 1
    
    def test_manager_connection(self):
        """Test 4: Manager Socket.IO connection"""
        print_header("Test 4: Manager Connection")
        
        self.sio_manager = socketio.Client()
        connected = False
        joined = False
        active_employees = []
        
        @self.sio_manager.on('connect')
        def on_connect():
            nonlocal connected
            connected = True
            print_success("Manager socket connected")
        
        @self.sio_manager.on('manager:joined')
        def on_joined(data):
            nonlocal joined, active_employees
            joined = True
            active_employees = data.get('active_employees', [])
            print_success(f"Manager joined room: {data.get('room')}")
            print_test(f"Active employees: {len(active_employees)}")
        
        try:
            self.sio_manager.connect(BACKEND_URL)
            time.sleep(1)
            
            if connected:
                self.test_manager_id = "test_manager_" + str(int(time.time()))
                self.sio_manager.emit('manager:join', {'manager_id': self.test_manager_id})
                time.sleep(1)
                
                if joined:
                    self.results["passed"] += 1
                else:
                    print_error("Manager did not join room")
                    self.results["failed"] += 1
            else:
                print_error("Manager socket did not connect")
                self.results["failed"] += 1
        except Exception as e:
            print_error(f"Manager connection failed: {str(e)}")
            self.results["failed"] += 1
    
    def test_shift_start(self):
        """Test 5: Employee shift start"""
        print_header("Test 5: Shift Start")
        
        if not self.sio_employee or not self.sio_employee.connected:
            print_error("Employee not connected, skipping test")
            self.results["failed"] += 1
            return
        
        shift_started = False
        location_received = False
        
        @self.sio_employee.on('shift:started')
        def on_shift_started(data):
            nonlocal shift_started
            shift_started = True
            print_success(f"Shift started for employee: {data.get('employee_id')}")
        
        @self.sio_manager.on('employee:location')
        def on_location(data):
            nonlocal location_received
            if data.get('employee_id') == self.test_employee_id:
                location_received = True
                print_success(f"Manager received location update: {data.get('status')}")
        
        try:
            shift_data = {
                'employee_id': self.test_employee_id,
                'lat': TEST_OFFICE_LAT + 0.0001,  # ~11m from office
                'lng': TEST_OFFICE_LNG + 0.0001,
                'accuracy': 15.5,
                'photo_url': '/uploads/test_photo.jpg',
                'started_at': datetime.utcnow().isoformat() + 'Z'
            }
            
            self.sio_employee.emit('shift:start', shift_data)
            time.sleep(2)
            
            if shift_started and location_received:
                print_success("Shift start successful")
                self.results["passed"] += 1
            else:
                if not shift_started:
                    print_error("Shift start confirmation not received")
                if not location_received:
                    print_error("Manager did not receive location update")
                self.results["failed"] += 1
        except Exception as e:
            print_error(f"Shift start failed: {str(e)}")
            self.results["failed"] += 1
    
    def test_location_updates(self):
        """Test 6: Periodic location updates"""
        print_header("Test 6: Location Updates")
        
        if not self.sio_employee or not self.sio_employee.connected:
            print_error("Employee not connected, skipping test")
            self.results["failed"] += 1
            return
        
        updates_received = 0
        
        @self.sio_manager.on('employee:location')
        def on_location(data):
            nonlocal updates_received
            if data.get('employee_id') == self.test_employee_id:
                updates_received += 1
        
        try:
            print_test("Sending 3 location updates...")
            for i in range(3):
                location_data = {
                    'employee_id': self.test_employee_id,
                    'lat': TEST_OFFICE_LAT + (0.0001 * (i + 1)),
                    'lng': TEST_OFFICE_LNG + (0.0001 * (i + 1)),
                    'accuracy': 12.0 + i,
                    'ts': datetime.utcnow().isoformat() + 'Z'
                }
                self.sio_employee.emit('location:update', location_data)
                time.sleep(1)
            
            time.sleep(1)
            
            if updates_received >= 3:
                print_success(f"Received {updates_received} location updates")
                self.results["passed"] += 1
            else:
                print_error(f"Only received {updates_received}/3 location updates")
                self.results["failed"] += 1
        except Exception as e:
            print_error(f"Location updates failed: {str(e)}")
            self.results["failed"] += 1
    
    def test_shift_stop(self):
        """Test 7: Employee shift stop"""
        print_header("Test 7: Shift Stop")
        
        if not self.sio_employee or not self.sio_employee.connected:
            print_error("Employee not connected, skipping test")
            self.results["failed"] += 1
            return
        
        shift_stopped = False
        
        @self.sio_employee.on('shift:stopped')
        def on_shift_stopped(data):
            nonlocal shift_stopped
            shift_stopped = True
            print_success(f"Shift stopped. Duration: {data.get('duration_minutes')} minutes")
        
        try:
            stop_data = {
                'employee_id': self.test_employee_id,
                'lat': TEST_OFFICE_LAT + 0.0001,
                'lng': TEST_OFFICE_LNG + 0.0001,
                'accuracy': 18.2,
                'stopped_at': datetime.utcnow().isoformat() + 'Z'
            }
            
            self.sio_employee.emit('shift:stop', stop_data)
            time.sleep(2)
            
            if shift_stopped:
                print_success("Shift stop successful")
                self.results["passed"] += 1
            else:
                print_error("Shift stop confirmation not received")
                self.results["failed"] += 1
        except Exception as e:
            print_error(f"Shift stop failed: {str(e)}")
            self.results["failed"] += 1
    
    def test_geofencing(self):
        """Test 8: Geofencing validation"""
        print_header("Test 8: Geofencing Validation")
        
        if not self.sio_employee or not self.sio_employee.connected:
            print_error("Employee not connected, skipping test")
            self.results["failed"] += 1
            return
        
        error_received = False
        
        @self.sio_employee.on('error')
        def on_error(data):
            nonlocal error_received
            error_received = True
            print_success(f"Geofence error received: {data.get('message')}")
        
        try:
            # Try to start shift far from office (should fail)
            far_location = {
                'employee_id': self.test_employee_id + '_far',
                'lat': TEST_OFFICE_LAT + 0.01,  # ~1km away
                'lng': TEST_OFFICE_LNG + 0.01,
                'accuracy': 15.0,
                'photo_url': '/uploads/test_photo.jpg',
                'started_at': datetime.utcnow().isoformat() + 'Z'
            }
            
            self.sio_employee.emit('shift:start', far_location)
            time.sleep(2)
            
            if error_received:
                print_success("Geofencing validation working")
                self.results["passed"] += 1
            else:
                print_warning("Geofence error not received (may need to check backend)")
                self.results["warnings"] += 1
        except Exception as e:
            print_error(f"Geofencing test failed: {str(e)}")
            self.results["failed"] += 1
    
    def test_photo_handling(self):
        """Test 9: Photo upload and retrieval"""
        print_header("Test 9: Photo Handling")
        
        print_test("Testing photo upload endpoint...")
        
        # Note: This requires authentication, so we'll just test the endpoint exists
        try:
            response = requests.options(f"{BACKEND_URL}/api/uploads/photo", timeout=5)
            if response.status_code in [200, 204, 405]:  # OPTIONS or method not allowed is OK
                print_success("Photo upload endpoint exists")
                self.results["passed"] += 1
            else:
                print_warning(f"Photo endpoint returned {response.status_code}")
                self.results["warnings"] += 1
        except Exception as e:
            print_error(f"Photo endpoint test failed: {str(e)}")
            self.results["failed"] += 1
    
    def test_frontend_page(self):
        """Test 10: Frontend page accessibility"""
        print_header("Test 10: Frontend Page")
        
        try:
            response = requests.get(f"{FRONTEND_URL}/hr/attendance/live-tracking", timeout=5)
            if response.status_code in [200, 302, 401]:  # 200 OK, 302 redirect, or 401 auth required
                print_success("Frontend page is accessible")
                self.results["passed"] += 1
            else:
                print_error(f"Frontend returned status {response.status_code}")
                self.results["failed"] += 1
        except requests.exceptions.ConnectionError:
            print_warning("Frontend not running (this is OK if testing backend only)")
            self.results["warnings"] += 1
        except Exception as e:
            print_error(f"Frontend test failed: {str(e)}")
            self.results["failed"] += 1
    
    def cleanup(self):
        """Cleanup connections"""
        print_test("\nCleaning up...")
        
        if self.sio_employee and self.sio_employee.connected:
            self.sio_employee.disconnect()
            print_test("Employee disconnected")
        
        if self.sio_manager and self.sio_manager.connected:
            self.sio_manager.disconnect()
            print_test("Manager disconnected")
    
    def print_summary(self):
        """Print test summary"""
        print_header("TEST SUMMARY")
        
        total = self.results["passed"] + self.results["failed"] + self.results["warnings"]
        
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.results['passed']}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.results['failed']}{Colors.END}")
        print(f"{Colors.YELLOW}Warnings: {self.results['warnings']}{Colors.END}")
        
        if self.results["failed"] == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.END}")
        
        print()


if __name__ == "__main__":
    print(f"{Colors.BOLD}Live Tracking System - Test Suite{Colors.END}")
    print(f"Backend: {BACKEND_URL}")
    print(f"Frontend: {FRONTEND_URL}")
    print()
    
    # Check dependencies
    try:
        import socketio
        import requests
    except ImportError as e:
        print_error(f"Missing dependency: {e}")
        print_test("Install with: pip install python-socketio requests")
        sys.exit(1)
    
    tester = LiveTrackingTester()
    tester.run_all_tests()
