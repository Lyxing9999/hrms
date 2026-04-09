/**
 * Icon mappings for navigation and route references
 * Used in sidebars, breadcrumbs, and navigation components
 */

export const ICONS = {
  // Auth
  LOGIN: "ep:login",
  FORGOT_PASSWORD: "ep:question-filled",
  RESET_PASSWORD: "ep:refresh",

  // Admin Module
  ADMIN_DASHBOARD: "ep:data-analysis",
  ADMIN_USERS: "ep:user",
  ADMIN_CLASSES: "ep:collection",
  ADMIN_SUBJECTS: "ep:notebook",
  ADMIN_SCHEDULES: "ep:calendar",
  ADMIN_TEACHING_ASSIGNMENTS: "ep:document-copy",
  ADMIN_NOTIFICATIONS: "ep:bell",
  ADMIN_EVENTS: "ep:date",
  ADMIN_SETTINGS: "ep:setting",

  // Teacher Module
  TEACHER_DASHBOARD: "ep:data-analysis",
  TEACHER_STUDENTS: "ep:user",
  TEACHER_CLASSES: "ep:collection",
  TEACHER_GRADES: "ep:document",
  TEACHER_SCHEDULE: "ep:calendar",
  TEACHER_ATTENDANCE: "ep:check",
  TEACHER_CALENDAR: "ep:date",
  TEACHER_NOTIFICATIONS: "ep:bell",
  TEACHER_SETTINGS: "ep:setting",

  // Student Module
  STUDENT_DASHBOARD: "ep:data-analysis",
  STUDENT_ENROLLMENTS: "ep:document-add",
  STUDENT_CLASSES: "ep:collection",
  STUDENT_GRADES: "ep:document",
  STUDENT_SCHEDULE: "ep:calendar",
  STUDENT_ATTENDANCE: "ep:check",
  STUDENT_CALENDAR: "ep:date",
  STUDENT_NOTIFICATIONS: "ep:bell",
  STUDENT_SETTINGS: "ep:setting",

  // HR Admin Module
  HR_ADMIN_DASHBOARD: "ep:data-analysis",
  HR_EMPLOYEES: "ep:user",
  HR_EMPLOYEE_ACCOUNTS: "ep:management",
  HR_EMPLOYEE_ARCHIVED: "ep:delete",
  HR_ATTENDANCE: "ep:check",
  HR_ATTENDANCE_WRONG_LOCATION: "ep:warning-filled",
  HR_ATTENDANCE_ADJUSTMENTS: "ep:edit",
  HR_ATTENDANCE_REPORTS: "ep:document",
  HR_OVERTIME: "ep:timer",
  HR_OVERTIME_REVIEWS: "ep:document-checked",
  HR_OVERTIME_HISTORY: "ep:history",
  HR_LEAVES: "ep:calendar",
  HR_LEAVE_REVIEWS: "ep:document-checked",
  HR_LEAVE_BALANCES: "ep:coin",
  HR_PAYROLL_RUNS: "ep:coin",
  HR_PAYROLL_GENERATE: "ep:document-add",
  HR_PAYSLIPS: "ep:document",
  HR_PAYROLL_HISTORY: "ep:history",
  HR_WORKING_SCHEDULES: "ep:calendar",
  HR_WORK_LOCATIONS: "ep:location",
  HR_PUBLIC_HOLIDAYS: "ep:date",
  HR_DEDUCTION_RULES: "ep:setting",
  HR_OVERTIME_RULES: "ep:setting",
  HR_REPORTS_ATTENDANCE: "ep:document",
  HR_REPORTS_OVERTIME: "ep:document",
  HR_REPORTS_PAYROLL: "ep:document",
  HR_REPORTS_WRONG_LOCATION: "ep:document",
  HR_SETTINGS: "ep:setting",

  // Employee Module
  EMPLOYEE_DASHBOARD: "ep:data-analysis",
  EMPLOYEE_PROFILE: "ep:user",
  EMPLOYEE_ATTENDANCE_CHECK: "ep:check",
  EMPLOYEE_ATTENDANCE_HISTORY: "ep:history",
  EMPLOYEE_OVERTIME_REQUEST: "ep:document-add",
  EMPLOYEE_OVERTIME_HISTORY: "ep:history",
  EMPLOYEE_LEAVE_REQUEST: "ep:document-add",
  EMPLOYEE_LEAVE_HISTORY: "ep:history",
  EMPLOYEE_LEAVE_BALANCE: "ep:coin",
  EMPLOYEE_PAYSLIPS: "ep:document",
  EMPLOYEE_SETTINGS: "ep:setting",

  // Manager Module
  MANAGER_DASHBOARD: "ep:data-analysis",
  MANAGER_ATTENDANCE_TEAM: "ep:check",
  MANAGER_ATTENDANCE_REPORTS: "ep:document",
  MANAGER_OVERTIME_REVIEWS: "ep:document-checked",
  MANAGER_OVERTIME_HISTORY: "ep:history",
  MANAGER_LEAVE_REVIEWS: "ep:document-checked",
  MANAGER_LEAVE_HISTORY: "ep:history",
  MANAGER_REPORTS_TEAM: "ep:document",
  MANAGER_SETTINGS: "ep:setting",

  // Payroll Manager Module
  PAYROLL_DASHBOARD: "ep:data-analysis",
  PAYROLL_PROCESS: "ep:document-add",
  PAYROLL_RUNS: "ep:coin",
  PAYROLL_PAYSLIPS: "ep:document",
  PAYROLL_ATTENDANCE: "ep:check",
  PAYROLL_OVERTIME: "ep:timer",
  PAYROLL_REPORTS: "ep:document",
  PAYROLL_SETTINGS: "ep:setting",
} as const;

