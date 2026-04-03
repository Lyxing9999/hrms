<script setup lang="ts">
import { Calendar, Document, Money } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  {
    label: "Attendance Batch",
    value: "Final",
    hint: "Locked input for payroll",
  },
  { label: "Records", value: "142", hint: "Demo employee count" },
  { label: "Adjustments", value: "3", hint: "Manual corrections" },
  { label: "Export", value: "Ready", hint: "Payroll handoff available" },
];

const actions = [
  {
    title: "Generate Payroll",
    description: "Proceed to the payroll generation flow.",
    route: ROUTES.PAYROLL_MANAGER.PAYROLL_PROCESS,
    icon: Money,
    color: "#0f766e",
  },
  {
    title: "Payroll Runs",
    description: "Inspect existing payroll batches.",
    route: ROUTES.PAYROLL_MANAGER.PAYROLL_RUNS,
    icon: Document,
    color: "#2563eb",
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
    title: "Finalization steps",
    items: [
      "lock attendance",
      "apply adjustments",
      "export to payroll",
      "confirm totals",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Final Attendance"
    description="Prototype final attendance page used by payroll to finalize the monthly batch."
    back-path="/payroll/dashboard"
    badge="Attendance"
    accent="#0f766e"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
