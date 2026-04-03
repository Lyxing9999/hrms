<script setup lang="ts">
import { Document, Timer } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Pending Approvals", value: "5", hint: "Prototype review queue" },
  { label: "Approved", value: "18", hint: "Monthly overtime total" },
  { label: "Rejected", value: "2", hint: "Demo count" },
  { label: "History", value: "Visible", hint: "Audit trail available" },
];

const actions = [
  {
    title: "OT Reviews",
    description: "Open the overtime approval queue.",
    route: ROUTES.MANAGER.OVERTIME_REVIEWS,
    icon: Timer,
    color: "#d97706",
  },
  {
    title: "OT History",
    description: "Inspect past overtime decisions.",
    route: ROUTES.MANAGER.OVERTIME_HISTORY,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Team Leave",
    description: "Switch to the leave review workflow.",
    route: ROUTES.MANAGER.LEAVE_REVIEWS,
    icon: Document,
    color: "#16a34a",
  },
];

const sections = [
  {
    title: "Backend actions",
    items: [
      "approve overtime request",
      "reject overtime request",
      "list overtime requests",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Manager Overtime"
    description="Prototype hub for manager overtime workflows and approvals."
    back-path="/manager/dashboard"
    badge="Overtime Hub"
    accent="#d97706"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
