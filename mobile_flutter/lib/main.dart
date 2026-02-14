import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:hrms_mobile/providers/auth_provider.dart';
import 'package:hrms_mobile/providers/attendance_provider.dart';
import 'package:hrms_mobile/screens/splash_screen.dart';
import 'package:hrms_mobile/screens/login_screen.dart';
import 'package:hrms_mobile/screens/home_screen.dart';
import 'package:hrms_mobile/config/app_config.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => AttendanceProvider()),
      ],
      child: MaterialApp(
        title: 'HRMS Mobile',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          primarySwatch: Colors.blue,
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF2196F3),
            brightness: Brightness.light,
          ),
        ),
        initialRoute: '/',
        routes: {
          '/': (context) => const SplashScreen(),
          '/login': (context) => const LoginScreen(),
          '/home': (context) => const HomeScreen(),
        },
      ),
    );
  }
}
