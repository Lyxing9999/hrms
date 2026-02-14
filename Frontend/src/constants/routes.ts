export const ROUTES = {
  // ============================================
  // ADMIN ROUTES (School Management)
  // ============================================
  ADMIN: {
    DASHBOARD: "/admin/dashboard",
    MANAGE_USERS: "/admin/manage-user",
    MANAGE_CLASSES: "/admin/manage-class",
    TEACHING_ASSIGNMENTS: "/admin/teaching-assignments",
    MANAGE_SUBJECTS: "/admin/manage-subject",
    MANAGE_SCHEDULES: "/admin/manage-schedule",
    NOTIFICATIONS: "/admin/notifications",
    SYSTEM_EVENTS: "/admin/events",
    SETTINGS: "/admin/settings",
  },

  // ============================================
  // TEACHER ROUTES
  // ============================================
  TEACHER: {
    DASHBOARD: "/teacher/dashboard",
    MANAGE_STUDENTS: "/teacher/students",
    MY_CLASSES: "/teacher/classes",
    GRADES: "/teacher/grades",
    SCHEDULE: "/teacher/schedule",
    ATTENDANCE: "/teacher/attendance",
    CALENDAR: "/teacher/calendar",
    NOTIFICATIONS: "/teacher/notifications",
    SETTINGS: "/teacher/settings",
  },

  // ============================================
  // STUDENT ROUTES
  // ============================================
  STUDENT: {
    DASHBOARD: "/student/dashboard",
    ENROLLMENTS: "/student/enrollments",
    MY_CLASSES: "/student/classes",
    MY_GRADES: "/student/grades",
    MY_SCHEDULE: "/student/schedule",
    ATTENDANCE: "/student/attendance",
    NOTIFICATIONS: "/student/notifications",
    CALENDAR: "/student/calendar",
    SETTINGS: "/student/settings",
  },

  // ============================================
  // HRMS ROUTES (Human Resource Management)
  // ============================================
  HR_ADMIN: {
    // Dashboard
    DASHBOARD: "/hr",
    
    // Employee Management
    EMPLOYEES: "/hr/employees/employee-profile",
    EMPLOYEE_DETAIL: (id: string) => `/hr/employees/${id}`,
    EMPLOYEE_CREATE: "/hr/employees/create",
    
    // Leave Management
    LEAVES: "/hr/leaves",
    LEAVE_DETAIL: "/hr/leaves/:id",
    MY_LEAVES: "/hr/my-leaves",
    LEAVE_APPROVALS: "/hr/leave-approvals",
    
    // Attendance System
    ATTENDANCE: "/hr/attendance",
    ATTENDANCE_CHECK_IN: "/hr/attendance/check-in",
    ATTENDANCE_HISTORY: "/hr/attendance/history",
    ATTENDANCE_TEAM: "/hr/attendance/team",
    ATTENDANCE_REPORTS: "/hr/attendance/reports",
    
    // Overtime Management
    OVERTIME: "/hr/overtime",
    OVERTIME_REQUEST: "/hr/overtime/request",
    OVERTIME_APPROVALS: "/hr/overtime/approvals",
    OVERTIME_HISTORY: "/hr/overtime/history",
    
    // Payroll System
    PAYROLL: "/hr/payroll",
    PAYROLL_PROCESS: "/hr/payroll/process",
    PAYROLL_HISTORY: "/hr/payroll/history",
    PAYSLIPS: "/hr/payslips",
    PAYSLIP_DETAIL: "/hr/payslips/:id",
    
    // Configuration
    CONFIG: "/hr/config",
    WORKING_SCHEDULES: "/hr/config/schedules",
    WORK_LOCATIONS: "/hr/config/locations",
    PUBLIC_HOLIDAYS: "/hr/config/holidays",
    DEDUCTION_RULES: "/hr/config/deductions",
    
    // Reports & Analytics
    REPORTS: "/hr/reports",
    REPORTS_ATTENDANCE: "/hr/reports/attendance",
    REPORTS_OVERTIME: "/hr/reports/overtime",
    REPORTS_PAYROLL: "/hr/reports/payroll",
    REPORTS_DEDUCTIONS: "/hr/reports/deductions",
    
    // Organization Structure (Legacy)
    COMPANY: "/hr/company",
    DEPARTMENT: "/hr/department",
    POSITION: "/hr/position",
    
    // System
    NOTIFICATIONS: "/hr/notifications",
    CALENDAR: "/hr/calendar",
    SETTINGS: "/hr/settings",
  },

  // ============================================
  // EMPLOYEE ROUTES (Self-Service Portal)
  // ============================================
  EMPLOYEE: {
    DASHBOARD: "/employee/dashboard",
    MY_PROFILE: "/employee/profile",
    MY_LEAVES: "/employee/leaves",
    MY_ATTENDANCE: "/employee/attendance",
    CHECK_IN: "/employee/check-in",
    MY_OVERTIME: "/employee/overtime",
    MY_PAYSLIPS: "/employee/payslips",
    MY_SCHEDULE: "/employee/schedule",
    NOTIFICATIONS: "/employee/notifications",
    SETTINGS: "/employee/settings",
  },

  // ============================================
  // MANAGER ROUTES
  // ============================================
  MANAGER: {
    DASHBOARD: "/manager/dashboard",
    TEAM: "/manager/team",
    TEAM_ATTENDANCE: "/manager/team/attendance",
    LEAVE_APPROVALS: "/manager/leave-approvals",
    OVERTIME_APPROVALS: "/manager/overtime-approvals",
    TEAM_REPORTS: "/manager/reports",
    NOTIFICATIONS: "/manager/notifications",
    SETTINGS: "/manager/settings",
  },

  // ============================================
  // PAYROLL MANAGER ROUTES
  // ============================================
  PAYROLL_MANAGER: {
    DASHBOARD: "/payroll/dashboard",
    PROCESS_PAYROLL: "/payroll/process",
    PAYROLL_HISTORY: "/payroll/history",
    PAYSLIPS: "/payroll/payslips",
    REPORTS: "/payroll/reports",
    SETTINGS: "/payroll/settings",
  },
} as const;

export type RoutePath = (typeof ROUTES)[keyof typeof ROUTES][keyof unknown];
