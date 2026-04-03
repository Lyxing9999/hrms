<script setup lang="ts">
import { Calendar, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Records", value: "21", hint: "Prototype overtime history" },
  { label: "Approved", value: "18", hint: "Accepted entries" },
  { label: "Rejected", value: "2", hint: "Rejected entries" },
  { label: "Cancelled", value: "1", hint: "Employee cancelled" },
];

const actions = [
  {
    title: "OT Reviews",
    description: "Go back to the approval queue.",
    route: ROUTES.MANAGER.OVERTIME_REVIEWS,
    icon: Calendar,
    color: "#d97706",
  },
  {
    title: "Team Attendance",
    description: "Inspect attendance timing around overtime.",
    route: ROUTES.MANAGER.ATTENDANCE_TEAM,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Payroll Reports",
    description: "Move into payroll reporting screens.",
    route: ROUTES.PAYROLL_MANAGER.REPORTS_PAYROLL,
    icon: Document,
    color: "#7c3aed",
  },
];

const sections = [
  {
    title: "History columns",
    items: ["employee", "hours", "decision", "review note"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Overtime History"
    description="Prototype history page for manager overtime records."
    back-path="/manager/overtime"
    badge="History"
    accent="#0f766e"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
