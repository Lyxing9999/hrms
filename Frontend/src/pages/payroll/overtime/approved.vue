<script setup lang="ts">
import { Calendar, Document, Money } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Approved OT", value: "38h", hint: "Included in payroll" },
  { label: "Employees", value: "11", hint: "Have approved OT" },
  { label: "Rejected", value: "2", hint: "Not included" },
  { label: "Total Impact", value: "$1,240", hint: "Prototype amount" },
];

const actions = [
  {
    title: "Generate Payroll",
    description: "Continue to payroll generation.",
    route: ROUTES.PAYROLL_MANAGER.PAYROLL_GENERATE,
    icon: Money,
    color: "#0f766e",
  },
  {
    title: "Payroll Runs",
    description: "Inspect the current payroll batch list.",
    route: ROUTES.PAYROLL_MANAGER.PAYROLL_RUNS,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Attendance Final",
    description: "Cross-check the source attendance data.",
    route: ROUTES.PAYROLL_MANAGER.ATTENDANCE_FINAL,
    icon: Calendar,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "Approved overtime fields",
    items: ["employee", "hours", "approval date", "pay impact"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Approved Overtime"
    description="Prototype page for overtime items that are approved and ready for payroll inclusion."
    back-path="/payroll/dashboard"
    badge="Approved OT"
    accent="#d97706"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
