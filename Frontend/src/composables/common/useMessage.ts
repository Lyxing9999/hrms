// composables/useMessage.ts
import { ElMessage } from "element-plus";

const DEFAULT_DURATION = {
  success: 3000,
  error: 5000,
  info: 3000,
  warning: 4000,
} as const;

type MessageType = keyof typeof DEFAULT_DURATION;

export function useMessage() {
  function show(type: MessageType, msg: string, duration?: number) {
    ElMessage({
      message: msg,
      type,
      duration: duration ?? DEFAULT_DURATION[type],
      showClose: true,
      grouping: true,
    });
  }

  /**
   * Show a success message toast
   * @param msg - Message text to display
   */
  function showSuccess(msg: string) {
    show("success", msg);
  }

  /**
   * Show an error message toast
   * @param msg - Message text to display
   */
  function showError(msg: string) {
    show("error", msg);
  }

  /**
   * Show an info message toast
   * @param msg - Message text to display
   */
  function showInfo(msg: string) {
    show("info", msg);
  }

  /**
   * Show a warning message toast
   * @param msg - Message text to display
   */
  function showWarning(msg: string) {
    show("warning", msg);
  }

  /**
   * Show a standard warning for repeated clicks while an action is running.
   */
  function showActionInProgress() {
    show("warning", "Action is already running. Please wait a moment.", 2200);
  }

  return {
    showSuccess,
    showError,
    showInfo,
    showWarning,
    showActionInProgress,
  };
}
