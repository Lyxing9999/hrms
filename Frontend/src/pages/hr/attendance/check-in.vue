<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useNuxtApp } from "nuxt/app";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import type { AttendanceDTO } from "~/api/hr_admin/attendance/attendance.dto";
import type { WorkLocationDTO } from "~/api/hr_admin/location/location.dto";
import { ElMessage } from "element-plus";

const { $hrAttendanceService, $hrLocationService } = useNuxtApp();

const loading = ref(false);
const locationLoading = ref(false);
const todayAttendance = ref<AttendanceDTO | null>(null);
const locations = ref<WorkLocationDTO[]>([]);
const selectedLocationId = ref<string>("");
const currentPosition = ref<{ latitude: number; longitude: number } | null>(null);
const notes = ref("");

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

const getCurrentLocation = (): Promise<{ latitude: number; longitude: number }> => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error("Geolocation is not supported by your browser"));
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
        reject(error);
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

const loadLocations = async () => {
  try {
    locationLoading.value = true;
    const res = await $hrLocationService.getLocations({
      is_active: true,
      page: 1,
      limit: 100,
    });
    locations.value = res.items || [];
    if (locations.value.length > 0) {
      selectedLocationId.value = locations.value[0].id;
    }
  } catch (error: any) {
    ElMessage.error("Failed to load work locations");
  } finally {
    locationLoading.value = false;
  }
};

const handleCheckIn = async () => {
  try {
    loading.value = true;
    
    // Get current location
    try {
      currentPosition.value = await getCurrentLocation();
    } catch (error: any) {
      ElMessage.warning("Could not get GPS location. Checking in without location.");
    }

    const data = {
      location_id: selectedLocationId.value || undefined,
      latitude: currentPosition.value?.latitude,
      longitude: currentPosition.value?.longitude,
      notes: notes.value || undefined,
    };

    todayAttendance.value = await $hrAttendanceService.checkIn(data);
    ElMessage.success("Checked in successfully!");
    notes.value = "";
  } catch (error: any) {
    ElMessage.error(error.message || "Failed to check in");
  } finally {
    loading.value = false;
  }
};

const handleCheckOut = async () => {
  if (!todayAttendance.value) return;

  try {
    loading.value = true;
    
    // Get current location
    try {
      currentPosition.value = await getCurrentLocation();
    } catch (error: any) {
      ElMessage.warning("Could not get GPS location. Checking out without location.");
    }

    const data = {
      latitude: currentPosition.value?.latitude,
      longitude: currentPosition.value?.longitude,
      notes: notes.value || undefined,
    };

    todayAttendance.value = await $hrAttendanceService.checkOut(
      todayAttendance.value.id,
      data
    );
    ElMessage.success("Checked out successfully!");
    notes.value = "";
  } catch (error: any) {
    ElMessage.error(error.message || "Failed to check out");
  } finally {
    loading.value = false;
  }
};

const formatTime = (dateStr: string | null) => {
  if (!dateStr) return "-";
  return new Date(dateStr).toLocaleTimeString();
};

onMounted(() => {
  loadTodayAttendance();
  loadLocations();
});
</script>

<template>
  <OverviewHeader
    :title="'Check In / Check Out'"
    :description="'Record your attendance with location verification'"
    :backPath="'/hr/attendance'"
  />

  <el-row :gutter="16" class="mt-4">
    <!-- Status Card -->
    <el-col :span="12">
      <el-card>
        <template #header>
          <div class="flex items-center justify-between">
            <span class="font-semibold">Today's Status</span>
            <el-tag :type="statusColor" size="large">{{ statusText }}</el-tag>
          </div>
        </template>

        <div v-if="todayAttendance" class="space-y-4">
          <div>
            <div class="text-sm text-gray-500">Check In Time</div>
            <div class="text-lg font-semibold">
              {{ formatTime(todayAttendance.check_in_time) }}
            </div>
            <div v-if="todayAttendance.late_minutes > 0" class="text-sm text-orange-500">
              Late by {{ todayAttendance.late_minutes }} minutes
            </div>
          </div>

          <div v-if="todayAttendance.check_out_time">
            <div class="text-sm text-gray-500">Check Out Time</div>
            <div class="text-lg font-semibold">
              {{ formatTime(todayAttendance.check_out_time) }}
            </div>
            <div v-if="todayAttendance.early_leave_minutes > 0" class="text-sm text-orange-500">
              Left {{ todayAttendance.early_leave_minutes }} minutes early
            </div>
          </div>

          <div v-if="todayAttendance.notes">
            <div class="text-sm text-gray-500">Notes</div>
            <div class="text-sm">{{ todayAttendance.notes }}</div>
          </div>
        </div>

        <div v-else class="text-center py-8 text-gray-400">
          <el-icon :size="48">
            <Clock />
          </el-icon>
          <p class="mt-2">You haven't checked in today</p>
        </div>
      </el-card>
    </el-col>

    <!-- Check In/Out Form -->
    <el-col :span="12">
      <el-card>
        <template #header>
          <span class="font-semibold">
            {{ isCheckedIn && !isCheckedOut ? "Check Out" : "Check In" }}
          </span>
        </template>

        <el-form label-position="top">
          <el-form-item v-if="!isCheckedIn" label="Work Location">
            <el-select
              v-model="selectedLocationId"
              placeholder="Select location"
              :loading="locationLoading"
              class="w-full"
            >
              <el-option
                v-for="loc in locations"
                :key="loc.id"
                :label="loc.name"
                :value="loc.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="Notes (Optional)">
            <el-input
              v-model="notes"
              type="textarea"
              :rows="3"
              placeholder="Add any notes..."
              :disabled="isCheckedOut"
            />
          </el-form-item>

          <el-form-item>
            <BaseButton
              v-if="!isCheckedIn"
              type="primary"
              :loading="loading"
              class="w-full"
              @click="handleCheckIn"
            >
              <el-icon class="mr-2"><Clock /></el-icon>
              Check In Now
            </BaseButton>

            <BaseButton
              v-else-if="!isCheckedOut"
              type="success"
              :loading="loading"
              class="w-full"
              @click="handleCheckOut"
            >
              <el-icon class="mr-2"><Check /></el-icon>
              Check Out Now
            </BaseButton>

            <el-alert
              v-else
              type="success"
              :closable="false"
              show-icon
            >
              You have completed your attendance for today
            </el-alert>
          </el-form-item>
        </el-form>

        <el-divider />

        <div class="text-xs text-gray-500">
          <el-icon><InfoFilled /></el-icon>
          Your GPS location will be recorded for verification
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>
