<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import { hrmsAdminService } from "~/api/hr_admin";
import type {
  AttendanceDTO,
  AttendanceStatus,
} from "~/api/hr_admin/attendance";

interface GeoCoordinates {
  latitude: number;
  longitude: number;
}

const attendanceService = hrmsAdminService().attendance;

const attendance = ref<AttendanceDTO | null>(null);
const currentLocalTime = ref(new Date());

const isLoadingAttendance = ref(false);
const isCheckingIn = ref(false);
const isCheckingOut = ref(false);

const pageError = ref("");
const actionError = ref("");
const geolocationError = ref("");
const wrongLocationReason = ref("");

let clockInterval: ReturnType<typeof setInterval> | null = null;

const hasCheckedIn = computed(() => Boolean(attendance.value?.check_in_time));
const hasCheckedOut = computed(() => Boolean(attendance.value?.check_out_time));

const canCheckIn = computed(
  () =>
    !hasCheckedIn.value &&
    !isLoadingAttendance.value &&
    !isCheckingIn.value &&
    !isCheckingOut.value,
);

const canCheckOut = computed(
  () =>
    hasCheckedIn.value &&
    !hasCheckedOut.value &&
    !isLoadingAttendance.value &&
    !isCheckingIn.value &&
    !isCheckingOut.value,
);

const showWrongLocationPending = computed(
  () => attendance.value?.status === "wrong_location_pending",
);

const statusBadgeClasses = computed(() => {
  const map: Record<string, string> = {
    checked_in: "bg-blue-100 text-blue-700 ring-blue-200",
    checked_out: "bg-emerald-100 text-emerald-700 ring-emerald-200",
    late: "bg-amber-100 text-amber-700 ring-amber-200",
    early_leave: "bg-orange-100 text-orange-700 ring-orange-200",
    absent: "bg-rose-100 text-rose-700 ring-rose-200",
    holiday_off: "bg-sky-100 text-sky-700 ring-sky-200",
    weekend_off: "bg-slate-100 text-slate-700 ring-slate-200",
    wrong_location_pending: "bg-yellow-100 text-yellow-700 ring-yellow-200",
    wrong_location_approved: "bg-emerald-100 text-emerald-700 ring-emerald-200",
    wrong_location_rejected: "bg-rose-100 text-rose-700 ring-rose-200",
  };

  return (
    map[attendance.value?.status ?? ""] ??
    "bg-gray-100 text-gray-700 ring-gray-200"
  );
});

const clockLabel = computed(() =>
  currentLocalTime.value.toLocaleString("en-US", {
    weekday: "short",
    month: "short",
    day: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }),
);

const formatDateTime = (iso?: string | null) => {
  if (!iso) return "-";

  return new Date(iso).toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatStatusLabel = (status?: string | null) => {
  if (!status) return "Not Checked In";

  const map: Record<AttendanceStatus, string> = {
    checked_in: "Checked In",
    checked_out: "Checked Out",
    late: "Late",
    early_leave: "Early Leave",
    absent: "Absent",
    holiday_off: "Holiday Off",
    weekend_off: "Weekend Off",
    wrong_location_pending: "Wrong Location Pending",
    wrong_location_approved: "Wrong Location Approved",
    wrong_location_rejected: "Wrong Location Rejected",
  };

  return map[status as AttendanceStatus] ?? status;
};

const resolveErrorMessage = (error: unknown) => {
  const e = error as {
    message?: string;
    response?: {
      status?: number;
      data?: { message?: string };
    };
  };

  return (
    e.response?.data?.message ||
    e.message ||
    "Something went wrong. Please try again."
  );
};

const getGeolocation = (): Promise<GeoCoordinates> =>
  new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error("Geolocation is not supported by your browser."));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      },
      (error) => {
        if (error.code === error.PERMISSION_DENIED) {
          reject(
            new Error(
              "Location permission was denied. Please allow location access and try again.",
            ),
          );
          return;
        }

        if (error.code === error.POSITION_UNAVAILABLE) {
          reject(
            new Error(
              "Unable to determine your location right now. Please try again.",
            ),
          );
          return;
        }

        if (error.code === error.TIMEOUT) {
          reject(new Error("Location request timed out. Please try again."));
          return;
        }

        reject(new Error("Failed to capture your location. Please try again."));
      },
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 0,
      },
    );
  });

