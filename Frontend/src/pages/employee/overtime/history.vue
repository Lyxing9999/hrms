<script setup lang="ts">
import { Clock, Document, Timer } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Total Requests", value: "12", hint: "Prototype history total" },
  { label: "Approved", value: "8", hint: "Approved overtime records" },
  { label: "Rejected", value: "2", hint: "Rejected by manager" },
  { label: "Cancelled", value: "2", hint: "Employee cancel flow" },
];

const actions = [
  {
    title: "Request Overtime",
    description: "Open a new overtime request.",
    route: ROUTES.EMPLOYEE.OVERTIME_REQUEST,
    icon: Timer,
    color: "#0f766e",
  },
  {
    title: "Attendance History",
    description: "Compare attendance records with overtime entries.",
    route: ROUTES.EMPLOYEE.ATTENDANCE_HISTORY,
    icon: Clock,
    color: "#2563eb",
  },
  {
    title: "Payslips",
    description: "See how the approved overtime feeds payroll.",
    route: ROUTES.EMPLOYEE.PAYSLIPS,
    icon: Document,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "History columns",
    items: ["Date", "Hours requested", "Approval status", "Reviewer comment"],
  },
  {
    title: "Backend endpoints",
    items: [
      "GET /api/hrms/overtime-requests/my",
      "GET /api/hrms/overtime-requests/:id",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Overtime History"
    description="Demo history page for employee overtime records, aligned to the backend overtime query endpoints."
    back-path="/employee/overtime"
    badge="History"
    accent="#2563eb"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
