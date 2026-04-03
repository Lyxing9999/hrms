<script setup lang="ts">
import { Document, Timer } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  {
    label: "Review Queue",
    value: "5 Items",
    hint: "Pending manager approvals",
  },
  { label: "Avg Hours", value: "3.5h", hint: "Prototype average request" },
  { label: "Approved Rate", value: "78%", hint: "Demo approval ratio" },
  { label: "Rejected Rate", value: "22%", hint: "Demo rejection ratio" },
];

const actions = [
  {
    title: "OT History",
    description: "Check older overtime decisions.",
    route: ROUTES.MANAGER.OVERTIME_HISTORY,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Team Attendance",
    description: "Compare overtime with attendance records.",
    route: ROUTES.MANAGER.ATTENDANCE_TEAM,
    icon: Timer,
    color: "#0f766e",
  },
  {
    title: "Leave Reviews",
    description: "Jump to leave review queues.",
    route: ROUTES.MANAGER.LEAVE_REVIEWS,
    icon: Document,
    color: "#16a34a",
  },
];

const sections = [
  {
    title: "Review checklist",
    items: [
      "hours requested",
      "manager comment",
      "approval state",
      "payroll handoff",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Overtime Reviews"
    description="Prototype review page for manager overtime approvals and rejections."
    back-path="/manager/overtime"
    badge="Review Queue"
    accent="#2563eb"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
