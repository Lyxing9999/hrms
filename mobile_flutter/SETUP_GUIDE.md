# Flutter Mobile App - Quick Setup Guide

## Step-by-Step Setup

### 1. Install Flutter

```bash
# macOS (using Homebrew)
brew install flutter

# Or download from: https://flutter.dev/docs/get-started/install
```

Verify installation:
```bash
flutter doctor
```

### 2. Setup Project

```bash
cd mobile_flutter
flutter pub get
```

### 3. Configure Backend URL

**For Android Emulator:**
```dart
// lib/config/app_config.dart
static const String baseUrl = 'http://10.0.2.2:5000';
```

**For iOS Simulator:**
```dart
static const String baseUrl = 'http://localhost:5000';
```

**For Physical Device:**
```dart
// Use your computer's IP address
static const String baseUrl = 'http://192.168.1.100:5000';
```

To find your IP:
```bash
# macOS/Linux
ifconfig | grep "inet "

# Windows
ipconfig
```

### 4. Add Android Permissions

Create/edit `android/app/src/main/AndroidManifest.xml`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
    <uses-permission android:name="android.permission.CAMERA"/>
    
    <application
        android:label="HRMS Mobile"
        android:usesCleartextTraffic="true"
        android:icon="@mipmap/ic_launcher">
        <!-- ... -->
    </application>
</manifest>
```

### 5. Add iOS Permissions

Create/edit `ios/Runner/Info.plist`:

```xml
<dict>
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>We need your location to verify check-in at office</string>
    
    <key>NSCameraUsageDescription</key>
    <string>We need camera access to take your photo for attendance</string>
    
    <key>NSPhotoLibraryUsageDescription</key>
    <string>We need photo library access to select photos</string>
</dict>
```

### 6. Run the App

```bash
# List available devices
flutter devices

# Run on specific device
flutter run -d <device_id>

# Or just run (will prompt to select device)
flutter run
```

### 7. Test Login

Use your existing backend credentials:
- Email: `employee@example.com`
- Password: `your_password`

## Common Issues & Solutions

### Issue: "No devices found"

**Solution:**
```bash
# For Android
# 1. Enable USB debugging on phone
# 2. Connect via USB
# 3. Accept debugging prompt on phone

# For iOS
# 1. Open Xcode
# 2. Connect iPhone
# 3. Trust computer on iPhone
```

### Issue: "Cannot connect to backend"

**Solution:**
1. Check backend is running:
   ```bash
   curl http://localhost:5000/api/iam/login
   ```

2. For physical device, use computer's IP:
   ```bash
   # Find your IP
   ifconfig | grep "inet "
   
   # Update app_config.dart
   static const String baseUrl = 'http://YOUR_IP:5000';
   ```

3. Ensure device and computer on same WiFi network

### Issue: "Location permission denied"

**Solution:**
- Go to device Settings
- Find HRMS Mobile app
- Enable Location permission
- Restart app

### Issue: "Camera not working"

**Solution:**
- Enable Camera permission in device settings
- Restart app
- Try using Gallery option instead

## Building for Production

### Android APK

```bash
# Build release APK
flutter build apk --release

# Output: build/app/outputs/flutter-apk/app-release.apk
```

### iOS App

```bash
# Build iOS app
flutter build ios --release

# Then open in Xcode to archive and upload
open ios/Runner.xcworkspace
```

## Testing Checklist

- [ ] Login with valid credentials
- [ ] Location permission granted
- [ ] Camera permission granted
- [ ] GPS location acquired
- [ ] Within geofence (150m from office)
- [ ] Photo captured successfully
- [ ] Check-in successful
- [ ] Check-out successful
- [ ] History displays correctly
- [ ] Logout works

## Next Steps

1. Test on physical device
2. Verify all features work
3. Build release APK/IPA
4. Distribute to employees

## Support

If you encounter issues:
1. Check `flutter doctor` output
2. Verify backend is running
3. Check device permissions
4. Review app logs: `flutter logs`
