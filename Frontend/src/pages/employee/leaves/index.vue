<script setup lang="ts">
import { Calendar, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Balance", value: "12 Days", hint: "Demo leave balance" },
  { label: "Pending", value: "1", hint: "Pending approval count" },
  { label: "Approved", value: "6", hint: "Approved leave history" },
  { label: "Rejected", value: "0", hint: "No rejected records" },
];

const actions = [
  {
    title: "Request Leave",
    description: "Create a new leave request.",
    route: ROUTES.EMPLOYEE.LEAVE_REQUEST,
    icon: Calendar,
    color: "#16a34a",
  },
  {
    title: "Leave History",
    description: "Review past leave requests and decisions.",
    route: ROUTES.EMPLOYEE.LEAVE_HISTORY,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Leave Balance",
    description: "Check remaining leave balance details.",
    route: ROUTES.EMPLOYEE.LEAVE_BALANCE,
    icon: Document,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "Backend actions",
    items: [
      "submit leave request",
      "approve leave request",
      "list leave requests",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Employee Leave"
    description="Prototype leave hub for employees. It mirrors the backend leave request and approval workflow."
    back-path="/employee/dashboard"
    badge="Leave Hub"
    accent="#16a34a"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
