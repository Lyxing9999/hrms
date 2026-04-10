<script setup lang="ts">
import { Calendar, Money, Document } from "@element-plus/icons-vue";
import PrototypePageShell from "~/components/hrms/PrototypePageShell.vue";
import { ROUTES } from "~/constants/routes";

const stats = [
  { label: "Cycle", value: "Apr 2026", hint: "Selected payroll month" },
  {
    label: "Attendance Input",
    value: "Final",
    hint: "Uses finalized attendance",
  },
  { label: "OT Input", value: "Approved", hint: "Approved overtime included" },
  { label: "Output", value: "Draft Run", hint: "Preview before publish" },
];

const actions = [
  {
    title: "Run List",
    description: "Go back to the payroll run list.",
    route: ROUTES.PAYROLL_MANAGER.PAYROLL_RUNS,
    icon: Document,
    color: "var(--chart-6)",
  },
  {
    title: "Final Attendance",
    description: "Check the final attendance source.",
    route: ROUTES.PAYROLL_MANAGER.ATTENDANCE_FINAL,
    icon: Calendar,
    color: "var(--button-warning-bg)",
  },
  {
    title: "Approved OT",
    description: "Inspect overtime approvals for payroll.",
    route: ROUTES.PAYROLL_MANAGER.OVERTIME_APPROVED,
    icon: Money,
    color: "var(--button-success-bg)",
  },
];

const sections = [
  {
    title: "Generation inputs",
    items: [
      "pay period",
      "final attendance",
      "approved overtime",
      "deductions",
    ],
  },
];
</script>

<template>
  <PrototypePageShell
    title="Generate Payroll"
    description="Prototype payroll generation page for the payroll manager role."
    back-path="/payroll/runs"
    badge="Generate"
    accent="var(--button-success-bg)"
    :stats="stats"
    :actions="actions"
    :sections="sections"
  />
</template>
