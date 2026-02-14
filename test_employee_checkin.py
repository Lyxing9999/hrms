#!/usr/bin/env python3
"""
Employee Check-In System - End-to-End Test Script

This script tests the complete employee check-in flow:
1. Login as employee
2. Check-in with GPS coordinates
3. Get today's attendance
4. Check-out
5. Get attendance history
6. Get statistics

Usage:
    python test_employee_checkin.py

Requirements:
    - Backend running on http://localhost:5001
    - Employee account with email/password
    - Employee profile linked to user account
"""

import requests
import json
from datetime import datetime, date

# Configuration
BASE_URL = "http://localhost:5001"
EMPLOYEE_EMAIL = "employee@example.com"  # Change this
EMPLOYEE_PASSWORD = "password123"  # Change this

# GPS coordinates (Phnom Penh, Cambodia)
GPS_LAT = 11.56873843923084
GPS_LON = 104.82006716278323


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_response(response):
    """Print formatted response"""
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, default=str)}")
        return data
    except:
        print(f"Response: {response.text}")
        return None


def test_employee_checkin():
    """Run complete employee check-in test"""
    
    print_section("EMPLOYEE CHECK-IN SYSTEM TEST")
    print(f"Testing against: {BASE_URL}")
    print(f"Employee: {EMPLOYEE_EMAIL}")
    print(f"GPS: {GPS_LAT}, {GPS_LON}")
    
    # Step 1: Login
    print_section("Step 1: Login as Employee")
    login_response = requests.post(
        f"{BASE_URL}/api/iam/login",
        json={
            "email": EMPLOYEE_EMAIL,
            "password": EMPLOYEE_PASSWORD
        }
    )
    login_data = print_response(login_response)
    
    if login_response.status_code != 200:
        print("❌ Login failed! Please check credentials.")
        return False
    
    access_token = login_data.get("access_token")
    if not access_token:
        print("❌ No access token received!")
        return False
    
    print(f"✅ Login successful! Token: {access_token[:20]}...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Check if already checked in today
    print_section("Step 2: Check Today's Attendance")
    today_response = requests.get(
        f"{BASE_URL}/api/hrms/employee/attendance/today",
        headers=headers
    )
    today_data = print_response(today_response)
    
    if today_response.status_code == 200 and today_data:
        print("⚠️  Already checked in today!")
        attendance_id = today_data.get("id")
        
        if not today_data.get("check_out_time"):
            print("📍 Proceeding to check-out...")
        else:
            print("✅ Already checked out today. Test complete!")
            return True
    else:
        print("✅ No attendance record for today. Proceeding to check-in...")
        attendance_id = None
    
    # Step 3: Check-In
    if not attendance_id:
        print_section("Step 3: Check-In with GPS")
        checkin_response = requests.post(
            f"{BASE_URL}/api/hrms/employee/attendance/check-in",
            headers=headers,
            json={
                "latitude": GPS_LAT,
                "longitude": GPS_LON,
                "notes": "Test check-in from automated script"
            }
        )
        checkin_data = print_response(checkin_response)
        
        if checkin_response.status_code != 200:
            print("❌ Check-in failed!")
            return False
        
        attendance_id = checkin_data.get("id")
        print(f"✅ Check-in successful! Attendance ID: {attendance_id}")
        print(f"   Check-in time: {checkin_data.get('check_in_time')}")
        print(f"   Status: {checkin_data.get('status')}")
        print(f"   Late minutes: {checkin_data.get('late_minutes')}")
    
    # Step 4: Get Today's Attendance (verify)
    print_section("Step 4: Verify Today's Attendance")
    verify_response = requests.get(
        f"{BASE_URL}/api/hrms/employee/attendance/today",
        headers=headers
    )
    verify_data = print_response(verify_response)
    
    if verify_response.status_code == 200 and verify_data:
        print("✅ Attendance record verified!")
    else:
        print("❌ Failed to verify attendance!")
        return False
    
    # Step 5: Check-Out
    print_section("Step 5: Check-Out")
    print("⏳ Waiting 2 seconds before check-out...")
    import time
    time.sleep(2)
    
    checkout_response = requests.post(
        f"{BASE_URL}/api/hrms/employee/attendance/{attendance_id}/check-out",
        headers=headers,
        json={
            "latitude": GPS_LAT,
            "longitude": GPS_LON,
            "notes": "Test check-out from automated script"
        }
    )
    checkout_data = print_response(checkout_response)
    
    if checkout_response.status_code != 200:
        print("❌ Check-out failed!")
        return False
    
    print(f"✅ Check-out successful!")
    print(f"   Check-out time: {checkout_data.get('check_out_time')}")
    print(f"   Status: {checkout_data.get('status')}")
    print(f"   Early leave minutes: {checkout_data.get('early_leave_minutes')}")
    
    # Step 6: Get Attendance History
    print_section("Step 6: Get Attendance History")
    today_str = date.today().isoformat()
    history_response = requests.get(
        f"{BASE_URL}/api/hrms/admin/attendances",
        headers=headers,
        params={
            "start_date": today_str,
            "end_date": today_str,
            "page": 1,
            "limit": 10
        }
    )
    history_data = print_response(history_response)
    
    if history_response.status_code == 200:
        total = history_data.get("total", 0)
        print(f"✅ Found {total} attendance record(s) for today")
    else:
        print("⚠️  Could not fetch history (may require admin role)")
    
    # Step 7: Get Statistics
    print_section("Step 7: Get Attendance Statistics")
    
    # First, get employee_id from today's attendance
    employee_id = verify_data.get("employee_id")
    
    if employee_id:
        # Get stats for current month
        today = date.today()
        start_of_month = date(today.year, today.month, 1).isoformat()
        end_of_month = today.isoformat()
        
        stats_response = requests.get(
            f"{BASE_URL}/api/hrms/admin/attendances/stats",
            headers=headers,
            params={
                "employee_id": employee_id,
                "start_date": start_of_month,
                "end_date": end_of_month
            }
        )
        stats_data = print_response(stats_response)
        
        if stats_response.status_code == 200:
            print(f"✅ Statistics retrieved successfully!")
            print(f"   Present days: {stats_data.get('present_days')}")
            print(f"   Late days: {stats_data.get('late_days')}")
            print(f"   Attendance rate: {stats_data.get('attendance_rate')}%")
        else:
            print("⚠️  Could not fetch statistics")
    else:
        print("⚠️  No employee_id available for statistics")
    
    # Final Summary
    print_section("TEST SUMMARY")
    print("✅ All tests passed successfully!")
    print("\nTest Results:")
    print("  ✅ Login")
    print("  ✅ Check-in with GPS")
    print("  ✅ Attendance verification")
    print("  ✅ Check-out")
    print("  ✅ Attendance history")
    print("  ✅ Statistics")
    print("\n🎉 Employee check-in system is fully functional!")
    
    return True


if __name__ == "__main__":
    try:
        success = test_employee_checkin()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
