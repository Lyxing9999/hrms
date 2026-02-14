<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useNuxtApp } from "nuxt/app";
import { ElMessage } from "element-plus";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import type { AttendanceDTO, AttendanceStatsDTO } from "~/api/hr_admin/attendance/attendance.dto";
import { Clock, Check, InfoFilled, Timer, Warning, Location, Calendar, TrendCharts } from "@element-plus/icons-vue";

const { $hrAttendanceService } = useNuxtApp();

// State
const loading = ref(false);
const todayAttendance = ref<AttendanceDTO | null>(null);
const currentPosition = ref<{ latitude: number; longitude: number } | null>(null);
const notes = ref("");
const locationDenied = ref(false);
const isCheckingPermission = ref(false);
const checkInProgress = ref(0);
const checkOutProgress = ref(0);
const currentTime = ref(new Date());
const activeTab = ref("check-in");

// Attendance history
const attendanceHistory = ref<AttendanceDTO[]>([]);
const historyLoading = ref(false);
const historyPage = ref(1);
const historyTotal = ref(0);
const historyPageSize = ref(10);

// Statistics
const stats = ref<AttendanceStatsDTO | null>(null);
const statsLoading = ref(false);

// Date range for history
const dateRange = ref<[Date, Date]>([
  new Date(new Date().getFullYear(), new Date().getMonth(), 1), // First day of current month
  new Date(), // Today
]);

// Computed
const isCheckedIn = computed(() => todayAttendance.value !== null);
const isCheckedOut = computed(() => todayAttendance.value?.check_out_time !== null);

const statusColor = computed(() => {
  if (!todayAttendance.value) return "info";
  if (todayAttendance.value.status === "late") return "warning";
  if (todayAttendance.value.status === "early_leave") return "warning";
  if (todayAttendance.value.status === "checked_out") return "success";
  return "primary";
});

const statusText = computed(() => {
  if (!todayAttendance.value) return "Not Checked In";
  if (todayAttendance.value.status === "late") return "Late";
  if (todayAttendance.value.status === "early_leave") return "Early Leave";
  if (todayAttendance.value.status === "checked_out") return "Checked Out";
  return "Checked In";
});

const statusIcon = computed(() => {
  if (!todayAttendance.value) return Clock;
  if (todayAttendance.value.status === "late") return Warning;
  if (todayAttendance.value.status === "checked_out") return Check;
  return Clock;
});

const canCheckIn = computed(() => !isCheckedIn.value && !loading.value && !locationDenied.value);
const canCheckOut = computed(() => isCheckedIn.value && !isCheckedOut.value && !loading.value && !locationDenied.value);

const formattedDateRange = computed(() => {
  if (!dateRange.value || dateRange.value.length !== 2) return "";
  const [start, end] = dateRange.value;
  return `${start.toLocaleDateString()} - ${end.toLocaleDateString()}`;
});

// Methods
const checkLocationPermission = async (): Promise<boolean> => {
  if (!navigator.geolocation) {
    ElMessage.error("Geolocation is not supported by your browser");
    locationDenied.value = true;
    return false;
  }

  try {
    const permissionStatus = await navigator.permissions.query({ name: "geolocation" as PermissionName });
    
    if (permissionStatus.state === "denied") {
      ElMessage.error("Location permission is blocked. Please enable it in your browser settings.");
      locationDenied.value = true;
      return false;
    }

    locationDenied.value = false;
    return true;
  } catch (e) {
    console.error("Permission query failed:", e);
    return true;
  }
};

const getCurrentLocation = (): Promise<{ latitude: number; longitude: number }> => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error("Geolocation is not supported by your browser"));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        locationDenied.value = false;
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      },
      (error) => {
        let errorMessage = "Unable to get your location";
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = "You denied the location request. Please allow location access to check in.";
            locationDenied.value = true;
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = "Location information is unavailable. Please try again.";
            break;
          case error.TIMEOUT:
            errorMessage = "Location request timed out. Please try again.";
            break;
          default:
            errorMessage = "An unknown error occurred while getting your location.";
        }
        reject(new Error(errorMessage));
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      }
    );
  });
};

