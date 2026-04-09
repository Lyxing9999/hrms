/**
 * API response and error handling utilities
 * Provides consistent formatting for API responses across the application
 */

export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T = any> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export class ApiError extends Error {
  constructor(
    public code: string,
    public statusCode: number,
    public details?: any,
  ) {
    super(`API Error: ${code}`);
    this.name = "ApiError";
  }
}

/**
 * Wrap API errors with consistent formatting
 */
export function handleApiError(error: any): ApiError {
  if (error instanceof ApiError) {
    return error;
  }

  const statusCode = error?.response?.status || error?.statusCode || 500;
  const message =
    error?.response?.data?.message || error?.message || "Unknown error";
  const details = error?.response?.data || error;

  return new ApiError(message, statusCode, details);
}

/**
 * Normalize paginated response
 */
export function normalizePaginatedResponse<T = any>(
  items: T[],
  total: number,
  page: number,
  pageSize: number,
): PaginatedResponse<T> {
  return {
    items,
    total,
    page,
    pageSize,
    totalPages: Math.ceil(total / pageSize),
  };
}

/**
 * Check if response is successful
 */
export function isSuccessResponse(response: any): response is ApiResponse {
  return response?.success === true || response?.data !== undefined;
}

/**
 * Validate required fields in API response
 */
export function validateApiResponse<T extends Record<string, any>>(
  data: any,
  requiredFields: Array<keyof T>,
): data is T {
  if (!data || typeof data !== "object") {
    return false;
  }

  return requiredFields.every((field) => data[field] !== undefined);
}
