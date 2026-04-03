<script setup lang="ts">
import { Calendar, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "History Rows", value: "19", hint: "Prototype leave history" },
  { label: "Approved", value: "15", hint: "Approved leave requests" },
  { label: "Pending", value: "4", hint: "Waiting for review" },
  { label: "Balance", value: "12 Days", hint: "Demo balance reference" },
];

const actions = [
  {
    title: "Leave Reviews",
    description: "Return to the review queue.",
    route: ROUTES.MANAGER.LEAVE_REVIEWS,
    icon: Calendar,
    color: "#16a34a",
  },
  {
    title: "Team Attendance",
    description: "Check attendance alongside leave usage.",
    route: ROUTES.MANAGER.ATTENDANCE_TEAM,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Team Reports",
    description: "Open the reporting hub.",
    route: ROUTES.MANAGER.REPORTS_TEAM,
    icon: Document,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "History columns",
    items: ["employee", "leave type", "date range", "decision"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Leave History"
    description="Prototype leave history page for managers."
    back-path="/manager/leaves"
    badge="History"
    accent="#2563eb"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