const loadTodayAttendance = async () => {
  try {
    loading.value = true;
    todayAttendance.value = await $hrAttendanceService.getTodayAttendance();
  } catch (error: any) {
    console.error("Failed to load attendance:", error);
  } finally {
    loading.value = false;
  }
};

const handleCheckIn = async () => {
  try {
    loading.value = true;
    checkInProgress.value = 0;
    
    // Step 1: Check permission (20%)
    checkInProgress.value = 20;
    const hasPermission = await checkLocationPermission();
    if (!hasPermission) {
      ElMessage.error("Location access is required to check in. Please enable location permissions.");
      checkInProgress.value = 0;
      return;
    }

    // Step 2: Get location (50%)
    checkInProgress.value = 50;
    try {
      currentPosition.value = await getCurrentLocation();
    } catch (error: any) {
      ElMessage.error(error.message || "Location access is required to check in. Please enable location permissions.");
      locationDenied.value = true;
      checkInProgress.value = 0;
      return;
    }

    // Validate location data
    if (!currentPosition.value?.latitude || !currentPosition.value?.longitude) {
      ElMessage.error("Unable to get your location. Location is required to check in.");
      checkInProgress.value = 0;
      return;
    }

    // Step 3: Send to backend (80%)
    checkInProgress.value = 80;
    const data = {
      latitude: currentPosition.value.latitude,
      longitude: currentPosition.value.longitude,
      notes: notes.value || undefined,
    };

    todayAttendance.value = await $hrAttendanceService.checkIn(data);
    
    // Step 4: Complete (100%)
    checkInProgress.value = 100;
    ElMessage.success("Checked in successfully!");
    
    if (todayAttendance.value.late_minutes > 0) {
      ElMessage.warning(`You are ${todayAttendance.value.late_minutes} minutes late`);
    }
    
    notes.value = "";
    
    // Reload history and stats
    loadAttendanceHistory();
    loadStats();
    
    // Reset progress after 1 second
    setTimeout(() => {
      checkInProgress.value = 0;
    }, 1000);
  } catch (error: any) {
    ElMessage.error(error.message || "Failed to check in");
    checkInProgress.value = 0;
  } finally {
    loading.value = false;
  }
};

const handleCheckOut = async () => {
  if (!todayAttendance.value) return;

  try {
    loading.value = true;
    checkOutProgress.value = 0;
    
    // Step 1: Check permission (20%)
    checkOutProgress.value = 20;
    const hasPermission = await checkLocationPermission();
    if (!hasPermission) {
      ElMessage.error("Location access is required to check out. Please enable location permissions.");
      checkOutProgress.value = 0;
      return;
    }

    // Step 2: Get location (50%)
    checkOutProgress.value = 50;
    try {
      currentPosition.value = await getCurrentLocation();
    } catch (error: any) {
      ElMessage.error(error.message || "Location access is required to check out. Please enable location permissions.");
      locationDenied.value = true;
      checkOutProgress.value = 0;
      return;
    }

    // Validate location data
    if (!currentPosition.value?.latitude || !currentPosition.value?.longitude) {
      ElMessage.error("Unable to get your location. Location is required to check out.");
      checkOutProgress.value = 0;
      return;
    }

    // Step 3: Send to backend (80%)
    checkOutProgress.value = 80;
    const data = {
      latitude: currentPosition.value.latitude,
      longitude: currentPosition.value.longitude,
      notes: notes.value || undefined,
    };

    todayAttendance.value = await $hrAttendanceService.checkOut(
      todayAttendance.value.id,
      data
    );
    
    // Step 4: Complete (100%)
    checkOutProgress.value = 100;
    ElMessage.success("Checked out successfully!");
    
    if (todayAttendance.value.early_leave_minutes > 0) {
      ElMessage.warning(`You left ${todayAttendance.value.early_leave_minutes} minutes early`);
    }
    
    notes.value = "";
    
    // Reload history and stats
    loadAttendanceHistory();
    loadStats();
    
    // Reset progress after 1 second
    setTimeout(() => {
      checkOutProgress.value = 0;
    }, 1000);
  } catch (error: any) {
    ElMessage.error(error.message || "Failed to check out");
    checkOutProgress.value = 0;
  } finally {
    loading.value = false;
  }
};

