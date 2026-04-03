<script setup lang="ts">
import { Document, Timer } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  {
    label: "Requests",
    value: "Demo Hub",
    hint: "Start or review overtime routes",
  },
  { label: "Pending", value: "2", hint: "Prototype queue count" },
  { label: "Approved", value: "8", hint: "History sample value" },
  { label: "Cancelled", value: "1", hint: "Cancel flow included" },
];

const actions = [
  {
    title: "Request Overtime",
    description: "Open the overtime request page.",
    route: ROUTES.EMPLOYEE.OVERTIME_REQUEST,
    icon: Timer,
    color: "#0f766e",
  },
  {
    title: "Overtime History",
    description: "Review my overtime request history.",
    route: ROUTES.EMPLOYEE.OVERTIME_HISTORY,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Payslips",
    description: "See how approved overtime feeds payroll.",
    route: ROUTES.EMPLOYEE.PAYSLIPS,
    icon: Document,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "Backend actions",
    items: [
      "create overtime request",
      "cancel overtime request",
      "list my overtime requests",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Employee Overtime"
    description="Prototype hub for the employee overtime flow. The routes mirror the backend overtime request lifecycle."
    back-path="/employee/dashboard"
    badge="Overtime Hub"
    accent="#0f766e"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