/**
 * Icon mappings by module for easier navigation organization
 */
export const NAVIGATION_STRUCTURE = {
  admin: {
    icon: ICONS.ADMIN_DASHBOARD,
    items: [
      { key: "dashboard", icon: ICONS.ADMIN_DASHBOARD },
      { key: "users", icon: ICONS.ADMIN_USERS },
      { key: "classes", icon: ICONS.ADMIN_CLASSES },
      { key: "subjects", icon: ICONS.ADMIN_SUBJECTS },
      { key: "schedules", icon: ICONS.ADMIN_SCHEDULES },
      { key: "teachingAssignments", icon: ICONS.ADMIN_TEACHING_ASSIGNMENTS },
      { key: "notifications", icon: ICONS.ADMIN_NOTIFICATIONS },
      { key: "events", icon: ICONS.ADMIN_EVENTS },
      { key: "settings", icon: ICONS.ADMIN_SETTINGS },
    ],
  },
  teacher: {
    icon: ICONS.TEACHER_DASHBOARD,
    items: [
      { key: "dashboard", icon: ICONS.TEACHER_DASHBOARD },
      { key: "students", icon: ICONS.TEACHER_STUDENTS },
      { key: "classes", icon: ICONS.TEACHER_CLASSES },
      { key: "grades", icon: ICONS.TEACHER_GRADES },
      { key: "schedule", icon: ICONS.TEACHER_SCHEDULE },
      { key: "attendance", icon: ICONS.TEACHER_ATTENDANCE },
      { key: "calendar", icon: ICONS.TEACHER_CALENDAR },
      { key: "notifications", icon: ICONS.TEACHER_NOTIFICATIONS },
      { key: "settings", icon: ICONS.TEACHER_SETTINGS },
    ],
  },
  student: {
    icon: ICONS.STUDENT_DASHBOARD,
    items: [
      { key: "dashboard", icon: ICONS.STUDENT_DASHBOARD },
      { key: "enrollments", icon: ICONS.STUDENT_ENROLLMENTS },
      { key: "classes", icon: ICONS.STUDENT_CLASSES },
      { key: "grades", icon: ICONS.STUDENT_GRADES },
      { key: "schedule", icon: ICONS.STUDENT_SCHEDULE },
      { key: "attendance", icon: ICONS.STUDENT_ATTENDANCE },
      { key: "calendar", icon: ICONS.STUDENT_CALENDAR },
      { key: "notifications", icon: ICONS.STUDENT_NOTIFICATIONS },
      { key: "settings", icon: ICONS.STUDENT_SETTINGS },
    ],
  },
  hrAdmin: {
    icon: ICONS.HR_ADMIN_DASHBOARD,
    items: [
      { key: "dashboard", icon: ICONS.HR_ADMIN_DASHBOARD },
      { key: "employees", icon: ICONS.HR_EMPLOYEES },
      { key: "attendance", icon: ICONS.HR_ATTENDANCE },
      { key: "overtime", icon: ICONS.HR_OVERTIME },
      { key: "leaves", icon: ICONS.HR_LEAVES },
      { key: "payroll", icon: ICONS.HR_PAYROLL_RUNS },
      { key: "settings", icon: ICONS.HR_SETTINGS },
    ],
  },
  employee: {
    icon: ICONS.EMPLOYEE_DASHBOARD,
    items: [
      { key: "dashboard", icon: ICONS.EMPLOYEE_DASHBOARD },
      { key: "attendance", icon: ICONS.EMPLOYEE_ATTENDANCE_CHECK },
      { key: "overtime", icon: ICONS.EMPLOYEE_OVERTIME_REQUEST },
      { key: "leaves", icon: ICONS.EMPLOYEE_LEAVE_REQUEST },
      { key: "payslips", icon: ICONS.EMPLOYEE_PAYSLIPS },
      { key: "settings", icon: ICONS.EMPLOYEE_SETTINGS },
    ],
  },
  manager: {
    icon: ICONS.MANAGER_DASHBOARD,
    items: [
      { key: "dashboard", icon: ICONS.MANAGER_DASHBOARD },
      { key: "attendance", icon: ICONS.MANAGER_ATTENDANCE_TEAM },
      { key: "overtime", icon: ICONS.MANAGER_OVERTIME_REVIEWS },
      { key: "leaves", icon: ICONS.MANAGER_LEAVE_REVIEWS },
      { key: "reports", icon: ICONS.MANAGER_REPORTS_TEAM },
      { key: "settings", icon: ICONS.MANAGER_SETTINGS },
    ],
  },
  payrollManager: {
    icon: ICONS.PAYROLL_DASHBOARD,
    items: [
      { key: "dashboard", icon: ICONS.PAYROLL_DASHBOARD },
      { key: "payroll", icon: ICONS.PAYROLL_RUNS },
      { key: "payslips", icon: ICONS.PAYROLL_PAYSLIPS },
      { key: "reports", icon: ICONS.PAYROLL_REPORTS },
      { key: "settings", icon: ICONS.PAYROLL_SETTINGS },
    ],
  },
} as const;
