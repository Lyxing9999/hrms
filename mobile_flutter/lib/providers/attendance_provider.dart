import 'dart:io';
import 'package:flutter/material.dart';
import 'package:hrms_mobile/models/attendance_model.dart';
import 'package:hrms_mobile/services/api_service.dart';
import 'package:hrms_mobile/services/location_service.dart';
import 'package:geolocator/geolocator.dart';

class AttendanceProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  final LocationService _locationService = LocationService();

  AttendanceModel? _currentAttendance;
  List<AttendanceModel> _history = [];
  bool _isLoading = false;
  String? _error;
  Position? _currentLocation;

  AttendanceModel? get currentAttendance => _currentAttendance;
  List<AttendanceModel> get history => _history;
  bool get isLoading => _isLoading;
  String? get error => _error;
  Position? get currentLocation => _currentLocation;
  bool get isCheckedIn => _currentAttendance != null && _currentAttendance!.checkOutTime == null;

  // Get current location
  Future<Position?> getCurrentLocation() async {
    try {
      _currentLocation = await _locationService.getCurrentLocation();
      notifyListeners();
      return _currentLocation;
    } catch (e) {
      _error = 'Failed to get location: ${e.toString()}';
      notifyListeners();
      return null;
    }
  }

  // Check if within geofence
  bool isWithinGeofence() {
    if (_currentLocation == null) return false;
    return _locationService.isWithinGeofence(
      _currentLocation!.latitude,
      _currentLocation!.longitude,
    );
  }

  // Get distance from office
  double? getDistanceFromOffice() {
    if (_currentLocation == null) return null;
    return _locationService.calculateDistanceFromOffice(
      _currentLocation!.latitude,
      _currentLocation!.longitude,
    );
  }

  // Check In
  Future<bool> checkIn(File photoFile) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // Get current location
      final position = await getCurrentLocation();
      if (position == null) {
        _error = 'Unable to get your location';
        _isLoading = false;
        notifyListeners();
        return false;
      }

      // Check geofence
      if (!isWithinGeofence()) {
        _error = 'You are too far from the office (${getDistanceFromOffice()?.toStringAsFixed(0)}m)';
        _isLoading = false;
        notifyListeners();
        return false;
      }

      // Upload photo
      final uploadResult = await _apiService.uploadPhoto(photoFile);
      if (!uploadResult['success']) {
        _error = uploadResult['error'];
        _isLoading = false;
        notifyListeners();
        return false;
      }

      final photoUrl = uploadResult['photo_url'];

      // Check in
      final result = await _apiService.checkIn(
        lat: position.latitude,
        lng: position.longitude,
        accuracy: position.accuracy,
        photoUrl: photoUrl,
      );

      if (result['success']) {
        _currentAttendance = AttendanceModel.fromJson(result['data']['attendance']);
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _error = result['error'];
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Check Out
  Future<bool> checkOut({File? photoFile}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // Get current location
      final position = await getCurrentLocation();
      if (position == null) {
        _error = 'Unable to get your location';
        _isLoading = false;
        notifyListeners();
        return false;
      }

      String? photoUrl;
      if (photoFile != null) {
        final uploadResult = await _apiService.uploadPhoto(photoFile);
        if (uploadResult['success']) {
          photoUrl = uploadResult['photo_url'];
        }
      }

      // Check out
      final result = await _apiService.checkOut(
        lat: position.latitude,
        lng: position.longitude,
        accuracy: position.accuracy,
        photoUrl: photoUrl,
      );

      if (result['success']) {
        _currentAttendance = AttendanceModel.fromJson(result['data']['attendance']);
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _error = result['error'];
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Load attendance history
  Future<void> loadHistory({DateTime? startDate, DateTime? endDate}) async {
    _isLoading = true;
    notifyListeners();

    try {
      final result = await _apiService.getAttendanceHistory(
        startDate: startDate,
        endDate: endDate,
      );

      if (result['success']) {
        final List<dynamic> data = result['data']['attendance'] ?? [];
        _history = data.map((json) => AttendanceModel.fromJson(json)).toList();
      } else {
        _error = result['error'];
      }
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}
