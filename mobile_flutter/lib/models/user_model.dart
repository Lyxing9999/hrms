class UserModel {
  final String id;
  final String username;
  final String email;
  final String? employeeId;
  final String? employeeName;
  final String? employeeCode;
  final String? department;
  final String? position;
  final String? photoUrl;
  final List<String> roles;

  UserModel({
    required this.id,
    required this.username,
    required this.email,
    this.employeeId,
    this.employeeName,
    this.employeeCode,
    this.department,
    this.position,
    this.photoUrl,
    required this.roles,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] ?? json['_id'] ?? '',
      username: json['username'] ?? '',
      email: json['email'] ?? '',
      employeeId: json['employee_id'],
      employeeName: json['employee_name'],
      employeeCode: json['employee_code'],
      department: json['department'],
      position: json['position'],
      photoUrl: json['photo_url'],
      roles: List<String>.from(json['roles'] ?? []),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'employee_id': employeeId,
      'employee_name': employeeName,
      'employee_code': employeeCode,
      'department': department,
      'position': position,
      'photo_url': photoUrl,
      'roles': roles,
    };
  }
}