const formatTime = (dateStr: string | null) => {
  if (!dateStr) return "-";
  return new Date(dateStr).toLocaleTimeString();
};

const formatDate = (dateStr: string | null) => {
  if (!dateStr) return "-";
  return new Date(dateStr).toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const getWorkDuration = () => {
  if (!todayAttendance.value?.check_in_time) return "-";
  if (!todayAttendance.value?.check_out_time) {
    const start = new Date(todayAttendance.value.check_in_time);
    const now = new Date();
    const diff = now.getTime() - start.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    return `${hours}h ${minutes}m (ongoing)`;
  }

  const start = new Date(todayAttendance.value.check_in_time);
  const end = new Date(todayAttendance.value.check_out_time);
  const diff = end.getTime() - start.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${hours}h ${minutes}m`;
};

const calculateDuration = (attendance: AttendanceDTO) => {
  if (!attendance.check_out_time) return "-";
  
  const start = new Date(attendance.check_in_time);
  const end = new Date(attendance.check_out_time);
  const diff = end.getTime() - start.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${hours}h ${minutes}m`;
};

const getStatusType = (status: string) => {
  switch (status) {
    case "checked_out":
      return "success";
    case "late":
      return "warning";
    case "early_leave":
      return "danger";
    case "checked_in":
      return "primary";
    default:
      return "info";
  }
};

const requestLocationPermission = async () => {
  isCheckingPermission.value = true;
  await checkLocationPermission();
  isCheckingPermission.value = false;
};

const retryLocationPermission = async () => {
  isCheckingPermission.value = true;
  
  try {
    currentPosition.value = await getCurrentLocation();
    locationDenied.value = false;
    ElMessage.success("Location access granted!");
  } catch (error: any) {
    await checkLocationPermission();
    if (locationDenied.value) {
      ElMessage.error("Location access is still denied. Please enable it in your browser settings.");
    }
  } finally {
    isCheckingPermission.value = false;
  }
};

// Load attendance history
const loadAttendanceHistory = async () => {
  try {
    historyLoading.value = true;
    const [startDate, endDate] = dateRange.value;
    
    const response = await $hrAttendanceService.getMyAttendanceHistory({
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0],
      page: historyPage.value,
      limit: historyPageSize.value,
    });
    
    attendanceHistory.value = response.items;
    historyTotal.value = response.total;
  } catch (error: any) {
    console.error("Failed to load attendance history:", error);
    ElMessage.error("Failed to load attendance history");
  } finally {
    historyLoading.value = false;
  }
};

// Load statistics
const loadStats = async () => {
  try {
    statsLoading.value = true;
    const [startDate, endDate] = dateRange.value;
    
    stats.value = await $hrAttendanceService.getMyAttendanceStats({
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0],
    });
  } catch (error: any) {
    console.error("Failed to load statistics:", error);
  } finally {
    statsLoading.value = false;
  }
};

// Handle date range change
const handleDateRangeChange = () => {
  historyPage.value = 1;
  loadAttendanceHistory();
  loadStats();
};

// Handle page change
const handlePageChange = (page: number) => {
  historyPage.value = page;
  loadAttendanceHistory();
};

// Update current time every second
let timeInterval: NodeJS.Timeout | null = null;
const updateCurrentTime = () => {
  currentTime.value = new Date();
};

// Lifecycle
onMounted(() => {
  loadTodayAttendance();
  requestLocationPermission();
  loadAttendanceHistory();
  
  // Update time every second
  timeInterval = setInterval(updateCurrentTime, 1000);
});

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval);
  }
});
</script>

