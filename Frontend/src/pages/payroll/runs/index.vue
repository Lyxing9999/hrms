<script setup lang="ts">
import { Calendar, Document, Money } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Runs", value: "6", hint: "Prototype payroll batches" },
  { label: "Draft", value: "1", hint: "Current working batch" },
  { label: "Completed", value: "5", hint: "Closed payroll cycles" },
  { label: "Payslips", value: "Ready", hint: "Run output visible" },
];

const actions = [
  {
    title: "Generate Payroll",
    description: "Open the payroll generation flow.",
    route: ROUTES.PAYROLL_MANAGER.PAYROLL_PROCESS,
    icon: Money,
    color: "#0f766e",
  },
  {
    title: "Payslips",
    description: "Inspect employee payslip output.",
    route: ROUTES.PAYROLL_MANAGER.PAYSLIPS,
    icon: Document,
    color: "#2563eb",
  },
  {
    title: "Payroll Reports",
    description: "Open the reporting dashboard.",
    route: ROUTES.PAYROLL_MANAGER.REPORTS_PAYROLL,
    icon: Calendar,
    color: "#d97706",
  },
];

const sections = [
  {
    title: "Run lifecycle",
    items: ["draft", "calculated", "reviewed", "published"],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Payroll Runs"
    description="Prototype list view for payroll run history and status tracking."
    back-path="/payroll/dashboard"
    badge="Runs"
    accent="#0f766e"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
