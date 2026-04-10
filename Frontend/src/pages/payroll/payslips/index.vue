<script setup lang="ts">
import { Calendar, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Generated", value: "142", hint: "Prototype payslip count" },
  { label: "Published", value: "Yes", hint: "Ready for employees" },
  { label: "Missing", value: "0", hint: "All employees covered" },
  { label: "Cycle", value: "Apr 2026", hint: "Current payslip month" },
];

const actions = [
  {
    title: "Payroll Runs",
    description: "Return to the run history view.",
    route: ROUTES.PAYROLL_MANAGER.PAYROLL_RUNS,
    icon: Calendar,
    color: "var(--chart-6)",
  },
  {
    title: "Generate Payroll",
    description: "Start or regenerate a payroll batch.",
    route: ROUTES.PAYROLL_MANAGER.PAYROLL_GENERATE,
    icon: Document,
    color: "var(--button-success-bg)",
  },
  {
    title: "Employee Payslips",
    description: "Open the employee-facing payslip view.",
    route: ROUTES.EMPLOYEE.PAYSLIPS,
    icon: Document,
    color: "var(--button-warning-bg)",
  },
];

const sections = [
  {
    title: "Publishing flow",
    items: [
      "generate run",
      "review output",
      "publish payslip",
      "employee visibility",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Payslips"
    description="Prototype payslip publishing page for payroll managers."
    back-path="/payroll/dashboard"
    badge="Payslips"
    accent="var(--chart-6)"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
