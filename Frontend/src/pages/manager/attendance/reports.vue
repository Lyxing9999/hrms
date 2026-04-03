<script setup lang="ts">
import { Calendar, Document, UserFilled } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Attendance Rate", value: "92%", hint: "Prototype KPI" },
  { label: "Late Events", value: "12", hint: "Monthly summary" },
  { label: "Missing Punches", value: "3", hint: "Demo issue count" },
  { label: "Wrong Location", value: "1", hint: "Flagged attendance" },
];

const actions = [
  {
    title: "Team Attendance",
    description: "Return to the team attendance list.",
    route: ROUTES.MANAGER.ATTENDANCE_TEAM,
    icon: UserFilled,
    color: "#2563eb",
  },
  {
    title: "Leave Reviews",
    description: "Move to leave approvals and history.",
    route: ROUTES.MANAGER.LEAVE_REVIEWS,
    icon: Document,
    color: "#16a34a",
  },
  {
    title: "Reports Hub",
    description: "Open the team report landing page.",
    route: ROUTES.MANAGER.REPORTS_TEAM,
    icon: Calendar,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "Report axes",
    items: [
      "attendance rate",
      "late counts",
      "missing punches",
      "wrong-location events",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Attendance Reports"
    description="Prototype reporting page for managers, aligned to the team attendance reporting surface."
    back-path="/manager/dashboard"
    badge="Reports"
    accent="#0f766e"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
