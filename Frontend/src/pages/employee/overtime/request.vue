<script setup lang="ts">
import { Timer, Calendar, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Form State", value: "Ready", hint: "Request demo form" },
  {
    label: "Approval Path",
    value: "Manager",
    hint: "Manager or HR admin review",
  },
  { label: "Policy", value: "24h Notice", hint: "Use the prototype guidance" },
  { label: "Status", value: "Draft", hint: "Not connected to submit yet" },
];

const actions = [
  {
    title: "History",
    description: "Inspect previous overtime requests.",
    route: ROUTES.EMPLOYEE.OVERTIME_HISTORY,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Check In",
    description: "Return to the attendance flow when needed.",
    route: ROUTES.EMPLOYEE.ATTENDANCE_CHECK,
    icon: Calendar,
    color: "#0f766e",
  },
  {
    title: "Leave Requests",
    description: "Go to the leave request prototype page.",
    route: ROUTES.EMPLOYEE.LEAVE_REQUEST,
    icon: Timer,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "Expected fields",
    items: [
      "Request date",
      "Start and end time",
      "Reason for overtime",
      "Optional notes for the reviewer",
    ],
  },
  {
    title: "Backend endpoint",
    items: ["POST /api/hrms/overtime-requests"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Request Overtime"
    description="Demo request page for the employee overtime workflow. Use it as a prototype for the backend overtime request endpoint."
    back-path="/employee/overtime"
    badge="Request Form"
    accent="#d97706"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
