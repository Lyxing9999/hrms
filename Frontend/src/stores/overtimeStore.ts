import { defineStore } from "pinia";
import { ref, reactive, computed } from "vue";
import { hrmsAdminService } from "~/api/hr_admin";
import type {
  OvertimeRequestDTO,
  OvertimeRequestCreateDTO,
  OvertimeApproveDTO,
  OvertimeRejectDTO,
  OvertimeCancelDTO,
  MyOvertimeSummaryDTO,
  OvertimePayrollSummaryDTO,
  OvertimeRequestListResponseDTO,
} from "~/api/hr_admin/overtime/dto";

export type OvertimeAction =
  | "createRequest"
  | "approveRequest"
  | "rejectRequest"
  | "cancelRequest"
  | "getRequests"
  | "getMyRequests"
  | "getRequest"
  | "getPendingRequests"
  | "getMyOvertimeSummary"
  | "getPayrollApprovedRequests"
  | "getPayrollOvertimeSummary";

type ActionStatus = {
  loading: boolean;
  success: boolean;
  error: string | null;
  updatedAt: number | null;
};

type OvertimeActionStatusMap = Record<OvertimeAction, ActionStatus>;

function createDefaultStatusMap(): OvertimeActionStatusMap {
  const init = (): ActionStatus => ({
    loading: false,
    success: false,
    error: null,
    updatedAt: null,
  });

  return {
    createRequest: init(),
    approveRequest: init(),
    rejectRequest: init(),
    cancelRequest: init(),
    getRequests: init(),
    getMyRequests: init(),
    getRequest: init(),
    getPendingRequests: init(),
    getMyOvertimeSummary: init(),
    getPayrollApprovedRequests: init(),
    getPayrollOvertimeSummary: init(),
  };
}

