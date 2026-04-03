<script setup lang="ts">
import { Calendar, Document, Money } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Gross Payroll", value: "$240K", hint: "Prototype monthly figure" },
  { label: "Net Payroll", value: "$181K", hint: "After deductions" },
  {
    label: "Deductions",
    value: "$59K",
    hint: "Includes late and absence deductions",
  },
  { label: "Reports", value: "Ready", hint: "Summary routes available" },
];

const actions = [
  {
    title: "Payroll Runs",
    description: "Return to payroll run history.",
    route: ROUTES.PAYROLL_MANAGER.PAYROLL_RUNS,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Generate Payroll",
    description: "Open the payroll generation page.",
    route: ROUTES.PAYROLL_MANAGER.PAYROLL_PROCESS,
    icon: Money,
    color: "#0f766e",
  },
  {
    title: "Approved OT",
    description: "Review overtime included in payroll.",
    route: ROUTES.PAYROLL_MANAGER.OVERTIME_APPROVED,
    icon: Calendar,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "Report panels",
    items: ["gross payroll", "net payroll", "deductions", "payslip completion"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Payroll Reports"
    description="Prototype payroll reporting hub for month-end review and summary analysis."
    back-path="/payroll/dashboard"
    badge="Reports"
    accent="#2563eb"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
