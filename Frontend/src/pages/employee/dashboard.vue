<script setup lang="ts">
import {
  Calendar,
  Clock,
  Document,
  User,
  Timer,
  Wallet,
} from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  {
    label: "Attendance Status",
    value: "Ready",
    hint: "Check-in and checkout flows are live",
  },
  { label: "Leave Balance", value: "12 Days", hint: "Prototype value only" },
  {
    label: "Overtime Requests",
    value: "3 Pending",
    hint: "Matches the overtime module",
  },
  {
    label: "Payslips",
    value: "Latest Ready",
    hint: "Payroll demo route available",
  },
];

const actions = [
  {
    title: "Check In",
    description:
      "Open the attendance flow built on the HRMS attendance endpoints.",
    route: ROUTES.EMPLOYEE.ATTENDANCE_CHECK,
    icon: Clock,
    color: "#0f766e",
  },
  {
    title: "Attendance History",
    description: "Review the current month and historical records.",
    route: ROUTES.EMPLOYEE.ATTENDANCE_HISTORY,
    icon: Calendar,
    color: "#2563eb",
  },
  {
    title: "Overtime",
    description: "Request or review overtime time entries.",
    route: ROUTES.EMPLOYEE.OVERTIME_REQUEST,
    icon: Timer,
    color: "#d97706",
  },
  {
    title: "Leave Requests",
    description: "Create or track leave requests from the employee workspace.",
    route: ROUTES.EMPLOYEE.LEAVE_REQUEST,
    icon: Document,
    color: "#16a34a",
  },
  {
    title: "Profile",
    description: "Open the employee profile and linked account summary.",
    route: ROUTES.EMPLOYEE.PROFILE,
    icon: User,
    color: "#7c3aed",
  },
  {
    title: "Payslips",
    description: "View payroll output generated for the employee role.",
    route: ROUTES.EMPLOYEE.PAYSLIPS,
    icon: Wallet,
    color: "#475569",
  },
];

const sections = [
  {
    title: "Backend surfaces",
    items: [
      "Attendance: check-in, check-out, history, wrong-location handling",
      "Overtime: request, cancel, and history views",
      "Leave: request, history, and balance demo pages",
      "Payroll: payslip viewing route",
    ],
    note: "Maps to the HRMS employee-facing services",
  },
  {
    title: "Suggested role flow",
    items: [
      "Start from check-in",
      "Review attendance history",
      "Request overtime or leave when needed",
      "Check payslips after payroll processing",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Employee Workspace"
    description="Prototype hub for the employee role, aligned to attendance, overtime, leave, and payroll surfaces from the backend HRMS module."
    badge="Employee Prototype"
    accent="#0f766e"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
<style>
.info-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  margin: 0;
}

.mt-6 {
  margin-top: 24px;
}

@media (max-width: 768px) {
  .welcome-title {
    font-size: 28px;
  }

  .welcome-subtitle {
    font-size: 16px;
  }

  .section-title {
    font-size: 20px;
  }
}
</style>
