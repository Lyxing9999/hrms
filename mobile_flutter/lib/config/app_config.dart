class AppConfig {
  // Backend API Configuration
  static const String baseUrl = 'http://localhost:5000'; // Change to your backend URL
  static const String apiBaseUrl = '$baseUrl/api';
  static const String socketUrl = baseUrl;
  
  // API Endpoints
  static const String loginEndpoint = '$apiBaseUrl/iam/login';
  static const String refreshEndpoint = '$apiBaseUrl/iam/refresh';
  static const String logoutEndpoint = '$apiBaseUrl/iam/logout';
  
  // HRMS Endpoints
  static const String checkInEndpoint = '$apiBaseUrl/hrms/employee/attendance/check-in';
  static const String checkOutEndpoint = '$apiBaseUrl/hrms/employee/attendance/check-out';
  static const String attendanceHistoryEndpoint = '$apiBaseUrl/hrms/employee/attendance/history';
  static const String uploadPhotoEndpoint = '$baseUrl/api/uploads/photo';
  
  // Office Location (PPIU - Phnom Penh International University)
  static const double officeLat = 11.5563;
  static const double officeLng = 104.9282;
  static const double geofenceRadius = 150.0; // meters
  
  // App Settings
  static const int locationUpdateInterval = 5000; // milliseconds
  static const int maxPhotoSizeMB = 5;
  static const Duration requestTimeout = Duration(seconds: 30);
}
