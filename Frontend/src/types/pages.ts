/**
 * Type definitions for page components
 * Ensures consistency across all pages in the application
 */

export interface PageMeta {
  layout?: string;
  middleware?: string | string[];
  requiresAuth?: boolean;
  roles?: string[];
  title?: string;
  description?: string;
}

export interface PageProps {
  id?: string;
}

export interface PageState<T = any> {
  loading: boolean;
  error: Error | null;
  data: T | null;
}

/**
 * Standard page component interface
 */
export interface Page<TProps extends Record<string, any> = any, TState = any> {
  props?: TProps;
  setup(): TState;
}

/**
 * List/Table page interface
 */
export interface ListPageOptions {
  pageSize?: number;
  sortBy?: string;
  sortOrder?: "asc" | "desc";
  filters?: Record<string, any>;
}

export interface ListPageState<T = any> {
  items: T[];
  loading: boolean;
  error: Error | null;
  page: number;
  pageSize: number;
  total: number;
  options: ListPageOptions;
}

/**
 * Detail/Edit page interface
 */
export interface DetailPageState<T = any> {
  item: T | null;
  loading: boolean;
  error: Error | null;
  isEditing: boolean;
  isSaving: boolean;
}

/**
 * Form page interface
 */
export interface FormPageState<T = any> {
  form: T;
  loading: boolean;
  error: Error | null;
  isSubmitting: boolean;
  isDirty: boolean;
  errors: Record<string, string>;
}