<template>
  <div>
    <OverviewHeader
      title="Attendance Management"
      :description="`${formatDate(new Date().toISOString())} - ${currentTime.toLocaleTimeString()}`"
    >
      <template #actions>
        <BaseButton
          plain
          :loading="loading"
          @click="loadTodayAttendance"
        >
          Refresh
        </BaseButton>
      </template>
    </OverviewHeader>

    <div class="content-wrapper">
      <!-- Tabs -->
      <el-tabs v-model="activeTab" class="mb-4">
        <el-tab-pane label="Check In/Out" name="check-in">
          <el-row :gutter="16">
            <!-- Status Card -->
            <el-col :xs="24" :sm="24" :md="12">
              <el-card shadow="hover">
                <template #header>
                  <div class="flex items-center justify-between">
                    <span class="font-semibold">Today's Status</span>
                    <el-tag :type="statusColor" size="large">
                      <el-icon class="mr-1">
                        <component :is="statusIcon" />
                      </el-icon>
                      {{ statusText }}
                    </el-tag>
                  </div>
                </template>

                <div v-if="todayAttendance" class="space-y-4">
                  <div>
                    <div class="text-sm text-[color:var(--el-text-color-secondary)]">Check In Time</div>
                    <div class="text-lg font-semibold">
                      {{ formatTime(todayAttendance.check_in_time) }}
                    </div>
                    <div v-if="todayAttendance.late_minutes > 0" class="text-sm text-[color:var(--el-color-warning)]">
                      <el-icon><Warning /></el-icon>
                      Late by {{ todayAttendance.late_minutes }} minutes
                    </div>
                  </div>

                  <div v-if="todayAttendance.check_out_time">
                    <div class="text-sm text-[color:var(--el-text-color-secondary)]">Check Out Time</div>
                    <div class="text-lg font-semibold">
                      {{ formatTime(todayAttendance.check_out_time) }}
                    </div>
                    <div v-if="todayAttendance.early_leave_minutes > 0" class="text-sm text-[color:var(--el-color-warning)]">
                      <el-icon><Warning /></el-icon>
                      Left {{ todayAttendance.early_leave_minutes }} minutes early
                    </div>
                  </div>

                  <div>
                    <div class="text-sm text-[color:var(--el-text-color-secondary)]">Work Duration</div>
                    <div class="text-lg font-semibold text-[color:var(--el-color-primary)]">
                      {{ getWorkDuration() }}
                    </div>
                  </div>

                  <div v-if="todayAttendance.notes">
                    <div class="text-sm text-[color:var(--el-text-color-secondary)]">Notes</div>
                    <div class="text-sm">{{ todayAttendance.notes }}</div>
                  </div>

                  <!-- Location Info -->
                  <div v-if="todayAttendance.check_in_latitude && todayAttendance.check_in_longitude">
                    <div class="text-sm text-[color:var(--el-text-color-secondary)]">
                      <el-icon><Location /></el-icon>
                      Check-In Location
                    </div>
                    <div class="text-xs text-[color:var(--el-text-color-regular)]">
                      {{ todayAttendance.check_in_latitude.toFixed(6) }}, {{ todayAttendance.check_in_longitude.toFixed(6) }}
                    </div>
                  </div>

                  <div v-if="todayAttendance.check_out_latitude && todayAttendance.check_out_longitude">
                    <div class="text-sm text-[color:var(--el-text-color-secondary)]">
                      <el-icon><Location /></el-icon>
                      Check-Out Location
                    </div>
                    <div class="text-xs text-[color:var(--el-text-color-regular)]">
                      {{ todayAttendance.check_out_latitude.toFixed(6) }}, {{ todayAttendance.check_out_longitude.toFixed(6) }}
                    </div>
                  </div>
                </div>

                <div v-else class="text-center py-8 text-[color:var(--el-text-color-placeholder)]">
                  <el-icon :size="48">
                    <Clock />
                  </el-icon>
                  <p class="mt-2">You haven't checked in today</p>
                </div>
              </el-card>
            </el-col>

            <!-- Action Card -->
            <el-col :xs="24" :sm="24" :md="12">
              <el-card shadow="hover">
                <template #header>
                  <span class="font-semibold">
                    {{ isCheckedIn && !isCheckedOut ? "Check Out" : "Check In" }}
                  </span>
                </template>

                <!-- Location Permission Alert -->
                <el-alert
                  v-if="locationDenied"
                  type="error"
                  :closable="false"
                  show-icon
                  class="mb-4"
                >
                  <template #title>
                    Location Access Required
                  </template>
                  <div class="text-sm">
                    <p class="mb-2">
                      You must enable location access to check in/out. Please allow location permissions in your browser settings.
                    </p>
                    <BaseButton
                      type="primary"
                      size="small"
                      :loading="isCheckingPermission"
                      @click="retryLocationPermission"
                    >
                      Try Again
                    </BaseButton>
                  </div>
                </el-alert>

                <el-form label-position="top">
                  <!-- Check-In Progress -->
                  <div v-if="checkInProgress > 0 && !isCheckedIn" class="mb-4">
                    <div class="text-sm text-[color:var(--el-text-color-secondary)] mb-2">
                      Checking in...
                    </div>
                    <el-progress
                      :percentage="checkInProgress"
                      :status="checkInProgress === 100 ? 'success' : undefined"
                      :stroke-width="8"
                    />
                  </div>

                  <!-- Check-Out Progress -->
                  <div v-if="checkOutProgress > 0 && isCheckedIn && !isCheckedOut" class="mb-4">
                    <div class="text-sm text-[color:var(--el-text-color-secondary)] mb-2">
                      Checking out...
                    </div>
                    <el-progress
                      :percentage="checkOutProgress"
                      :status="checkOutProgress === 100 ? 'success' : undefined"
                      :stroke-width="8"
                    />
                  </div>

                  <!-- Notes -->
                  <el-form-item label="Notes (Optional)">
                    <el-input
                      v-model="notes"
                      type="textarea"
                      :rows="3"
                      placeholder="Add any notes..."
                      :disabled="isCheckedOut || locationDenied"
                      maxlength="500"
                      show-word-limit
                    />
                  </el-form-item>

                  <!-- Action Buttons -->
                  <el-form-item>
                    <BaseButton
                      v-if="canCheckIn"
                      type="primary"
                      :loading="loading"
                      :disabled="locationDenied"
                      class="w-full"
                      @click="handleCheckIn"
                    >
                      <el-icon class="mr-2"><Clock /></el-icon>
                      Check In Now
                    </BaseButton>

                    <BaseButton
                      v-else-if="canCheckOut"
                      type="success"
                      :loading="loading"
                      :disabled="locationDenied"
                      class="w-full"
                      @click="handleCheckOut"
                    >
                      <el-icon class="mr-2"><Check /></el-icon>
                      Check Out Now
                    </BaseButton>

                    <el-alert
                      v-else-if="isCheckedOut"
                      type="success"
                      :closable="false"
                      show-icon
                    >
                      You have completed your attendance for today
                    </el-alert>

                    <el-alert
                      v-else-if="locationDenied && !isCheckedOut"
                      type="warning"
                      :closable="false"
                      show-icon
                    >
                      Enable location access to check in/out
                    </el-alert>
                  </el-form-item>
                </el-form>

                <el-divider />

                <div class="text-xs text-[color:var(--el-text-color-secondary)] flex items-center gap-2">
                  <el-icon><InfoFilled /></el-icon>
                  <span>Your GPS location is required and will be recorded for attendance verification</span>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>

        <el-tab-pane label="Attendance History" name="history">
          <!-- Statistics Cards -->
          <el-row :gutter="16" class="mb-4">
            <el-col :xs="12" :sm="6">
              <el-card shadow="hover">
                <div class="stat-card">
                  <div class="stat-icon" style="background: var(--el-color-primary-light-9)">
                    <el-icon :size="24" color="var(--el-color-primary)">
                      <Calendar />
                    </el-icon>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ stats?.present_days || 0 }}</div>
                    <div class="stat-label">Present Days</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :xs="12" :sm="6">
              <el-card shadow="hover">
                <div class="stat-card">
                  <div class="stat-icon" style="background: var(--el-color-warning-light-9)">
                    <el-icon :size="24" color="var(--el-color-warning)">
                      <Warning />
                    </el-icon>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ stats?.late_days || 0 }}</div>
                    <div class="stat-label">Late Days</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :xs="12" :sm="6">
              <el-card shadow="hover">
                <div class="stat-card">
                  <div class="stat-icon" style="background: var(--el-color-danger-light-9)">
                    <el-icon :size="24" color="var(--el-color-danger)">
                      <Timer />
                    </el-icon>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ stats?.total_late_minutes || 0 }}</div>
                    <div class="stat-label">Late Minutes</div>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :xs="12" :sm="6">
              <el-card shadow="hover">
                <div class="stat-card">
                  <div class="stat-icon" style="background: var(--el-color-success-light-9)">
                    <el-icon :size="24" color="var(--el-color-success)">
                      <TrendCharts />
                    </el-icon>
                  </div>
                  <div class="stat-content">
                    <div class="stat-value">{{ stats?.attendance_rate.toFixed(1) || 0 }}%</div>
                    <div class="stat-label">Attendance Rate</div>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>

          <!-- Filters -->
          <el-card shadow="hover" class="mb-4">
            <el-form inline>
              <el-form-item label="Date Range">
                <el-date-picker
                  v-model="dateRange"
                  type="daterange"
                  range-separator="To"
                  start-placeholder="Start date"
                  end-placeholder="End date"
                  @change="handleDateRangeChange"
                />
              </el-form-item>
              <el-form-item>
                <BaseButton @click="handleDateRangeChange">
                  Apply Filter
                </BaseButton>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- Attendance Table -->
          <el-card shadow="hover">
            <el-table
              :data="attendanceHistory"
              v-loading="historyLoading"
              stripe
              style="width: 100%"
            >
              <el-table-column prop="check_in_time" label="Date" width="120">
                <template #default="{ row }">
                  {{ new Date(row.check_in_time).toLocaleDateString() }}
                </template>
              </el-table-column>
              <el-table-column prop="check_in_time" label="Check In" width="100">
                <template #default="{ row }">
                  {{ formatTime(row.check_in_time) }}
                </template>
              </el-table-column>
              <el-table-column prop="check_out_time" label="Check Out" width="100">
                <template #default="{ row }">
                  {{ row.check_out_time ? formatTime(row.check_out_time) : '-' }}
                </template>
              </el-table-column>
              <el-table-column label="Duration" width="120">
                <template #default="{ row }">
                  {{ calculateDuration(row) }}
                </template>
              </el-table-column>
              <el-table-column prop="late_minutes" label="Late" width="80">
                <template #default="{ row }">
                  <el-tag v-if="row.late_minutes > 0" type="warning" size="small">
                    {{ row.late_minutes }}m
                  </el-tag>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column prop="early_leave_minutes" label="Early Leave" width="100">
                <template #default="{ row }">
                  <el-tag v-if="row.early_leave_minutes > 0" type="danger" size="small">
                    {{ row.early_leave_minutes }}m
                  </el-tag>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="Status" width="120">
                <template #default="{ row }">
                  <el-tag
                    :type="getStatusType(row.status)"
                    size="small"
                  >
                    {{ row.status.replace('_', ' ').toUpperCase() }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="notes" label="Notes" min-width="150">
                <template #default="{ row }">
                  {{ row.notes || '-' }}
                </template>
              </el-table-column>
            </el-table>

            <!-- Pagination -->
            <div class="mt-4 flex justify-end">
              <el-pagination
                v-model:current-page="historyPage"
                :page-size="historyPageSize"
                :total="historyTotal"
                layout="total, prev, pager, next"
                @current-change="handlePageChange"
              />
            </div>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<style scoped>
.content-wrapper {
  margin-top: 16px;
}

.space-y-4 > * + * {
  margin-top: 16px;
}

.flex {
  display: flex;
}

.items-center {
  align-items: center;
}

.justify-between {
  justify-content: space-between;
}

.justify-end {
  justify-content: flex-end;
}

.gap-2 {
  gap: 8px;
}

.font-semibold {
  font-weight: 600;
}

.text-sm {
  font-size: 14px;
}

.text-xs {
  font-size: 12px;
}

.text-lg {
  font-size: 18px;
}

.text-center {
  text-align: center;
}

.py-8 {
  padding-top: 32px;
  padding-bottom: 32px;
}

.mt-2 {
  margin-top: 8px;
}

.mt-4 {
  margin-top: 16px;
}

.mr-1 {
  margin-right: 4px;
}

.mr-2 {
  margin-right: 8px;
}

.mb-2 {
  margin-bottom: 8px;
}

.mb-4 {
  margin-bottom: 16px;
}

.w-full {
  width: 100%;
}

/* Statistics Card Styles */
.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  line-height: 1.2;
  color: var(--el-text-color-primary);
}

.stat-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 4px;
}
</style>