const loadMyAttendance = async () => {
  isLoadingAttendance.value = true;
  pageError.value = "";

  try {
    const result = await attendanceService.getMyAttendance({
      showError: false,
    });

    if (result) {
      attendance.value = result;
    } else {
      attendance.value = null;
    }
  } catch (error) {
    const message = resolveErrorMessage(error).toLowerCase();
    const status = (error as { response?: { status?: number } })?.response
      ?.status;

    if (
      status === 404 ||
      message.includes("not found") ||
      message.includes("no attendance")
    ) {
      attendance.value = null;
      return;
    }

    pageError.value = resolveErrorMessage(error);
  } finally {
    isLoadingAttendance.value = false;
  }
};

const handleRefresh = async () => {
  await loadMyAttendance();
};

const handleCheckIn = async () => {
  if (!canCheckIn.value) return;

  isCheckingIn.value = true;
  actionError.value = "";
  geolocationError.value = "";

  try {
    const location = await getGeolocation();
    const checkInTime = new Date().toISOString();

    await attendanceService.checkIn({
      check_in_time: checkInTime,
      latitude: location.latitude,
      longitude: location.longitude,
      wrong_location_reason: wrongLocationReason.value.trim() || null,
    });

    wrongLocationReason.value = "";

    await loadMyAttendance();
  } catch (error) {
    const message = resolveErrorMessage(error);
    actionError.value = message;

    if (
      message.toLowerCase().includes("location") ||
      message.toLowerCase().includes("geolocation")
    ) {
      geolocationError.value = message;
    }
  } finally {
    isCheckingIn.value = false;
  }
};

const handleCheckOut = async () => {
  if (!canCheckOut.value) return;

  isCheckingOut.value = true;
  actionError.value = "";
  geolocationError.value = "";

  try {
    const location = await getGeolocation();
    const checkOutTime = new Date().toISOString();

    await attendanceService.checkOut({
      check_out_time: checkOutTime,
      latitude: location.latitude,
      longitude: location.longitude,
    });

    await loadMyAttendance();
  } catch (error) {
    const message = resolveErrorMessage(error);
    actionError.value = message;

    if (
      message.toLowerCase().includes("location") ||
      message.toLowerCase().includes("geolocation")
    ) {
      geolocationError.value = message;
    }
  } finally {
    isCheckingOut.value = false;
  }
};

onMounted(async () => {
  await loadMyAttendance();

  clockInterval = setInterval(() => {
    currentLocalTime.value = new Date();
  }, 1000);
});

onUnmounted(() => {
  if (clockInterval) clearInterval(clockInterval);
});
const formatDate = (iso?: string | null) => {
  if (!iso) return "-";

  return new Date(iso).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "2-digit",
  });
};
</script>

