# app/contexts/hrms/realtime/handlers.py
"""
Realtime attendance handlers for employee location tracking and shift management.
Uses Flask-SocketIO with eventlet async_mode.
"""
from flask import request
from flask_socketio import join_room, leave_room, emit
from datetime import datetime
from typing import Optional

from app.contexts.infra.realtime.socketio_ext import socketio
from app.contexts.infra.database.mongodb import get_db
from app.contexts.hrms.realtime.attendance_realtime_service import AttendanceRealtimeService


# ============================================================================
# ROOM DESIGN DECISION:
# - Employees join: room="employee:<employee_id>" (their own room)
# - Managers join: room="managers" (single shared room for all managers)
#
# WHY "managers" (single room) instead of "manager:<manager_id>":
# 1. Simpler broadcasting: emit once to "managers" vs. iterating all manager IDs
# 2. Scalability: No need to track which managers are online
# 3. Frontend filtering: Managers can filter employees by team on client side
# 4. Reduced complexity: No need to maintain manager-employee relationships in realtime
# 5. Consistent with notification patterns: broadcast to role-based rooms
# ============================================================================


@socketio.on("employee:join", namespace="/")
def handle_employee_join(data: dict):
    """
    Employee joins their personal room for receiving notifications.
    Payload: { employee_id: str }
    """
    try:
        employee_id = data.get("employee_id")
        if not employee_id:
            emit("error", {"message": "employee_id is required"})
            return

        room = f"employee:{employee_id}"
        join_room(room)
        
        emit("employee:joined", {
            "employee_id": employee_id,
            "room": room,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        emit("error", {"message": f"Failed to join employee room: {str(e)}"})


@socketio.on("manager:join", namespace="/")
def handle_manager_join(data: dict):
    """
    Manager joins the shared managers room to receive all employee location updates.
    Payload: { manager_id: str }
    """
    try:
        manager_id = data.get("manager_id")
        if not manager_id:
            emit("error", {"message": "manager_id is required"})
            return

        # Join shared managers room
        join_room("managers")
        
        # Also join their personal room for notifications
        personal_room = f"manager:{manager_id}"
        join_room(personal_room)
        
        # Get current active employees and their locations
        db = get_db()
        service = AttendanceRealtimeService(db)
        active_employees = service.get_active_employees_locations()
        
        emit("manager:joined", {
            "manager_id": manager_id,
            "room": "managers",
            "active_employees": active_employees,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        emit("error", {"message": f"Failed to join manager room: {str(e)}"})


@socketio.on("shift:start", namespace="/")
def handle_shift_start(data: dict):
    """
    Employee starts their shift with initial location and photo.
    Payload: {
        employee_id: str,
        lat: float,
        lng: float,
        accuracy: float,
        photo_url: str,
        started_at: str (ISO format)
    }
    """
    try:
        # Validate required fields
        required = ["employee_id", "lat", "lng", "accuracy", "photo_url", "started_at"]
        missing = [f for f in required if f not in data]
        if missing:
            emit("error", {"message": f"Missing required fields: {', '.join(missing)}"})
            return

        employee_id = data["employee_id"]
        lat = float(data["lat"])
        lng = float(data["lng"])
        accuracy = float(data["accuracy"])
        photo_url = data["photo_url"]
        started_at = data["started_at"]

        db = get_db()
        service = AttendanceRealtimeService(db)
        
        # Process shift start (includes validation and storage)
        result = service.start_shift(
            employee_id=employee_id,
            lat=lat,
            lng=lng,
            accuracy=accuracy,
            photo_url=photo_url,
            started_at=started_at
        )
        
        if not result["success"]:
            emit("error", {"message": result["error"]})
            return
        
        # Confirm to employee
        emit("shift:started", {
            "employee_id": employee_id,
            "started_at": started_at,
            "location": {"lat": lat, "lng": lng, "accuracy": accuracy}
        }, room=f"employee:{employee_id}")
        
        # Broadcast to managers
        socketio.emit("employee:location", {
            "employee_id": employee_id,
            "lat": lat,
            "lng": lng,
            "accuracy": accuracy,
            "status": "active",
            "photo_url": photo_url,
            "last_seen_at": datetime.utcnow().isoformat()
        }, room="managers", namespace="/")
        
    except ValueError as e:
        emit("error", {"message": f"Invalid data format: {str(e)}"})
    except Exception as e:
        emit("error", {"message": f"Failed to start shift: {str(e)}"})


@socketio.on("location:update", namespace="/")
def handle_location_update(data: dict):
    """
    Employee sends periodic location updates during active shift.
    Payload: {
        employee_id: str,
        lat: float,
        lng: float,
        accuracy: float,
        ts: str (ISO format timestamp)
    }
    """
    try:
        # Validate required fields
        required = ["employee_id", "lat", "lng", "accuracy", "ts"]
        missing = [f for f in required if f not in data]
        if missing:
            emit("error", {"message": f"Missing required fields: {', '.join(missing)}"})
            return

        employee_id = data["employee_id"]
        lat = float(data["lat"])
        lng = float(data["lng"])
        accuracy = float(data["accuracy"])
        ts = data["ts"]

        db = get_db()
        service = AttendanceRealtimeService(db)
        
        # Update location (includes validation)
        result = service.update_location(
            employee_id=employee_id,
            lat=lat,
            lng=lng,
            accuracy=accuracy,
            ts=ts
        )
        
        if not result["success"]:
            emit("error", {"message": result["error"]})
            return
        
        # Broadcast to managers (no confirmation to employee to reduce traffic)
        socketio.emit("employee:location", {
            "employee_id": employee_id,
            "lat": lat,
            "lng": lng,
            "accuracy": accuracy,
            "status": result["status"],
            "photo_url": result.get("photo_url"),
            "last_seen_at": ts
        }, room="managers", namespace="/")
        
    except ValueError as e:
        emit("error", {"message": f"Invalid data format: {str(e)}"})
    except Exception as e:
        emit("error", {"message": f"Failed to update location: {str(e)}"})


@socketio.on("shift:stop", namespace="/")
def handle_shift_stop(data: dict):
    """
    Employee stops their shift with final location.
    Payload: {
        employee_id: str,
        lat: float,
        lng: float,
        accuracy: float,
        stopped_at: str (ISO format)
    }
    """
    try:
        # Validate required fields
        required = ["employee_id", "lat", "lng", "accuracy", "stopped_at"]
        missing = [f for f in required if f not in data]
        if missing:
            emit("error", {"message": f"Missing required fields: {', '.join(missing)}"})
            return

        employee_id = data["employee_id"]
        lat = float(data["lat"])
        lng = float(data["lng"])
        accuracy = float(data["accuracy"])
        stopped_at = data["stopped_at"]

        db = get_db()
        service = AttendanceRealtimeService(db)
        
        # Process shift stop
        result = service.stop_shift(
            employee_id=employee_id,
            lat=lat,
            lng=lng,
            accuracy=accuracy,
            stopped_at=stopped_at
        )
        
        if not result["success"]:
            emit("error", {"message": result["error"]})
            return
        
        # Confirm to employee
        emit("shift:stopped", {
            "employee_id": employee_id,
            "stopped_at": stopped_at,
            "duration_minutes": result.get("duration_minutes"),
            "location": {"lat": lat, "lng": lng, "accuracy": accuracy}
        }, room=f"employee:{employee_id}")
        
        # Broadcast to managers
        socketio.emit("employee:location", {
            "employee_id": employee_id,
            "lat": lat,
            "lng": lng,
            "accuracy": accuracy,
            "status": "inactive",
            "photo_url": result.get("photo_url"),
            "last_seen_at": stopped_at
        }, room="managers", namespace="/")
        
    except ValueError as e:
        emit("error", {"message": f"Invalid data format: {str(e)}"})
    except Exception as e:
        emit("error", {"message": f"Failed to stop shift: {str(e)}"})


@socketio.on("disconnect", namespace="/")
def handle_disconnect():
    """Handle client disconnect - cleanup if needed"""
    pass
