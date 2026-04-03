<script setup lang="ts">
import { Calendar, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Form State", value: "Ready", hint: "Leave request demo form" },
  { label: "Approval", value: "Manager", hint: "Manager review flow" },
  { label: "Balance Used", value: "0 Days", hint: "Prototype only" },
  { label: "Status", value: "Draft", hint: "Not connected to submit yet" },
];

const actions = [
  {
    title: "Leave History",
    description: "Review previous leave requests.",
    route: ROUTES.EMPLOYEE.LEAVE_HISTORY,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Leave Balance",
    description: "Open the balance overview page.",
    route: ROUTES.EMPLOYEE.LEAVE_BALANCE,
    icon: Document,
    color: "#d97706",
  },
  {
    title: "Attendance",
    description: "Go back to the attendance workspace.",
    route: ROUTES.EMPLOYEE.ATTENDANCE_CHECK,
    icon: Calendar,
    color: "#0f766e",
  },
];

const sections = [
  {
    title: "Expected fields",
    items: ["Leave type", "Start date", "End date", "Reason and notes"],
  },
  {
    title: "Backend endpoint",
    items: ["Submit leave request use case"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Request Leave"
    description="Demo leave request page for employees. Use it to prototype the employee leave submission flow."
    back-path="/employee/leaves"
    badge="Request Form"
    accent="#16a34a"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
