import { computed, type Ref } from "vue";
import { useHeaderState } from "~/composables/ui/useHeaderState";

export function useHrEmployeeHeaderStats(
  totalRows: Ref<number>,
  rowsWithAccount: Ref<number>,
) {
  const totalEmployees = computed(() => totalRows.value ?? 0);

  return useHeaderState({
    items: [
      {
        key: "employees",
        getValue: () => totalEmployees.value,
        singular: "employee",
        plural: "employees",
        variant: "primary",
        hideWhenZero: false,
      },
      {
        key: "accounts",
        getValue: () => rowsWithAccount.value,
        singular: "linked account",
        plural: "linked accounts",
        variant: "secondary",
        hideWhenZero: false,
      },
    ],
  });
}
