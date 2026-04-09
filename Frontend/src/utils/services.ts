/**
 * API Services utility module
 * Provides lazy-loaded service instances for all modules
 */

let _adminServiceInstance: any = null;
let _hrmsAdminServiceInstance: any = null;
let _studentServiceInstance: any = null;
let _teacherServiceInstance: any = null;

/**
 * Get or create Admin service instance
 */
export function getAdminService() {
  if (!_adminServiceInstance) {
    const { adminService } = useAsyncData("admin-service", () =>
      import("~/api/admin").then((m) => ({ service: m.adminService() })),
    );
    _adminServiceInstance = adminService.value?.service;
  }
  return _adminServiceInstance;
}

/**
 * Get or create HRMS Admin service instance
 */
export function getHrmsAdminService() {
  if (!_hrmsAdminServiceInstance) {
    const { hrmsAdminService } = useAsyncData("hrms-admin-service", () =>
      import("~/api/hr_admin").then((m) => ({ service: m.hrmsAdminService() })),
    );
    _hrmsAdminServiceInstance = hrmsAdminService.value?.service;
  }
  return _hrmsAdminServiceInstance;
}

/**
 * Get or create Student service instance
 */
export function getStudentService() {
  if (!_studentServiceInstance) {
    const { studentService } = useAsyncData("student-service", () =>
      import("~/api/student").then((m) => ({ service: m.studentService?.() })),
    );
    _studentServiceInstance = studentService.value?.service;
  }
  return _studentServiceInstance;
}

/**
 * Get or create Teacher service instance
 */
export function getTeacherService() {
  if (!_teacherServiceInstance) {
    const { teacherService } = useAsyncData("teacher-service", () =>
      import("~/api/teacher").then((m) => ({ service: m.teacherService?.() })),
    );
    _teacherServiceInstance = teacherService.value?.service;
  }
  return _teacherServiceInstance;
}
