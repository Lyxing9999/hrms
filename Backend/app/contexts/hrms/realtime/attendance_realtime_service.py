# app/contexts/hrms/realtime/attendance_realtime_service.py
"""
Service for handling realtime attendance operations including location tracking,
geofencing validation, and shift management.
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pymongo.database import Database
from bson import ObjectId
import math


class AttendanceRealtimeService:
    """
    Handles realtime attendance operations with GPS validation and geofencing.
    """
    
    # Geofence configuration (can be moved to settings/database)
    OFFICE_LAT = 11.5564  # Example: Phnom Penh coordinates
    OFFICE_LNG = 104.9282
    GEOFENCE_RADIUS_M = 150  # 150 meters radius
    MAX_ACCURACY_M = 200  # Reject if GPS accuracy > 200m
    
    def __init__(self, db: Database):
        self.db = db
        self.attendance_events = db["attendance_events"]
        self.live_locations = db["live_locations"]
        self.employees = db["employees"]
    
    @staticmethod
    def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula.
        Returns distance in meters.
        """
        R = 6371000  # Earth radius in meters
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_phi / 2) ** 2 +
             math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def validate_location(self, lat: float, lng: float, accuracy: float) -> Dict[str, any]:
        """
        Validate GPS location against accuracy and geofence requirements.
        Returns: {"valid": bool, "error": str or None, "distance_m": float}
        """
        # Check accuracy
        if accuracy > self.MAX_ACCURACY_M:
            return {
                "valid": False,
                "error": f"GPS accuracy too low ({accuracy:.0f}m). Please wait for better signal (required: <{self.MAX_ACCURACY_M}m)",
                "distance_m": None
            }
        
        # Check geofence
        distance = self.haversine_distance(lat, lng, self.OFFICE_LAT, self.OFFICE_LNG)
        
        if distance > self.GEOFENCE_RADIUS_M:
            return {
                "valid": False,
                "error": f"You are {distance:.0f}m from office. Please be within {self.GEOFENCE_RADIUS_M}m to check in",
                "distance_m": distance
            }
        
        return {
            "valid": True,
            "error": None,
            "distance_m": distance
        }
    
    def start_shift(
        self,
        employee_id: str,
        lat: float,
        lng: float,
        accuracy: float,
        photo_url: str,
        started_at: str
    ) -> Dict[str, any]:
        """
        Start employee shift with location and photo validation.
        """
        try:
            # Validate location
            validation = self.validate_location(lat, lng, accuracy)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"]}
            
            # Verify employee exists and get photo
            employee = self.employees.find_one({
                "_id": ObjectId(employee_id),
                "lifecycle.deleted_at": None
            })
            if not employee:
                return {"success": False, "error": "Employee not found"}
            
            # Use employee photo from database if available, otherwise use uploaded photo
            employee_photo = employee.get("photo_url") or photo_url
            
            # Check if already active
            existing = self.live_locations.find_one({"employee_id": employee_id, "status": "active"})
            if existing:
                return {"success": False, "error": "Shift already active. Please stop current shift first"}
            
            now = datetime.now(timezone.utc)
            started_dt = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
            
            # Store attendance event
            event_doc = {
                "employee_id": employee_id,
                "type": "shift_start",
                "lat": lat,
                "lng": lng,
                "accuracy": accuracy,
                "distance_from_office_m": validation["distance_m"],
                "photo_url": employee_photo,
                "created_at": started_dt,
                "metadata": {
                    "employee_name": employee.get("full_name"),
                    "employee_code": employee.get("employee_code")
                }
            }
            self.attendance_events.insert_one(event_doc)
            
            # Update/create live location
            location_doc = {
                "employee_id": employee_id,
                "lat": lat,
                "lng": lng,
                "accuracy": accuracy,
                "distance_from_office_m": validation["distance_m"],
                "status": "active",
                "photo_url": employee_photo,
                "shift_started_at": started_dt,
                "last_seen_at": now,
                "updated_at": now,
                "metadata": {
                    "employee_name": employee.get("full_name"),
                    "employee_code": employee.get("employee_code"),
                    "department": employee.get("department"),
                    "position": employee.get("position")
                }
            }
            
            self.live_locations.update_one(
                {"employee_id": employee_id},
                {"$set": location_doc},
                upsert=True
            )
            
            return {"success": True, "distance_m": validation["distance_m"]}
            
        except Exception as e:
            return {"success": False, "error": f"Internal error: {str(e)}"}
    
    def update_location(
        self,
        employee_id: str,
        lat: float,
        lng: float,
        accuracy: float,
        ts: str
    ) -> Dict[str, any]:
        """
        Update employee location during active shift.
        """
        try:
            # Validate location
            validation = self.validate_location(lat, lng, accuracy)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"]}
            
            # Check if shift is active
            live_loc = self.live_locations.find_one({"employee_id": employee_id})
            if not live_loc:
                return {"success": False, "error": "No active shift found. Please start shift first"}
            
            if live_loc.get("status") != "active":
                return {"success": False, "error": "Shift is not active"}
            
            ts_dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            
            # Update live location
            self.live_locations.update_one(
                {"employee_id": employee_id},
                {
                    "$set": {
                        "lat": lat,
                        "lng": lng,
                        "accuracy": accuracy,
                        "distance_from_office_m": validation["distance_m"],
                        "last_seen_at": ts_dt,
                        "updated_at": datetime.now(timezone.utc)
                    }
                }
            )
            
            return {
                "success": True,
                "status": live_loc.get("status"),
                "photo_url": live_loc.get("photo_url"),
                "distance_m": validation["distance_m"]
            }
            
        except Exception as e:
            return {"success": False, "error": f"Internal error: {str(e)}"}
    
    def stop_shift(
        self,
        employee_id: str,
        lat: float,
        lng: float,
        accuracy: float,
        stopped_at: str
    ) -> Dict[str, any]:
        """
        Stop employee shift with final location.
        """
        try:
            # Validate location
            validation = self.validate_location(lat, lng, accuracy)
            if not validation["valid"]:
                return {"success": False, "error": validation["error"]}
            
            # Check if shift is active
            live_loc = self.live_locations.find_one({"employee_id": employee_id, "status": "active"})
            if not live_loc:
                return {"success": False, "error": "No active shift found"}
            
            stopped_dt = datetime.fromisoformat(stopped_at.replace('Z', '+00:00'))
            started_dt = live_loc.get("shift_started_at")
            
            # Calculate duration
            duration_minutes = 0
            if started_dt:
                duration = stopped_dt - started_dt
                duration_minutes = int(duration.total_seconds() / 60)
            
            # Store attendance event
            event_doc = {
                "employee_id": employee_id,
                "type": "shift_stop",
                "lat": lat,
                "lng": lng,
                "accuracy": accuracy,
                "distance_from_office_m": validation["distance_m"],
                "photo_url": live_loc.get("photo_url"),  # Use start photo
                "created_at": stopped_dt,
                "metadata": {
                    "employee_name": live_loc.get("metadata", {}).get("employee_name"),
                    "employee_code": live_loc.get("metadata", {}).get("employee_code"),
                    "duration_minutes": duration_minutes
                }
            }
            self.attendance_events.insert_one(event_doc)
            
            # Update live location to inactive
            self.live_locations.update_one(
                {"employee_id": employee_id},
                {
                    "$set": {
                        "lat": lat,
                        "lng": lng,
                        "accuracy": accuracy,
                        "distance_from_office_m": validation["distance_m"],
                        "status": "inactive",
                        "shift_stopped_at": stopped_dt,
                        "last_seen_at": stopped_dt,
                        "updated_at": datetime.now(timezone.utc)
                    }
                }
            )
            
            return {
                "success": True,
                "duration_minutes": duration_minutes,
                "photo_url": live_loc.get("photo_url"),
                "distance_m": validation["distance_m"]
            }
            
        except Exception as e:
            return {"success": False, "error": f"Internal error: {str(e)}"}
    
    def get_active_employees_locations(self) -> List[Dict]:
        """
        Get all active employees and their current locations for manager dashboard.
        """
        try:
            cursor = self.live_locations.find({"status": "active"})
            
            locations = []
            for doc in cursor:
                locations.append({
                    "employee_id": doc.get("employee_id"),
                    "employee_name": doc.get("metadata", {}).get("employee_name"),
                    "employee_code": doc.get("metadata", {}).get("employee_code"),
                    "department": doc.get("metadata", {}).get("department"),
                    "position": doc.get("metadata", {}).get("position"),
                    "lat": doc.get("lat"),
                    "lng": doc.get("lng"),
                    "accuracy": doc.get("accuracy"),
                    "distance_from_office_m": doc.get("distance_from_office_m"),
                    "status": doc.get("status"),
                    "photo_url": doc.get("photo_url"),
                    "shift_started_at": doc.get("shift_started_at").isoformat() if doc.get("shift_started_at") else None,
                    "last_seen_at": doc.get("last_seen_at").isoformat() if doc.get("last_seen_at") else None
                })
            
            return locations
            
        except Exception as e:
            return []
