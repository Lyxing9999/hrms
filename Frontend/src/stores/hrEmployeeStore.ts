import { defineStore } from "pinia";
import { reactive, ref } from "vue";
import axios from "axios";
import { hrmsAdminService } from "~/api/hr_admin";
import type { EmployeeService } from "~/api/hr_admin/employees/service";
import type {
  HrCreateEmployeeAccountDTO,
  HrCreateEmployeeDTO,
  HrEmployeeDTO,
  HrEmployeeOnboardDTO,
  HrEmployeeWithAccountDTO,
} from "~/api/hr_admin/employees/dto";

type EmployeeAction =
  | "getEmployeesWithAccounts"
  | "getEmployee"
  | "getEmployeeAccount"
  | "createEmployee"
  | "updateEmployee"
  | "softDeleteEmployee"
  | "restoreEmployee"
  | "createAccount"
  | "onboardEmployee"
  | "softDeleteEmployeeAccount"
  | "restoreEmployeeAccount"
  | "getEmployeeAccounts"
  | "linkAccount"
  | "updateEmployeeAccount"
  | "requestEmployeeAccountPasswordReset"
  | "setEmployeeAccountStatus";

type ActionStatus = {
  loading: boolean;
  success: boolean;
  error: string | null;
  updatedAt: number | null;
};

type EmployeeActionStatusMap = Record<EmployeeAction, ActionStatus>;

type CreateEmployeeFlowStatus = {
  creatingEmployee: boolean;
  employeeCreated: boolean;
  createdEmployeeId: string | null;
  creatingAccount: boolean;
  accountCreated: boolean;
  createdAccountId: string | null;
  error: string | null;
  updatedAt: number | null;
};

type CreateEmployeeWithAccountResult = {
  employee: HrEmployeeDTO;
  account: HrEmployeeWithAccountDTO | null;
};

type CreateEmployeeWithAccountOptions = {
  employeeOptions?: Parameters<EmployeeService["createEmployee"]>[1];
  accountOptions?: Parameters<EmployeeService["createAccount"]>[2];
  onboardOptions?: Parameters<EmployeeService["onboardEmployee"]>[1];
};

function createDefaultStatusMap(): EmployeeActionStatusMap {
  const init = (): ActionStatus => ({
    loading: false,
    success: false,
    error: null,
    updatedAt: null,
  });

  return {
    getEmployeesWithAccounts: init(),
    getEmployee: init(),
    getEmployeeAccount: init(),
    createEmployee: init(),
    updateEmployee: init(),
    softDeleteEmployee: init(),
    restoreEmployee: init(),
    createAccount: init(),
    onboardEmployee: init(),
    softDeleteEmployeeAccount: init(),
    restoreEmployeeAccount: init(),
    getEmployeeAccounts: init(),
    linkAccount: init(),
    updateEmployeeAccount: init(),
    requestEmployeeAccountPasswordReset: init(),
    setEmployeeAccountStatus: init(),
  };
}

function createDefaultCreateFlowStatus(): CreateEmployeeFlowStatus {
  return {
    creatingEmployee: false,
    employeeCreated: false,
    createdEmployeeId: null,
    creatingAccount: false,
    accountCreated: false,
    createdAccountId: null,
    error: null,
    updatedAt: null,
  };
}

function toErrorMessage(error: unknown) {
  if (axios.isAxiosError(error)) {
    const apiMessage =
      (error.response?.data?.user_message as string | undefined) ||
      (error.response?.data?.message as string | undefined);
    if (apiMessage) return apiMessage;
  }

  if (error instanceof Error) return error.message;
  return "Unknown error";
}

