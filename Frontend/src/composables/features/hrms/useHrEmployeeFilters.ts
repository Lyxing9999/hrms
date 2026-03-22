import { ref, computed } from "vue";

export function useHrEmployeeFilters() {
  const q = ref("");
  const hasAccount = ref<"" | "yes" | "no">("");
  const employeeStatus = ref<"" | "active" | "inactive">("");

  const searchModel = computed<string>({
    get: () => q.value,
    set: (v) => (q.value = v),
  });

  const filters = computed(() => ({
    q: q.value.trim(),
    hasAccount: hasAccount.value || undefined,
    status: employeeStatus.value || undefined,
  }));

  const isDirty = computed(() => {
    return !!q.value.trim() || !!hasAccount.value || !!employeeStatus.value;
  });

  function resetAll() {
    q.value = "";
    hasAccount.value = "";
    employeeStatus.value = "";
  }

  return {
    q,
    hasAccount,
    employeeStatus,
    searchModel,
    filters,
    isDirty,
    resetAll,
  };
}
