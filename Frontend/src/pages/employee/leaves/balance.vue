<script setup lang="ts">
import { Calendar, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Available", value: "12 Days", hint: "Current leave balance" },
  { label: "Used", value: "8 Days", hint: "Consumed in this cycle" },
  { label: "Pending", value: "1 Day", hint: "Requested but not reviewed" },
  { label: "Carry Over", value: "2 Days", hint: "Prototype carry over value" },
];

const actions = [
  {
    title: "Request Leave",
    description: "Submit a new leave request.",
    route: ROUTES.EMPLOYEE.LEAVE_REQUEST,
    icon: Calendar,
    color: "#16a34a",
  },
  {
    title: "Leave History",
    description: "Review the request list and approvals.",
    route: ROUTES.EMPLOYEE.LEAVE_HISTORY,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Dashboard",
    description: "Return to the employee hub.",
    route: ROUTES.EMPLOYEE.DASHBOARD,
    icon: Document,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "Balance breakdown",
    items: ["Annual leave", "Sick leave", "Casual leave", "Carry-over leave"],
  },
  {
    title: "Prototype notes",
    items: ["This page is a demo view", "Balance values are static samples"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Leave Balance"
    description="Prototype balance view for the employee leave module."
    back-path="/employee/leaves"
    badge="Balance"
    accent="#d97706"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
