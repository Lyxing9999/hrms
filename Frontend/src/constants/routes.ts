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
    DASHBOARD: "/hr",

    EMPLOYEES: "/hr/employees",
    EMPLOYEE_ACCOUNTS: "/hr/employees/accounts",
    EMPLOYEE_ARCHIVED: "/hr/employees/archived",

    ATTENDANCE: "/hr/attendance",
    ATTENDANCE_WRONG_LOCATION: "/hr/attendance/wrong-location",
    ATTENDANCE_ADJUSTMENTS: "/hr/attendance/adjustments",
    ATTENDANCE_REPORTS: "/hr/attendance/reports",

    OVERTIME: "/hr/overtime",
    OVERTIME_REVIEWS: "/hr/overtime/reviews",
    OVERTIME_HISTORY: "/hr/overtime/history",

    LEAVES: "/hr/leaves",
    LEAVE_REVIEWS: "/hr/leaves/reviews",
    LEAVE_BALANCES: "/hr/leaves/balances",

    PAYROLL_RUNS: "/hr/payroll/runs",
    PAYSLIPS: "/hr/payroll/payslips",
    PAYROLL_HISTORY: "/hr/payroll/history",

    WORKING_SCHEDULES: "/hr/config/schedules",
    WORK_LOCATIONS: "/hr/config/locations",
    PUBLIC_HOLIDAYS: "/hr/config/public-holidays",
    DEDUCTION_RULES: "/hr/config/deduction-rules",
    OT_RULES: "/hr/config/overtime-rules",

    REPORTS_ATTENDANCE: "/hr/reports/attendance",
    REPORTS_OVERTIME: "/hr/reports/overtime",
    REPORTS_PAYROLL: "/hr/reports/payroll",
    REPORTS_WRONG_LOCATION: "/hr/reports/wrong-location",
  },

  EMPLOYEE: {
    DASHBOARD: "/employee",
    PROFILE: "/employee/profile",

    ATTENDANCE_CHECK: "/employee/attendance/check",
    ATTENDANCE_HISTORY: "/employee/attendance/history",

    OVERTIME_REQUEST: "/employee/overtime/request",
    OVERTIME_HISTORY: "/employee/overtime/history",

    LEAVE_REQUEST: "/employee/leaves/request",
    LEAVE_HISTORY: "/employee/leaves/history",
    LEAVE_BALANCE: "/employee/leaves/balance",

    PAYSLIPS: "/employee/payslips",
  },

  MANAGER: {
    DASHBOARD: "/manager",

    ATTENDANCE_TEAM: "/manager/attendance/team",
    ATTENDANCE_REPORTS: "/manager/attendance/reports",

    OVERTIME_REVIEWS: "/manager/overtime/reviews",
    OVERTIME_HISTORY: "/manager/overtime/history",

    LEAVE_REVIEWS: "/manager/leaves/reviews",
    LEAVE_HISTORY: "/manager/leaves/history",

    REPORTS_TEAM: "/manager/reports/team",
  },

  PAYROLL_MANAGER: {
    DASHBOARD: "/payroll",

    PAYROLL_PROCESS: "/payroll/runs/generate",
    PAYROLL_RUNS: "/payroll/runs",
    PAYSLIPS: "/payroll/payslips",

    ATTENDANCE_FINAL: "/payroll/attendance/final",
    OVERTIME_APPROVED: "/payroll/overtime/approved",

    REPORTS_PAYROLL: "/payroll/reports",
  },
} as const;

export type RoutePath = (typeof ROUTES)[keyof typeof ROUTES][keyof unknown];
