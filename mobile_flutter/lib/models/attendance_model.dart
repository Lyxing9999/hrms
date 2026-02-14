class AttendanceModel {
  final String id;
  final String employeeId;
  final DateTime checkInTime;
  final DateTime? checkOutTime;
  final LocationData checkInLocation;
  final LocationData? checkOutLocation;
  final String? checkInPhotoUrl;
  final String? checkOutPhotoUrl;
  final String status;
  final int? durationMinutes;

  AttendanceModel({
    required this.id,
    required this.employeeId,
    required this.checkInTime,
    this.checkOutTime,
    required this.checkInLocation,
    this.checkOutLocation,
    this.checkInPhotoUrl,
    this.checkOutPhotoUrl,
    required this.status,
    this.durationMinutes,
  });

  factory AttendanceModel.fromJson(Map<String, dynamic> json) {
    return AttendanceModel(
      id: json['_id'] ?? json['id'] ?? '',
      employeeId: json['employee_id'] ?? '',
      checkInTime: DateTime.parse(json['check_in_time']),
      checkOutTime: json['check_out_time'] != null
          ? DateTime.parse(json['check_out_time'])
          : null,
      checkInLocation: LocationData.fromJson(json['check_in_location']),
      checkOutLocation: json['check_out_location'] != null
          ? LocationData.fromJson(json['check_out_location'])
          : null,
      checkInPhotoUrl: json['check_in_photo_url'],
      checkOutPhotoUrl: json['check_out_photo_url'],
      status: json['status'] ?? 'active',
      durationMinutes: json['duration_minutes'],
    );
  }
}

class LocationData {
  final double lat;
  final double lng;
  final double accuracy;
  final double? distanceFromOffice;

  LocationData({
    required this.lat,
    required this.lng,
    required this.accuracy,
    this.distanceFromOffice,
  });

  factory LocationData.fromJson(Map<String, dynamic> json) {
    return LocationData(
      lat: (json['lat'] ?? 0.0).toDouble(),
      lng: (json['lng'] ?? 0.0).toDouble(),
      accuracy: (json['accuracy'] ?? 0.0).toDouble(),
      distanceFromOffice: json['distance_from_office_m']?.toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'lat': lat,
      'lng': lng,
      'accuracy': accuracy,
      if (distanceFromOffice != null) 'distance_from_office_m': distanceFromOffice,
    };
  }
}
