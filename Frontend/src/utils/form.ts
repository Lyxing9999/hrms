/**
 * Form utilities for consistent form handling across pages
 */

import { ref, reactive, computed, readonly } from "vue";
import type { Ref } from "vue";

export interface FormState<T> {
  values: T;
  errors: Record<keyof T, string>;
  touched: Record<keyof T, boolean>;
  isDirty: boolean;
  isSubmitting: boolean;
}

export interface FormOptions<T> {
  initialValues: T;
  onSubmit?: (values: T) => Promise<void>;
  validate?: (values: T) => Record<keyof T, string>;
}

/**
 * Generic form composable for handling form state
 */
export function useForm<T extends Record<string, any>>({
  initialValues,
  onSubmit,
  validate,
}: FormOptions<T>) {
  const values = reactive<T>(JSON.parse(JSON.stringify(initialValues)));
  const errors = reactive<Record<keyof T, string>>({} as any);
  const touched = reactive<Record<keyof T, boolean>>({} as any);
  const isSubmitting = ref(false);

  const isDirty = computed(() => {
    return JSON.stringify(values) !== JSON.stringify(initialValues);
  });

  const setFieldValue = (field: keyof T, value: any) => {
    values[field] = value;
    touched[field] = true;
  };

  const setFieldError = (field: keyof T, error: string) => {
    errors[field] = error;
  };

  const setFieldTouched = (field: keyof T, isTouched: boolean = true) => {
    touched[field] = isTouched;
  };

  const validateForm = () => {
    if (!validate) return true;

    const newErrors = validate(values);
    Object.assign(errors, newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) {
      return;
    }

    if (!onSubmit) return;

    isSubmitting.value = true;
    try {
      await onSubmit(values);
    } catch (error: any) {
      if (error.fieldErrors) {
        Object.assign(errors, error.fieldErrors);
      }
      throw error;
    } finally {
      isSubmitting.value = false;
    }
  };

  const reset = () => {
    Object.assign(values, JSON.parse(JSON.stringify(initialValues)));
    Object.assign(errors, {});
    Object.assign(touched, {});
  };

  const getFieldProps = (field: keyof T) => ({
    modelValue: values[field],
    error: touched[field] ? errors[field] : undefined,
    onChange: (value: any) => setFieldValue(field, value),
    onBlur: () => setFieldTouched(field, true),
  });

  return {
    values: readonly(values),
    errors: readonly(errors),
    touched: readonly(touched),
    isDirty,
    isSubmitting,
    setFieldValue,
    setFieldError,
    setFieldTouched,
    validateForm,
    handleSubmit,
    reset,
    getFieldProps,
  };
}

/**
 * Validation utilities
 */
export const validators = {
  required: (field: string) => (value: any) =>
    value ? "" : `${field} is required`,

  email: (value: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? "" : "Invalid email address",

  minLength: (length: number, field: string) => (value: string) =>
    value?.length >= length
      ? ""
      : `${field} must be at least ${length} characters`,

  maxLength: (length: number, field: string) => (value: string) =>
    value?.length <= length
      ? ""
      : `${field} must be at most ${length} characters`,

  pattern: (pattern: RegExp, message: string) => (value: string) =>
    pattern.test(value) ? "" : message,

  custom: (fn: (value: any) => boolean, message: string) => (value: any) =>
    fn(value) ? "" : message,
};

/**
 * Compose multiple validators
 */
export function composeValidators<T extends Record<string, any>>(
  validationRules: Record<keyof T, Array<(value: any) => string>>,
) {
  return (values: T): Record<keyof T, string> => {
    const errors: any = {};

    Object.entries(validationRules).forEach(([field, rules]) => {
      for (const rule of rules) {
        const error = rule(values[field as keyof T]);
        if (error) {
          errors[field] = error;
          break;
        }
      }
    });

    return errors;
  };
}