<template>
  <div class="space-y-6 pb-10">
    <OverviewHeader
      :title="'My Attendance'"
      :description="'Check in and check out with GPS verification for accurate attendance records.'"
      :backPath="'/hr/attendance'"
    >
      <template #actions>
        <button
          type="button"
          class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="isLoadingAttendance || isCheckingIn || isCheckingOut"
          @click="handleRefresh"
        >
          Refresh
        </button>
      </template>
    </OverviewHeader>

    <section
      class="rounded-2xl border border-slate-200 bg-gradient-to-r from-slate-900 to-slate-700 p-5 text-white shadow-sm sm:p-6"
    >
      <p class="text-xs uppercase tracking-[0.2em] text-slate-300">
        Local Time
      </p>
      <p class="mt-2 text-2xl font-semibold sm:text-3xl">
        {{ clockLabel }}
      </p>
    </section>

    <div
      v-if="pageError"
      class="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700"
    >
      {{ pageError }}
    </div>

    <div class="grid gap-5 lg:grid-cols-2">
      <section
        class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6"
      >
        <div class="flex items-start justify-between gap-4">
          <div>
            <h2 class="text-lg font-semibold text-slate-900">
              Today&apos;s Attendance
            </h2>
            <p class="text-sm text-slate-500">
              Self-service summary for your current attendance day.
            </p>
          </div>
          <span
            class="inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ring-1 ring-inset"
            :class="statusBadgeClasses"
          >
            {{ formatStatusLabel(attendance?.status) }}
          </span>
        </div>

        <div v-if="isLoadingAttendance" class="mt-5 animate-pulse space-y-3">
          <div class="h-10 rounded-lg bg-slate-100" />
          <div class="h-10 rounded-lg bg-slate-100" />
          <div class="h-10 rounded-lg bg-slate-100" />
        </div>

        <div v-else-if="attendance" class="mt-5 space-y-4">
          <!-- Basic Info Grid -->
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div
              class="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
            >
              <p
                class="text-xs font-medium uppercase tracking-wide text-slate-500"
              >
                Attendance Date
              </p>
              <p class="mt-1 text-sm font-semibold text-slate-800">
                {{ formatDate(attendance.attendance_date) }}
              </p>
            </div>

            <div
              class="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
            >
              <p
                class="text-xs font-medium uppercase tracking-wide text-slate-500"
              >
                Check-In Time
              </p>
              <p class="mt-1 text-sm font-semibold text-slate-800">
                {{ formatDateTime(attendance.check_in_time) }}
              </p>
            </div>

            <div
              class="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
            >
              <p
                class="text-xs font-medium uppercase tracking-wide text-slate-500"
              >
                Check-Out Time
              </p>
              <p class="mt-1 text-sm font-semibold text-slate-800">
                {{ formatDateTime(attendance.check_out_time) }}
              </p>
            </div>

            <div
              class="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
            >
              <p
                class="text-xs font-medium uppercase tracking-wide text-slate-500"
              >
                Status
              </p>
              <p class="mt-1 text-sm font-semibold text-slate-800">
                {{ formatStatusLabel(attendance.status) }}
              </p>
            </div>

            <div
              class="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
            >
              <p
                class="text-xs font-medium uppercase tracking-wide text-slate-500"
              >
                Late Minutes
              </p>
              <p class="mt-1 text-sm font-semibold text-slate-800">
                {{ attendance.late_minutes ?? 0 }}
              </p>
            </div>

            <div
              class="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
            >
              <p
                class="text-xs font-medium uppercase tracking-wide text-slate-500"
              >
                Early Leave Minutes
              </p>
              <p class="mt-1 text-sm font-semibold text-slate-800">
                {{ attendance.early_leave_minutes ?? 0 }}
              </p>
            </div>
          </div>

          <!-- Location Information -->
          <div class="rounded-xl border border-blue-200 bg-blue-50 p-4">
            <h3 class="text-sm font-semibold text-blue-900">
              Check-In Location Details
            </h3>
            <div class="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2 text-sm">
              <div>
                <p class="text-xs font-medium text-blue-700">Latitude</p>
                <p class="mt-1 font-mono text-blue-900">
                  {{ attendance.check_in_latitude?.toFixed(6) ?? "-" }}
                </p>
              </div>
              <div>
                <p class="text-xs font-medium text-blue-700">Longitude</p>
                <p class="mt-1 font-mono text-blue-900">
                  {{ attendance.check_in_longitude?.toFixed(6) ?? "-" }}
                </p>
              </div>
              <div>
                <p class="text-xs font-medium text-blue-700">Location ID</p>
                <p class="mt-1 font-mono text-blue-900 truncate">
                  {{ attendance.location_id ?? "-" }}
                </p>
              </div>
              <div>
                <p class="text-xs font-medium text-blue-700">Schedule ID</p>
                <p class="mt-1 font-mono text-blue-900 truncate">
                  {{ attendance.schedule_id ?? "-" }}
                </p>
              </div>
            </div>
          </div>

          <!-- Wrong Location Reason -->
          <div
            v-if="showWrongLocationPending || attendance.wrong_location_reason"
            class="rounded-xl border border-yellow-200 bg-yellow-50 px-4 py-3"
          >
            <div class="flex gap-2">
              <span class="text-xl">⚠️</span>
              <div>
                <p class="font-semibold text-yellow-900">
                  Location Pending Review
                </p>
                <p class="mt-1 text-sm text-yellow-800">
                  {{
                    attendance.wrong_location_reason || "Reason not provided"
                  }}
                </p>
              </div>
            </div>
            <p class="mt-2 text-xs text-yellow-700">
              Your check-in location is pending admin review. You can still
              monitor your status here.
            </p>
          </div>

          <!-- Lifecycle Information -->
          <div class="rounded-xl border border-slate-200 bg-slate-50 p-4">
            <h3 class="text-sm font-semibold text-slate-900">
              Record Timeline
            </h3>
            <div class="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2 text-sm">
              <div>
                <p class="text-xs font-medium text-slate-600">Created</p>
                <p class="mt-1 text-slate-800">
                  {{ formatDateTime(attendance.lifecycle?.created_at) }}
                </p>
              </div>
              <div>
                <p class="text-xs font-medium text-slate-600">Last Updated</p>
                <p class="mt-1 text-slate-800">
                  {{ formatDateTime(attendance.lifecycle?.updated_at) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div
          v-else
          class="mt-5 rounded-xl border border-dashed border-slate-300 bg-slate-50 px-4 py-8 text-center text-sm text-slate-500"
        >
          No attendance record found for today yet. Use the action panel to
          check in.
        </div>
      </section>

      <section
        class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6"
      >
        <div>
          <h2 class="text-lg font-semibold text-slate-900">
            Attendance Actions
          </h2>
          <p class="text-sm text-slate-500">
            Your current time is automatically sent as ISO datetime on each
            action.
          </p>
        </div>

        <div
          v-if="geolocationError"
          class="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800"
        >
          {{ geolocationError }}
        </div>

        <div
          v-else-if="actionError"
          class="mt-4 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700"
        >
          {{ actionError }}
        </div>

        <div class="mt-5 space-y-6">
          <div class="rounded-xl border border-slate-200 p-4">
            <div class="flex items-center justify-between">
              <h3
                class="text-sm font-semibold uppercase tracking-wide text-slate-700"
              >
                Check-In
              </h3>
              <span
                class="text-xs font-medium"
                :class="hasCheckedIn ? 'text-emerald-700' : 'text-slate-500'"
              >
                {{ hasCheckedIn ? "Completed" : "Pending" }}
              </span>
            </div>

            <label
              for="wrong-location-reason"
              class="mt-4 block text-sm font-medium text-slate-700"
            >
              Wrong Location Reason (Optional)
            </label>
            <textarea
              id="wrong-location-reason"
              v-model="wrongLocationReason"
              rows="3"
              class="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-700 outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200 disabled:cursor-not-allowed disabled:bg-slate-100"
              :disabled="!canCheckIn"
              placeholder="If you are checking in from a different location, add a reason for admin review..."
            />

            <button
              type="button"
              class="mt-4 w-full rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:bg-slate-300"
              :disabled="!canCheckIn"
              @click="handleCheckIn"
            >
              {{
                isCheckingIn
                  ? "Checking In..."
                  : hasCheckedIn
                  ? "Already Checked In"
                  : "Check In Now"
              }}
            </button>
          </div>

          <div class="rounded-xl border border-slate-200 p-4">
            <div class="flex items-center justify-between">
              <h3
                class="text-sm font-semibold uppercase tracking-wide text-slate-700"
              >
                Check-Out
              </h3>
              <span
                class="text-xs font-medium"
                :class="hasCheckedOut ? 'text-emerald-700' : 'text-slate-500'"
              >
                {{ hasCheckedOut ? "Completed" : "Pending" }}
              </span>
            </div>

            <p class="mt-4 text-sm text-slate-500">
              Check-out also requires geolocation and sends the current datetime
              as ISO string.
            </p>

            <button
              type="button"
              class="mt-4 w-full rounded-xl bg-emerald-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:bg-slate-300"
              :disabled="!canCheckOut"
              @click="handleCheckOut"
            >
              {{
                isCheckingOut
                  ? "Checking Out..."
                  : hasCheckedOut
                  ? "Already Checked Out"
                  : "Check Out Now"
              }}
            </button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
