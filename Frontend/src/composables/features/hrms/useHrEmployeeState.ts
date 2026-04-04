import { useHrEmployeeStore } from "~/stores/hrEmployeeStore";

export function useHrEmployeeState() {
  return useHrEmployeeStore();
}
