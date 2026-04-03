<script setup lang="ts">
import { Document, UserFilled } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Team Members", value: "18", hint: "Demo team size" },
  { label: "Present", value: "14", hint: "Attendance status snapshot" },
  { label: "Late", value: "2", hint: "Late arrivals today" },
  { label: "Absent", value: "2", hint: "Missing check-ins" },
];

const actions = [
  {
    title: "Attendance Reports",
    description: "Open the team attendance reporting page.",
    route: ROUTES.MANAGER.ATTENDANCE_REPORTS,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "OT Reviews",
    description: "Review overtime requests for the team.",
    route: ROUTES.MANAGER.OVERTIME_REVIEWS,
    icon: UserFilled,
    color: "#d97706",
  },
  {
    title: "Leave Reviews",
    description: "Review team leave requests and comments.",
    route: ROUTES.MANAGER.LEAVE_REVIEWS,
    icon: Document,
    color: "#16a34a",
  },
];

const sections = [
  {
    title: "Team attendance view",
    items: [
      "Today status",
      "Late arrivals",
      "Check-in times",
      "Missing records",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Team Attendance"
    description="Prototype attendance view for managers. It mirrors the team-attendance backend surface."
    back-path="/manager/dashboard"
    badge="Attendance"
    accent="#2563eb"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
