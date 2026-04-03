<script setup lang="ts">
import { Calendar, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Review Queue", value: "4 Items", hint: "Pending leave requests" },
  { label: "Approved", value: "15", hint: "Accepted in this cycle" },
  { label: "Rejected", value: "1", hint: "Rejected leave request" },
  {
    label: "Balance",
    value: "Visible",
    hint: "Manager can inspect balance data",
  },
];

const actions = [
  {
    title: "Leave History",
    description: "Move to the team leave history page.",
    route: ROUTES.MANAGER.LEAVE_HISTORY,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Team Attendance",
    description: "Compare leave and attendance context.",
    route: ROUTES.MANAGER.ATTENDANCE_TEAM,
    icon: Calendar,
    color: "#0f766e",
  },
  {
    title: "OT Reviews",
    description: "Switch to overtime approvals.",
    route: ROUTES.MANAGER.OVERTIME_REVIEWS,
    icon: Document,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "Review checklist",
    items: ["leave type", "date range", "comment", "decision"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Leave Reviews"
    description="Prototype leave approval page for managers."
    back-path="/manager/leaves"
    badge="Review Queue"
    accent="#0f766e"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
