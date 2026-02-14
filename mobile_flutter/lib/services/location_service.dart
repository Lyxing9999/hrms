import 'dart:math';
import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:hrms_mobile/config/app_config.dart';

class LocationService {
  // Request location permission
  Future<bool> requestPermission() async {
    final status = await Permission.location.request();
    return status.isGranted;
  }

  // Check if location permission is granted
  Future<bool> hasPermission() async {
    final status = await Permission.location.status;
    return status.isGranted;
  }

  // Get current location
  Future<Position?> getCurrentLocation() async {
    try {
      final hasPermission = await this.hasPermission();
      if (!hasPermission) {
        final granted = await requestPermission();
        if (!granted) return null;
      }

      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        timeLimit: const Duration(seconds: 10),
      );

      return position;
    } catch (e) {
      print('Error getting location: $e');
      return null;
    }
  }

  // Calculate distance from office
  double calculateDistanceFromOffice(double lat, double lng) {
    return _calculateDistance(
      lat,
      lng,
      AppConfig.officeLat,
      AppConfig.officeLng,
    );
  }

  // Check if within geofence
  bool isWithinGeofence(double lat, double lng) {
    final distance = calculateDistanceFromOffice(lat, lng);
    return distance <= AppConfig.geofenceRadius;
  }

  // Calculate distance between two coordinates (Haversine formula)
  double _calculateDistance(double lat1, double lng1, double lat2, double lng2) {
    const R = 6371000.0; // Earth radius in meters
    final phi1 = lat1 * pi / 180;
    final phi2 = lat2 * pi / 180;
    final deltaPhi = (lat2 - lat1) * pi / 180;
    final deltaLambda = (lng2 - lng1) * pi / 180;

    final a = sin(deltaPhi / 2) * sin(deltaPhi / 2) +
        cos(phi1) * cos(phi2) * sin(deltaLambda / 2) * sin(deltaLambda / 2);
    final c = 2 * atan2(sqrt(a), sqrt(1 - a));

    return R * c;
  }

  // Get location accuracy status
  String getAccuracyStatus(double accuracy) {
    if (accuracy < 50) return 'Good';
    if (accuracy < 100) return 'Fair';
    return 'Poor';
  }

  // Get distance status
  String getDistanceStatus(double distance) {
    if (distance < 50) return 'Very Close';
    if (distance < 100) return 'Close';
    if (distance <= AppConfig.geofenceRadius) return 'Within Range';
    return 'Too Far';
  }
}