export const useOvertimeStore = defineStore("overtime", () => {
  // State - List data
  const list = ref<OvertimeRequestDTO[]>([]);
  const myRequests = ref<OvertimeRequestDTO[]>([]);
  const pendingApproval = ref<OvertimeRequestDTO[]>([]);
  const payrollApproved = ref<OvertimeRequestDTO[]>([]);

  // State - Detail data
  const requestDetail = ref<OvertimeRequestDTO | null>(null);
  const mySummary = ref<MyOvertimeSummaryDTO | null>(null);
  const payrollSummary = ref<OvertimePayrollSummaryDTO | null>(null);

  // State - Pagination
  const pagination = reactive({
    page: 1,
    limit: 10,
    total: 0,
    totalPages: 0,
  });

  // State - Filters
  const filters = reactive({
    status: null as string | null,
    employee_id: null as string | null,
    start_date: null as string | null,
    end_date: null as string | null,
  });

  // State - Action status tracking
  const actionStatus = reactive<OvertimeActionStatusMap>(
    createDefaultStatusMap(),
  );

  /**
   * Get error message for a specific action
   */
  function getError(action: OvertimeAction): string | null {
    return actionStatus[action]?.error ?? null;
  }

  /**
   * Get loading state for a specific action
   */
  function isLoading(action: OvertimeAction): boolean {
    return actionStatus[action]?.loading ?? false;
  }

  /**
   * Set action status
   */
  function setActionStatus(
    action: OvertimeAction,
    status: Partial<ActionStatus>,
  ) {
    Object.assign(actionStatus[action], status);
  }

  function normalizeRequestDate(value: string): string {
    const trimmed = String(value ?? "").trim();
    if (/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) return trimmed;

    const parsed = new Date(trimmed);
    if (Number.isNaN(parsed.getTime())) {
      throw new Error("request_date must be a valid date in YYYY-MM-DD format");
    }

    const year = parsed.getFullYear();
    const month = String(parsed.getMonth() + 1).padStart(2, "0");
    const day = String(parsed.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  }

  function toCambodiaOffsetDateTime(date: Date): string {
    const cambodiaOffsetMinutes = 7 * 60;
    const cambodiaTimeMs = date.getTime() + cambodiaOffsetMinutes * 60_000;
    const cambodiaDate = new Date(cambodiaTimeMs);

    const year = cambodiaDate.getUTCFullYear();
    const month = String(cambodiaDate.getUTCMonth() + 1).padStart(2, "0");
    const day = String(cambodiaDate.getUTCDate()).padStart(2, "0");
    const hours = String(cambodiaDate.getUTCHours()).padStart(2, "0");
    const minutes = String(cambodiaDate.getUTCMinutes()).padStart(2, "0");
    const seconds = String(cambodiaDate.getUTCSeconds()).padStart(2, "0");

    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}+07:00`;
  }

  function toIsoDateTime(requestDate: string, timeValue: string): string {
    const raw = String(timeValue ?? "").trim();

    // Already full datetime input -> normalize to Cambodia offset datetime
    if (raw.includes("T")) {
      const parsed = new Date(raw);
      if (!Number.isNaN(parsed.getTime()))
        return toCambodiaOffsetDateTime(parsed);
      throw new Error("time value must be a valid datetime");
    }

    // Time-only input (HH:mm or HH:mm:ss) -> Cambodia local datetime
    if (/^\d{2}:\d{2}$/.test(raw)) {
      return `${requestDate}T${raw}:00+07:00`;
    }

    if (/^\d{2}:\d{2}:\d{2}$/.test(raw)) {
      return `${requestDate}T${raw}+07:00`;
    }

    // Last chance: parse as date-like input
    const parsed = new Date(raw);
    if (!Number.isNaN(parsed.getTime()))
      return toCambodiaOffsetDateTime(parsed);

    throw new Error("start_time/end_time must be valid datetime values");
  }

  function normalizeCreatePayload(
    payload: OvertimeRequestCreateDTO,
  ): OvertimeRequestCreateDTO {
    const requestDate = normalizeRequestDate(payload.request_date);
    const startTime = toIsoDateTime(requestDate, payload.start_time);
    const endTime = toIsoDateTime(requestDate, payload.end_time);
    const cambodiaStartDate = startTime.slice(0, 10);

    return {
      ...payload,
      // Backend requires request_date to match overtime start date in Cambodia time.
      request_date: cambodiaStartDate,
      start_time: startTime,
      end_time: endTime,
    };
  }

  /**
   * Create a new overtime request
   * POST /api/hrms/overtime-requests
   */
  async function createRequest(payload: OvertimeRequestCreateDTO) {
    const action: OvertimeAction = "createRequest";
    setActionStatus(action, { loading: true, error: null, success: false });
    try {
      const normalizedPayload = normalizeCreatePayload(payload);
      const result = await hrmsAdminService().overtimeRequest.createRequest(
        normalizedPayload,
      );
      setActionStatus(action, { success: true, loading: false });
      // Refresh my requests list
      if (myRequests.value) {
        myRequests.value.unshift(result);
      }
      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message ||
        error?.message ||
        "Failed to create request";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Get all overtime requests
   * GET /api/hrms/overtime-requests
   */
  async function fetchList(page = 1) {
    const action: OvertimeAction = "getRequests";
    setActionStatus(action, { loading: true, error: null });
    try {
      const result = await hrmsAdminService().overtimeRequest.getRequests({
        page,
        limit: pagination.limit,
        status: (filters.status as any) || undefined,
        employee_id: filters.employee_id || undefined,
        start_date: filters.start_date || undefined,
        end_date: filters.end_date || undefined,
      });

      list.value = result.items ?? [];
      pagination.page = result.page ?? 1;
      pagination.total = result.total ?? 0;
      pagination.totalPages = result.total_pages ?? 0;

      setActionStatus(action, { loading: false, success: true });
      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message || "Failed to fetch requests";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Get my overtime requests
   * GET /api/hrms/overtime-requests/my
   */
  async function fetchMyList(page = 1) {
    const action: OvertimeAction = "getMyRequests";
    setActionStatus(action, { loading: true, error: null });
    try {
      const result = await hrmsAdminService().overtimeRequest.getMyRequests({
        page,
        limit: pagination.limit,
        status: (filters.status as any) || undefined,
        start_date: filters.start_date || undefined,
        end_date: filters.end_date || undefined,
      });

      myRequests.value = result.items ?? [];
      pagination.page = result.page ?? 1;
      pagination.total = result.total ?? 0;
      pagination.totalPages = result.total_pages ?? 0;

      setActionStatus(action, { loading: false, success: true });
      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message || "Failed to fetch my requests";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Get a specific overtime request
   * GET /api/hrms/overtime-requests/<overtime_id>
   */
  async function fetchOne(id: string) {
    const action: OvertimeAction = "getRequest";
    setActionStatus(action, { loading: true, error: null });
    try {
      const result = await hrmsAdminService().overtimeRequest.getRequest(id);
      requestDetail.value = result;
      setActionStatus(action, { loading: false, success: true });
      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message || "Failed to fetch request detail";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Get pending overtime requests
   * GET /api/hrms/overtime-requests/pending-approval
   */
  async function fetchPendingApproval(page = 1) {
    const action: OvertimeAction = "getPendingRequests";
    setActionStatus(action, { loading: true, error: null });
    try {
      const result =
        await hrmsAdminService().overtimeRequest.getPendingRequests({
          page,
          limit: pagination.limit,
          employee_id: filters.employee_id || undefined,
          start_date: filters.start_date || undefined,
          end_date: filters.end_date || undefined,
        });

      pendingApproval.value = result.items ?? [];
      pagination.page = result.page ?? 1;
      pagination.total = result.total ?? 0;
      pagination.totalPages = result.total_pages ?? 0;

      setActionStatus(action, { loading: false, success: true });
      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message || "Failed to fetch pending approvals";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Get my overtime summary
   * GET /api/hrms/overtime-requests/my-summary
   */
  async function fetchMySummary() {
    const action: OvertimeAction = "getMyOvertimeSummary";
    setActionStatus(action, { loading: true, error: null });
    try {
      const result =
        await hrmsAdminService().overtimeRequest.getMyOvertimeSummary();
      mySummary.value = result;
      setActionStatus(action, { loading: false, success: true });
      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message || "Failed to fetch my summary";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Get payroll approved overtime requests
   * GET /api/hrms/overtime-requests/payroll-approved
   */
  async function fetchPayrollApproved(page = 1) {
    const action: OvertimeAction = "getPayrollApprovedRequests";
    setActionStatus(action, { loading: true, error: null });
    try {
      const result =
        await hrmsAdminService().overtimeRequest.getPayrollApprovedRequests({
          page,
          limit: pagination.limit,
          employee_id: filters.employee_id || undefined,
          start_date: filters.start_date || undefined,
          end_date: filters.end_date || undefined,
        });

      payrollApproved.value = result.items ?? [];
      pagination.page = result.page ?? 1;
      pagination.total = result.total ?? 0;
      pagination.totalPages = result.total_pages ?? 0;

      setActionStatus(action, { loading: false, success: true });
      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message ||
        "Failed to fetch payroll approved requests";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Get payroll overtime summary
   * GET /api/hrms/overtime-requests/payroll-summary
   */
  async function fetchPayrollSummary() {
    const action: OvertimeAction = "getPayrollOvertimeSummary";
    setActionStatus(action, { loading: true, error: null });
    try {
      const result =
        await hrmsAdminService().overtimeRequest.getPayrollOvertimeSummary({
          start_date: filters.start_date || undefined,
          end_date: filters.end_date || undefined,
          employee_id: filters.employee_id || undefined,
        });
      payrollSummary.value = result;
      setActionStatus(action, { loading: false, success: true });
      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message || "Failed to fetch payroll summary";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Approve an overtime request
   * POST /api/hrms/overtime-requests/<overtime_id>/approve
   */
  async function approveRequest(id: string, payload: OvertimeApproveDTO) {
    const action: OvertimeAction = "approveRequest";
    setActionStatus(action, { loading: true, error: null, success: false });
    try {
      const result = await hrmsAdminService().overtimeRequest.approveRequest(
        id,
        payload,
      );
      setActionStatus(action, { success: true, loading: false });

      // Update the request in lists
      updateRequestInLists(result);
      if (requestDetail.value?.id === id) {
        requestDetail.value = result;
      }

      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message || "Failed to approve request";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Reject an overtime request
   * POST /api/hrms/overtime-requests/<overtime_id>/reject
   */
  async function rejectRequest(id: string, payload: OvertimeRejectDTO) {
    const action: OvertimeAction = "rejectRequest";
    setActionStatus(action, { loading: true, error: null, success: false });
    try {
      const result = await hrmsAdminService().overtimeRequest.rejectRequest(
        id,
        payload,
      );
      setActionStatus(action, { success: true, loading: false });

      // Update the request in lists
      updateRequestInLists(result);
      if (requestDetail.value?.id === id) {
        requestDetail.value = result;
      }

      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message || "Failed to reject request";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Cancel an overtime request
   * POST /api/hrms/overtime-requests/<overtime_id>/cancel
   */
  async function cancelRequest(id: string, payload?: OvertimeCancelDTO) {
    const action: OvertimeAction = "cancelRequest";
    setActionStatus(action, { loading: true, error: null, success: false });
    try {
      const result = await hrmsAdminService().overtimeRequest.cancelRequest(
        id,
        payload,
      );
      setActionStatus(action, { success: true, loading: false });

      // Update the request in lists
      updateRequestInLists(result);
      if (requestDetail.value?.id === id) {
        requestDetail.value = result;
      }

      return result;
    } catch (error: any) {
      const errorMsg =
        error?.response?.data?.message || "Failed to cancel request";
      setActionStatus(action, { error: errorMsg, loading: false });
      throw error;
    }
  }

  /**
   * Helper to update request in all lists
   */
  function updateRequestInLists(request: OvertimeRequestDTO) {
    const updateList = (items: OvertimeRequestDTO[]) => {
      const index = items.findIndex((r) => r.id === request.id);
      if (index !== -1) {
        items[index] = request;
      }
    };

    updateList(list.value);
    updateList(myRequests.value);
    updateList(pendingApproval.value);
    updateList(payrollApproved.value);
  }

  /**
   * Set pagination
   */
  function setPagination(page: number, limit: number) {
    pagination.page = page;
    pagination.limit = limit;
  }

  /**
   * Set filters
   */
  function setFilters(newFilters: Partial<typeof filters>) {
    Object.assign(filters, newFilters);
  }

  /**
   * Reset filters
   */
  function resetFilters() {
    filters.status = null;
    filters.employee_id = null;
    filters.start_date = null;
    filters.end_date = null;
  }

  /**
   * Clear detail
   */
  function clearDetail() {
    requestDetail.value = null;
  }

  return {
    // State
    list,
    myRequests,
    pendingApproval,
    payrollApproved,
    requestDetail,
    mySummary,
    payrollSummary,
    pagination,
    filters,
    actionStatus,

    // Getters
    getError,
    isLoading,

    // Actions
    createRequest,
    fetchList,
    fetchMyList,
    fetchOne,
    fetchPendingApproval,
    fetchMySummary,
    fetchPayrollApproved,
    fetchPayrollSummary,
    approveRequest,
    rejectRequest,
    cancelRequest,

    // Utilities
    setActionStatus,
    setFilters,
    resetFilters,
    setPagination,
    clearDetail,
  };
});
