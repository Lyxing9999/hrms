<script setup lang="ts">
import { Calendar, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Requests", value: "9", hint: "Prototype leave history" },
  { label: "Approved", value: "8", hint: "Approved leave items" },
  { label: "Pending", value: "1", hint: "Waiting for review" },
  { label: "Balance", value: "12 Days", hint: "Remaining leave balance" },
];

const actions = [
  {
    title: "Request Leave",
    description: "Create another leave request.",
    route: ROUTES.EMPLOYEE.LEAVE_REQUEST,
    icon: Calendar,
    color: "#16a34a",
  },
  {
    title: "Leave Balance",
    description: "Open the balance summary page.",
    route: ROUTES.EMPLOYEE.LEAVE_BALANCE,
    icon: Document,
    color: "#d97706",
  },
  {
    title: "Payslips",
    description: "Cross-reference payroll output with leave history.",
    route: ROUTES.EMPLOYEE.PAYSLIPS,
    icon: Document,
    color: "#2563eb",
  },
];

const sections = [
  {
    title: "History columns",
    items: ["Leave type", "Date range", "Approval state", "Reviewer comment"],
  },
  {
    title: "Backend endpoint",
    items: ["Leave history query and approval lifecycle"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Leave History"
    description="Prototype history page for employee leave requests and approvals."
    back-path="/employee/leaves"
    badge="History"
    accent="#2563eb"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
