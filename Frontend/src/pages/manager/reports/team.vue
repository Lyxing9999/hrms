<script setup lang="ts">
import { Calendar, Document, UserFilled } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Team KPI", value: "92%", hint: "Prototype summary" },
  { label: "Attendance", value: "Live", hint: "Attendance aggregate" },
  { label: "Overtime", value: "Tracked", hint: "Overtime aggregate" },
  { label: "Leaves", value: "Tracked", hint: "Leave aggregate" },
];

const actions = [
  {
    title: "Team Attendance",
    description: "Open attendance details for the team.",
    route: ROUTES.MANAGER.ATTENDANCE_TEAM,
    icon: UserFilled,
    color: "#2563eb",
  },
  {
    title: "OT Reviews",
    description: "Inspect overtime review queues.",
    route: ROUTES.MANAGER.OVERTIME_REVIEWS,
    icon: Calendar,
    color: "#d97706",
  },
  {
    title: "Leave Reviews",
    description: "Inspect leave approval queues.",
    route: ROUTES.MANAGER.LEAVE_REVIEWS,
    icon: Document,
    color: "#16a34a",
  },
];

const sections = [
  {
    title: "Report rows",
    items: ["attendance rate", "late count", "overtime hours", "leave days"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Team Reports"
    description="Prototype reporting hub for managers to review team health and HR summary metrics."
    back-path="/manager/dashboard"
    badge="Reports"
    accent="#7c3aed"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