export const useHrEmployeeStore = defineStore("hr-employee", () => {
  const service = hrmsAdminService().employee;
  const actionStatus = reactive<EmployeeActionStatusMap>(
    createDefaultStatusMap(),
  );
  const lastAction = ref<EmployeeAction | null>(null);
  const createFlowStatus = reactive<CreateEmployeeFlowStatus>(
    createDefaultCreateFlowStatus(),
  );

  async function runAction<T>(
    action: EmployeeAction,
    runner: () => Promise<T>,
  ): Promise<T> {
    const state = actionStatus[action];
    state.loading = true;
    state.success = false;
    state.error = null;
    lastAction.value = action;

    try {
      const data = await runner();
      state.success = true;
      state.updatedAt = Date.now();
      return data;
    } catch (error) {
      state.error = toErrorMessage(error);
      state.updatedAt = Date.now();
      throw error;
    } finally {
      state.loading = false;
    }
  }

  function clearAction(action: EmployeeAction) {
    actionStatus[action].loading = false;
    actionStatus[action].success = false;
    actionStatus[action].error = null;
    actionStatus[action].updatedAt = null;
  }

  function clearAllActions() {
    (Object.keys(actionStatus) as EmployeeAction[]).forEach((action) => {
      clearAction(action);
    });
  }

  function resetCreateFlowStatus() {
    Object.assign(createFlowStatus, createDefaultCreateFlowStatus());
  }

  function isLoading(action: EmployeeAction) {
    return actionStatus[action].loading;
  }

  function getError(action: EmployeeAction) {
    return actionStatus[action].error;
  }

  function isSuccess(action: EmployeeAction) {
    return actionStatus[action].success;
  }

  const getEmployeesWithAccounts: EmployeeService["getEmployeesWithAccounts"] =
    (...args) =>
      runAction("getEmployeesWithAccounts", () =>
        service.getEmployeesWithAccounts(...args),
      );

  const getEmployee: EmployeeService["getEmployee"] = (...args) =>
    runAction("getEmployee", () => service.getEmployee(...args));

  const getEmployeeAccount: EmployeeService["getEmployeeAccount"] = (...args) =>
    runAction("getEmployeeAccount", () => service.getEmployeeAccount(...args));

  const createEmployee: EmployeeService["createEmployee"] = (...args) =>
    runAction("createEmployee", () => service.createEmployee(...args));

  const updateEmployee: EmployeeService["updateEmployee"] = (...args) =>
    runAction("updateEmployee", () => service.updateEmployee(...args));

  const softDeleteEmployee: EmployeeService["softDeleteEmployee"] = (...args) =>
    runAction("softDeleteEmployee", () => service.softDeleteEmployee(...args));

  const restoreEmployee: EmployeeService["restoreEmployee"] = (...args) =>
    runAction("restoreEmployee", () => service.restoreEmployee(...args));

  const createAccount: EmployeeService["createAccount"] = (...args) =>
    runAction("createAccount", () => service.createAccount(...args));

  const onboardEmployee: EmployeeService["onboardEmployee"] = (...args) =>
    runAction("onboardEmployee", () => service.onboardEmployee(...args));

  async function createEmployeeWithAccount(
    employeePayload: HrCreateEmployeeDTO,
    accountPayload?: HrCreateEmployeeAccountDTO,
    options?: CreateEmployeeWithAccountOptions,
  ): Promise<CreateEmployeeWithAccountResult> {
    resetCreateFlowStatus();
    createFlowStatus.creatingEmployee = true;
    createFlowStatus.updatedAt = Date.now();

    try {
      if (accountPayload) {
        const onboardPayload: HrEmployeeOnboardDTO = {
          employee: employeePayload,
          email: accountPayload.email,
          password: accountPayload.password,
          username: accountPayload.username,
          role: String(accountPayload.role),
        };

        createFlowStatus.creatingAccount = true;
        const onboardResult = await onboardEmployee(
          onboardPayload,
          options?.onboardOptions,
        );

        createFlowStatus.creatingEmployee = false;
        createFlowStatus.creatingAccount = false;
        createFlowStatus.employeeCreated = true;
        createFlowStatus.accountCreated = true;
        createFlowStatus.createdEmployeeId = onboardResult.employee?.id ?? null;
        createFlowStatus.createdAccountId = onboardResult.user?.id ?? null;
        createFlowStatus.updatedAt = Date.now();

        return {
          employee: onboardResult.employee,
          account: onboardResult,
        };
      }

      const employee = await createEmployee(
        employeePayload,
        options?.employeeOptions,
      );

      createFlowStatus.creatingEmployee = false;
      createFlowStatus.employeeCreated = true;
      createFlowStatus.createdEmployeeId = employee.id;
      createFlowStatus.updatedAt = Date.now();

      return { employee, account: null };
    } catch (error) {
      createFlowStatus.error = toErrorMessage(error);
      createFlowStatus.updatedAt = Date.now();
      throw error;
    } finally {
      createFlowStatus.creatingEmployee = false;
      createFlowStatus.creatingAccount = false;
    }
  }

  const softDeleteEmployeeAccount: EmployeeService["softDeleteEmployeeAccount"] =
    (...args) =>
      runAction("softDeleteEmployeeAccount", () =>
        service.softDeleteEmployeeAccount(...args),
      );

  const restoreEmployeeAccount: EmployeeService["restoreEmployeeAccount"] = (
    ...args
  ) =>
    runAction("restoreEmployeeAccount", () =>
      service.restoreEmployeeAccount(...args),
    );

  const getEmployeeAccounts: EmployeeService["getEmployeeAccounts"] = (
    ...args
  ) =>
    runAction("getEmployeeAccounts", () =>
      service.getEmployeeAccounts(...args),
    );

  const linkAccount: EmployeeService["linkAccount"] = (...args) =>
    runAction("linkAccount", () => service.linkAccount(...args));

  const updateEmployeeAccount: EmployeeService["updateEmployeeAccount"] = (
    ...args
  ) =>
    runAction("updateEmployeeAccount", () =>
      service.updateEmployeeAccount(...args),
    );

  const requestEmployeeAccountPasswordReset: EmployeeService["requestEmployeeAccountPasswordReset"] =
    (...args) =>
      runAction("requestEmployeeAccountPasswordReset", () =>
        service.requestEmployeeAccountPasswordReset(...args),
      );

  const setEmployeeAccountStatus: EmployeeService["setEmployeeAccountStatus"] =
    (...args) =>
      runAction("setEmployeeAccountStatus", () =>
        service.setEmployeeAccountStatus(...args),
      );

  return {
    actionStatus,
    lastAction,
    createFlowStatus,
    clearAction,
    clearAllActions,
    resetCreateFlowStatus,
    isLoading,
    getError,
    isSuccess,
    getEmployeesWithAccounts,
    getEmployee,
    getEmployeeAccount,
    createEmployee,
    updateEmployee,
    softDeleteEmployee,
    restoreEmployee,
    createAccount,
    onboardEmployee,
    createEmployeeWithAccount,
    softDeleteEmployeeAccount,
    restoreEmployeeAccount,
    getEmployeeAccounts,
    linkAccount,
    updateEmployeeAccount,
    requestEmployeeAccountPasswordReset,
    setEmployeeAccountStatus,
  };
});
