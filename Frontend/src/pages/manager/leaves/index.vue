<script setup lang="ts">
import { Calendar, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Pending Leaves", value: "4", hint: "Prototype manager queue" },
  { label: "Approved", value: "15", hint: "Approved leave requests" },
  { label: "Rejected", value: "1", hint: "Rejected request sample" },
  { label: "History", value: "Visible", hint: "Review trail available" },
];

const actions = [
  {
    title: "Leave Reviews",
    description: "Open the leave approval queue.",
    route: ROUTES.MANAGER.LEAVE_REVIEWS,
    icon: Calendar,
    color: "#16a34a",
  },
  {
    title: "Leave History",
    description: "Inspect the team leave record list.",
    route: ROUTES.MANAGER.LEAVE_HISTORY,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Team Reports",
    description: "Review the team report hub.",
    route: ROUTES.MANAGER.REPORTS_TEAM,
    icon: Document,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "Backend actions",
    items: [
      "approve leave request",
      "submit leave request",
      "list leave history",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Manager Leave"
    description="Prototype hub for manager leave approvals and history."
    back-path="/manager/dashboard"
    badge="Leave Hub"
    accent="#16a34a"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
