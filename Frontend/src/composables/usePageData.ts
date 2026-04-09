/**
 * Composable hook for managing page-level data loading and error handling
 * Provides consistent patterns across all page components
 */

import { ref, readonly, computed } from "vue";
import type { Ref } from "vue";

export interface UsePageDataOptions {
  pageName?: string;
  showNotification?: boolean;
}

export interface PageDataState<T> {
  data: Ref<T | null>;
  loading: Ref<boolean>;
  error: Ref<Error | null>;
  isLoaded: Ref<boolean>;
}

/**
 * Generic composable for page data loading
 * Usage:
 * ```ts
 * const { data, loading, error, executeRequest } = usePageData({ pageName: 'Users' });
 * onMounted(() => {
 *   executeRequest(() => userService.getList());
 * });
 * ```
 */
export function usePageData<T>(
  options: UsePageDataOptions = {},
): PageDataState<T> & {
  executeRequest: (requestFn: () => Promise<T>) => Promise<void>;
  reset: () => void;
} {
  const data = ref<T | null>(null);
  const loading = ref(false);
  const error = ref<Error | null>(null);
  const isLoaded = ref(false);

  const reset = () => {
    data.value = null;
    error.value = null;
    isLoaded.value = false;
  };

  const executeRequest = async (requestFn: () => Promise<T>) => {
    loading.value = true;
    error.value = null;

    try {
      data.value = await requestFn();
      isLoaded.value = true;

      if (options.showNotification) {
        // Notification will be handled by parent component or notification service
        console.log(`✓ ${options.pageName || "Data"} loaded successfully`);
      }
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err));
      console.error(
        `✗ ${options.pageName || "Data"} load failed:`,
        error.value.message,
      );

      if (options.showNotification) {
        // Notification service integration can be added here
      }
    } finally {
      loading.value = false;
    }
  };

  return {
    data: readonly(data),
    loading: readonly(loading),
    error: readonly(error),
    isLoaded: readonly(isLoaded),
    executeRequest,
    reset,
  };
}

/**
 * Composable for list/table data management with pagination and filtering
 */
export interface UsePageListOptions<TFilter = any> extends UsePageDataOptions {
  pageSize?: number;
  initialFilters?: TFilter;
}

export interface PageListState<T, TFilter = any> extends PageDataState<T[]> {
  page: Ref<number>;
  pageSize: Ref<number>;
  total: Ref<number>;
  filters: Ref<TFilter>;
  hasMore: Ref<boolean>;
}

export function usePageList<T, TFilter = any>(
  options: UsePageListOptions<TFilter> = {},
): PageListState<T, TFilter> & {
  executeRequest: (
    requestFn: (
      page: number,
      pageSize: number,
      filters: TFilter,
    ) => Promise<{ data: T[]; total: number }>,
  ) => Promise<void>;
  nextPage: () => Promise<void>;
  prevPage: () => Promise<void>;
  goToPage: (pageNumber: number) => Promise<void>;
  setFilters: (filters: TFilter) => void;
  reset: () => void;
} {
  const data = ref<T[]>([]);
  const loading = ref(false);
  const error = ref<Error | null>(null);
  const isLoaded = ref(false);
  const page = ref(1);
  const pageSize = ref(options.pageSize || 10);
  const total = ref(0);
  const filters = ref<TFilter>(options.initialFilters || ({} as TFilter));

  const hasMore = computed(() => page.value * pageSize.value < total.value);

  let lastRequestFn:
    | ((
        page: number,
        pageSize: number,
        filters: TFilter,
      ) => Promise<{ data: T[]; total: number }>)
    | null = null;

  const reset = () => {
    data.value = [];
    error.value = null;
    isLoaded.value = false;
    page.value = 1;
    total.value = 0;
  };

  const executeRequest = async (
    requestFn: (
      page: number,
      pageSize: number,
      filters: TFilter,
    ) => Promise<{ data: T[]; total: number }>,
  ) => {
    lastRequestFn = requestFn;
    loading.value = true;
    error.value = null;

    try {
      const result = await requestFn(page.value, pageSize.value, filters.value);
      data.value = result.data;
      total.value = result.total;
      isLoaded.value = true;
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err));
    } finally {
      loading.value = false;
    }
  };

  const nextPage = async () => {
    if (hasMore.value && lastRequestFn) {
      page.value++;
      await executeRequest(lastRequestFn);
    }
  };

  const prevPage = async () => {
    if (page.value > 1 && lastRequestFn) {
      page.value--;
      await executeRequest(lastRequestFn);
    }
  };

  const goToPage = async (pageNumber: number) => {
    if (pageNumber >= 1 && lastRequestFn) {
      page.value = pageNumber;
      await executeRequest(lastRequestFn);
    }
  };

  const setFilters = (newFilters: TFilter) => {
    filters.value = newFilters;
    page.value = 1; // Reset to first page on filter change
  };

  return {
    data: readonly(data),
    loading: readonly(loading),
    error: readonly(error),
    isLoaded: readonly(isLoaded),
    page: readonly(page),
    pageSize: readonly(pageSize),
    total: readonly(total),
    filters: readonly(filters),
    hasMore: readonly(hasMore),
    executeRequest,
    nextPage,
    prevPage,
    goToPage,
    setFilters,
    reset,
  };
}
