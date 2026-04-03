<script setup lang="ts">
import { User, Document, Calendar } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  {
    label: "Profile Status",
    value: "Complete",
    hint: "Prototype profile record",
  },
  { label: "Account Link", value: "Synced", hint: "Connected HRMS account" },
  { label: "Manager", value: "Assigned", hint: "Direct reporting line" },
  {
    label: "Documents",
    value: "3 Files",
    hint: "Demo attachments and contracts",
  },
];

const actions = [
  {
    title: "Attendance",
    description: "Go back to attendance and check-in flows.",
    route: ROUTES.EMPLOYEE.ATTENDANCE_CHECK,
    icon: Calendar,
    color: "#2563eb",
  },
  {
    title: "Payslips",
    description: "Open the payroll viewing page for this employee.",
    route: ROUTES.EMPLOYEE.PAYSLIPS,
    icon: Document,
    color: "#d97706",
  },
  {
    title: "Leave Request",
    description: "Create a leave request from the employee flow.",
    route: ROUTES.EMPLOYEE.LEAVE_REQUEST,
    icon: Document,
    color: "#16a34a",
  },
  {
    title: "Profile Summary",
    description: "Review the role setup and linked account state.",
    route: ROUTES.EMPLOYEE.PROFILE,
    icon: User,
    color: "#7c3aed",
  },
];

const sections = [
  {
    title: "Profile data points",
    items: [
      "Employee identity and contact details",
      "Linked IAM account status",
      "Assigned schedule and work location",
      "Document placeholders for contracts and IDs",
    ],
  },
  {
    title: "Backend relationship",
    items: [
      "Employee record",
      "Employee account summary",
      "Schedule assignment",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Employee Profile"
    description="Profile prototype for employee self-service. It mirrors the employee record and linked account shape from the backend HRMS domain."
    back-path="/employee/dashboard"
    badge="Employee Profile"
    accent="#7c3aed"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
