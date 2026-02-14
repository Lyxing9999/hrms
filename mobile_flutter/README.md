# HRMS Mobile - Flutter Employee Check-in App

A Flutter mobile application for employee attendance management with GPS-based check-in/check-out and real-time location tracking.

## Features

- ✅ **Login/Logout** - Secure authentication using existing backend API
- 📍 **GPS Location Tracking** - Real-time location with geofence validation
- 📸 **Photo Capture** - Take selfie for check-in/check-out
- ⏰ **Check-in/Check-out** - Track work hours with location verification
- 📊 **Attendance History** - View past attendance records
- 🔒 **Secure Storage** - Encrypted token storage
- 🌐 **Real-time Updates** - Socket.IO integration for live tracking

## Prerequisites

- Flutter SDK (>=3.0.0)
- Dart SDK
- Android Studio / Xcode
- Backend API running on `http://localhost:5000`

## Installation

### 1. Install Flutter Dependencies

```bash
cd mobile_flutter
flutter pub get
```

### 2. Configure Backend URL

Edit `lib/config/app_config.dart`:

```dart
static const String baseUrl = 'http://YOUR_BACKEND_IP:5000';
```

**Important:** 
- For Android Emulator: Use `http://10.0.2.2:5000`
- For iOS Simulator: Use `http://localhost:5000`
- For Physical Device: Use your computer's IP address (e.g., `http://192.168.1.100:5000`)

### 3. Platform-Specific Setup

#### Android

Add permissions to `android/app/src/main/AndroidManifest.xml`:

```xml
<manifest>
    <!-- Add these permissions -->
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
    <uses-permission android:name="android.permission.CAMERA"/>
    
    <application
        android:usesCleartextTraffic="true">
        <!-- ... -->
    </application>
</manifest>
```

#### iOS

Add permissions to `ios/Runner/Info.plist`:

```xml
<dict>
    <!-- Add these keys -->
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>We need your location to verify check-in at office</string>
    <key>NSCameraUsageDescription</key>
    <string>We need camera access to take your photo for attendance</string>
    <key>NSPhotoLibraryUsageDescription</key>
    <string>We need photo library access to select photos</string>
</dict>
```

## Running the App

### Development Mode

```bash
# Run on connected device/emulator
flutter run

# Run with specific device
flutter devices
flutter run -d <device_id>

# Run in release mode
flutter run --release
```

### Build APK (Android)

```bash
# Debug APK
flutter build apk --debug

# Release APK
flutter build apk --release

# Split APKs by ABI (smaller size)
flutter build apk --split-per-abi
```

### Build iOS

```bash
flutter build ios --release
```

## Project Structure

```
mobile_flutter/
├── lib/
│   ├── config/
│   │   └── app_config.dart          # App configuration
│   ├── models/
│   │   ├── user_model.dart          # User data model
│   │   └── attendance_model.dart    # Attendance data model
│   ├── providers/
│   │   ├── auth_provider.dart       # Authentication state
│   │   └── attendance_provider.dart # Attendance state
│   ├── screens/
│   │   ├── splash_screen.dart       # Splash screen
│   │   ├── login_screen.dart        # Login screen
│   │   ├── home_screen.dart         # Main navigation
│   │   ├── check_in_screen.dart     # Check-in/out screen
│   │   └── history_screen.dart      # Attendance history
│   ├── services/
│   │   ├── api_service.dart         # Backend API calls
│   │   ├── storage_service.dart     # Local storage
│   │   └── location_service.dart    # GPS location
│   └── main.dart                    # App entry point
├── pubspec.yaml                     # Dependencies
└── README.md                        # This file
```

## Backend API Integration

The app uses the following backend endpoints:

### Authentication
- `POST /api/iam/login` - Login
- `POST /api/iam/logout` - Logout
- `POST /api/iam/refresh` - Refresh token

### Attendance
- `POST /api/hrms/employee/attendance/check-in` - Check in
- `POST /api/hrms/employee/attendance/check-out` - Check out
- `GET /api/hrms/employee/attendance/history` - Get history

### Upload
- `POST /api/uploads/photo` - Upload photo

## Configuration

### Office Location (PPIU)

Edit `lib/config/app_config.dart`:

```dart
static const double officeLat = 11.5563;
static const double officeLng = 104.9282;
static const double geofenceRadius = 150.0; // meters
```

### API Timeout

```dart
static const Duration requestTimeout = Duration(seconds: 30);
```

## Usage

### 1. Login
- Enter your email and password
- Credentials are validated against backend API
- Token is securely stored

### 2. Check In
- Allow location permission
- Ensure you're within 150m of office
- Take a selfie photo
- Tap "Check In" button
- Location and photo are sent to backend

### 3. Check Out
- Tap "Check Out" button
- Optionally take another photo
- Duration is calculated automatically

### 4. View History
- Navigate to "History" tab
- See all past attendance records
- Pull to refresh

## Troubleshooting

### Location Permission Denied
- Go to device Settings > Apps > HRMS Mobile > Permissions
- Enable Location permission

### Camera Not Working
- Enable Camera permission in device settings
- Restart the app

### Cannot Connect to Backend
- Check backend is running: `curl http://localhost:5000/api/iam/login`
- Verify `baseUrl` in `app_config.dart`
- For physical device, use computer's IP address
- Ensure device and computer are on same network

### GPS Accuracy Poor
- Move to an open area
- Wait a few seconds for GPS to stabilize
- Check if location services are enabled

### Outside Geofence Error
- Verify office coordinates in `app_config.dart`
- Check geofence radius (default: 150m)
- Ensure GPS accuracy is good (<50m)

## Testing Credentials

Use the same credentials as your web application:

```
Email: employee@example.com
Password: your_password
```

## Dependencies

Key packages used:

- `provider` - State management
- `http` & `dio` - HTTP requests
- `shared_preferences` - Local storage
- `flutter_secure_storage` - Secure token storage
- `geolocator` - GPS location
- `permission_handler` - Runtime permissions
- `image_picker` - Camera/gallery access
- `socket_io_client` - Real-time communication
- `intl` - Date/time formatting

## Security

- Tokens stored in encrypted secure storage
- HTTPS recommended for production
- Location data validated on backend
- Photo upload with size limits
- Session timeout handling

## Future Enhancements

- [ ] Offline mode with sync
- [ ] Push notifications
- [ ] Biometric authentication
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Leave request management
- [ ] Payroll information

## License

Proprietary - PPIU (Phnom Penh International University)

## Support

For issues or questions, contact your system administrator.
