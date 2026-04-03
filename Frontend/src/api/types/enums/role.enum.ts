// All roles in the system
export enum Role {
  ADMIN = "admin",
  TEACHER = "teacher",
  STUDENT = "student",
  FRONT_OFFICE = "front_office",
  PARENT = "parent",
  ACADEMIC = "academic",
  FINANCE = "finance",
  HR_ADMIN = "hr_admin",
  EMPLOYEE = "employee",
  MANAGER = "manager",
  PAYROLL_MANAGER = "payroll_manager",
}

// Non-staff users
export enum UserRole {
  STUDENT = "student",
  PARENT = "parent",
  EMPLOYEE = "employee",
}

// Staff members
export enum StaffRole {
  TEACHER = "teacher",
  ACADEMIC = "academic",
  HR_ADMIN = "hr_admin",
  EMPLOYEE = "employee",
  MANAGER = "manager",
  PAYROLL_MANAGER = "payroll_manager",
}

// Arrays for easy checks
export const AllRoles: Role[] = [
  Role.ADMIN,
  Role.TEACHER,
  Role.STUDENT,
  Role.FRONT_OFFICE,
  Role.PARENT,
  Role.ACADEMIC,
  Role.FINANCE,
  Role.HR_ADMIN,
  Role.EMPLOYEE,
  Role.MANAGER,
  Role.PAYROLL_MANAGER,
];

export const AllUserRoles: UserRole[] = [UserRole.STUDENT, UserRole.PARENT];

export const AllStaffRoles: StaffRole[] = [
  StaffRole.TEACHER,
  StaffRole.ACADEMIC,
  StaffRole.EMPLOYEE,
  StaffRole.MANAGER,
  StaffRole.PAYROLL_MANAGER,
];
