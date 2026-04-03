<script setup lang="ts">
import { Calendar, Document, Timer, UserFilled } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  {
    label: "Team Attendance",
    value: "Live",
    hint: "Review team check-ins and status",
  },
  {
    label: "OT Reviews",
    value: "Ready",
    hint: "Approve or reject overtime requests",
  },
  {
    label: "Leave Reviews",
    value: "Ready",
    hint: "Track team leave approvals",
  },
  {
    label: "Reports",
    value: "Team Summary",
    hint: "Demo analytics and summaries",
  },
];

const actions = [
  {
    title: "Team Attendance",
    description: "Open the team attendance view for managers.",
    route: ROUTES.MANAGER.ATTENDANCE_TEAM,
    icon: UserFilled,
    color: "#2563eb",
  },
  {
    title: "Attendance Reports",
    description: "Review status trends and reports for the team.",
    route: ROUTES.MANAGER.ATTENDANCE_REPORTS,
    icon: Calendar,
    color: "#0891b2",
  },
  {
    title: "OT Reviews",
    description: "Approve, reject, or inspect overtime records.",
    route: ROUTES.MANAGER.OVERTIME_REVIEWS,
    icon: Timer,
    color: "#d97706",
  },
  {
    title: "Leave Reviews",
    description: "Manage leave requests and team leave history.",
    route: ROUTES.MANAGER.LEAVE_REVIEWS,
    icon: Document,
    color: "#16a34a",
  },
  {
    title: "Team Reports",
    description: "Open the prototype team report hub.",
    route: ROUTES.MANAGER.REPORTS_TEAM,
    icon: Document,
    color: "#7c3aed",
  },
];

const sections = [
  {
    title: "Manager responsibilities",
    items: [
      "Monitor team attendance",
      "Review overtime approval queues",
      "Handle leave review decisions",
      "Use team reports for quick oversight",
    ],
  },
  {
    title: "Backend alignment",
    items: [
      "Attendance team and report endpoints",
      "Overtime approval and history endpoints",
      "Leave review and history endpoints",
    ],
    note: "The page is a prototype shell, but the routes match the HRMS role model",
  },
];
</script>

<template>
  <PrototypePageShell
    title="Manager Workspace"
    description="Demo workspace for team leads and line managers. The navigation mirrors the backend HRMS roles for attendance, overtime, leave, and reporting."
    badge="Manager Prototype"
    accent="#1d4ed8"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
