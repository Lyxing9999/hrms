import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:hrms_mobile/config/app_config.dart';
import 'package:hrms_mobile/services/storage_service.dart';

class ApiService {
  final StorageService _storage = StorageService();

  Future<Map<String, String>> _getHeaders({bool includeAuth = true}) async {
    final headers = {
      'Content-Type': 'application/json',
    };

    if (includeAuth) {
      final token = await _storage.getAccessToken();
      if (token != null) {
        headers['Authorization'] = 'Bearer $token';
      }
    }

    return headers;
  }

  // Login
  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final response = await http
          .post(
            Uri.parse(AppConfig.loginEndpoint),
            headers: await _getHeaders(includeAuth: false),
            body: jsonEncode({
              'email': email,
              'password': password,
            }),
          )
          .timeout(AppConfig.requestTimeout);

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        return {'success': true, 'data': data};
      } else {
        return {
          'success': false,
          'error': data['message'] ?? 'Login failed'
        };
      }
    } catch (e) {
      return {'success': false, 'error': 'Network error: ${e.toString()}'};
    }
  }

  // Logout
  Future<Map<String, dynamic>> logout() async {
    try {
      final response = await http
          .post(
            Uri.parse(AppConfig.logoutEndpoint),
            headers: await _getHeaders(),
          )
          .timeout(AppConfig.requestTimeout);

      return {'success': response.statusCode == 200};
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }

  // Check In
  Future<Map<String, dynamic>> checkIn({
    required double lat,
    required double lng,
    required double accuracy,
    required String photoUrl,
  }) async {
    try {
      final response = await http
          .post(
            Uri.parse(AppConfig.checkInEndpoint),
            headers: await _getHeaders(),
            body: jsonEncode({
              'latitude': lat,
              'longitude': lng,
              'accuracy': accuracy,
              'photo_url': photoUrl,
            }),
          )
          .timeout(AppConfig.requestTimeout);

      final data = jsonDecode(response.body);

      if (response.statusCode == 200 || response.statusCode == 201) {
        return {'success': true, 'data': data};
      } else {
        return {
          'success': false,
          'error': data['message'] ?? 'Check-in failed'
        };
      }
    } catch (e) {
      return {'success': false, 'error': 'Network error: ${e.toString()}'};
    }
  }

  // Check Out
  Future<Map<String, dynamic>> checkOut({
    required double lat,
    required double lng,
    required double accuracy,
    String? photoUrl,
  }) async {
    try {
      // First, get today's attendance to get the ID
      final todayResponse = await http
          .get(
            Uri.parse('${AppConfig.apiBaseUrl}/hrms/employee/attendance/today'),
            headers: await _getHeaders(),
          )
          .timeout(AppConfig.requestTimeout);

      if (todayResponse.statusCode != 200) {
        return {'success': false, 'error': 'No active check-in found for today'};
      }

      final todayData = jsonDecode(todayResponse.body);
      final attendanceId = todayData['data']['id'];

      // Now check out
      final response = await http
          .post(
            Uri.parse('${AppConfig.apiBaseUrl}/hrms/employee/attendance/$attendanceId/check-out'),
            headers: await _getHeaders(),
            body: jsonEncode({
              'latitude': lat,
              'longitude': lng,
              'accuracy': accuracy,
              if (photoUrl != null) 'photo_url': photoUrl,
            }),
          )
          .timeout(AppConfig.requestTimeout);

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        return {'success': true, 'data': data};
      } else {
        return {
          'success': false,
          'error': data['message'] ?? 'Check-out failed'
        };
      }
    } catch (e) {
      return {'success': false, 'error': 'Network error: ${e.toString()}'};
    }
  }

  // Get Attendance History
  Future<Map<String, dynamic>> getAttendanceHistory({
    DateTime? startDate,
    DateTime? endDate,
  }) async {
    try {
      var url = AppConfig.attendanceHistoryEndpoint;
      if (startDate != null && endDate != null) {
        url +=
            '?start_date=${startDate.toIso8601String()}&end_date=${endDate.toIso8601String()}';
      }

      final response = await http
          .get(
            Uri.parse(url),
            headers: await _getHeaders(),
          )
          .timeout(AppConfig.requestTimeout);

      final data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        return {'success': true, 'data': data};
      } else {
        return {
          'success': false,
          'error': data['message'] ?? 'Failed to fetch history'
        };
      }
    } catch (e) {
      return {'success': false, 'error': 'Network error: ${e.toString()}'};
    }
  }

  // Upload Photo
  Future<Map<String, dynamic>> uploadPhoto(File imageFile) async {
    try {
      final token = await _storage.getAccessToken();
      final request = http.MultipartRequest(
        'POST',
        Uri.parse(AppConfig.uploadPhotoEndpoint),
      );

      request.headers['Authorization'] = 'Bearer $token';
      request.files.add(
        await http.MultipartFile.fromPath('photo', imageFile.path),
      );

      final streamedResponse =
          await request.send().timeout(AppConfig.requestTimeout);
      final response = await http.Response.fromStream(streamedResponse);
      final data = jsonDecode(response.body);

      if (response.statusCode == 200 || response.statusCode == 201) {
        return {'success': true, 'photo_url': data['photo_url']};
      } else {
        return {
          'success': false,
          'error': data['error'] ?? 'Upload failed'
        };
      }
    } catch (e) {
      return {'success': false, 'error': 'Upload error: ${e.toString()}'};
    }
  }
}
