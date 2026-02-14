<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useNuxtApp } from "nuxt/app";
import { ElMessage, ElTag } from "element-plus";
import { io, Socket } from "socket.io-client";
import OverviewHeader from "~/components/overview/OverviewHeader.vue";
import BaseButton from "~/components/base/BaseButton.vue";
import { Location, User, Clock, Refresh, MapLocation, Search } from "@element-plus/icons-vue";
import { useAuthStore } from "~/stores/authStore";

// Types
interface EmployeeLocation {
  employee_id: string;
  employee_name: string;
  employee_code: string;
  department: string;
  position: string;
  lat: number;
  lng: number;
  accuracy: number;
  distance_from_office_m: number;
  status: "active" | "inactive";
  photo_url: string;
  shift_started_at: string;
  last_seen_at: string;
}

const nuxtApp = useNuxtApp();
const authStore = useAuthStore();

// State
const socket = ref<Socket | null>(null);
const employees = ref<Map<string, EmployeeLocation>>(new Map());
const selectedEmployee = ref<string | null>(null);
const mapContainer = ref<HTMLElement | null>(null);
const map = ref<any>(null);
const markers = ref<Map<string, any>>(new Map());
const loading = ref(true);
const connected = ref(false);
const searchQuery = ref("");
const statusFilter = ref<"all" | "active" | "inactive">("active");
const departmentFilter = ref<string>("all");
const currentUserId = ref<string>("");
const userLocation = ref<{ lat: number; lng: number } | null>(null);
const userLocationMarker = ref<any>(null);
const gettingLocation = ref(false);

// Office location - PPIU (Phnom Penh International University, 169 Czech Republic Blvd)
const OFFICE_LAT = 11.5563;
const OFFICE_LNG = 104.9282;
const GEOFENCE_RADIUS = 150;

// Get current user
currentUserId.value = authStore.user?.id || "";

// Computed
const activeEmployees = computed(() => {
  return Array.from(employees.value.values()).filter(emp => emp.status === "active");
});

const filteredEmployees = computed(() => {
  let filtered = Array.from(employees.value.values());
  
  // Status filter
  if (statusFilter.value !== "all") {
    filtered = filtered.filter(emp => emp.status === statusFilter.value);
  }
  
  // Department filter
  if (departmentFilter.value !== "all") {
    filtered = filtered.filter(emp => emp.department === departmentFilter.value);
  }
  
  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(emp => 
      emp.employee_name?.toLowerCase().includes(query) ||
      emp.employee_code?.toLowerCase().includes(query) ||
      emp.department?.toLowerCase().includes(query)
    );
  }
  
  return filtered;
});

const departments = computed(() => {
  const depts = new Set<string>();
  employees.value.forEach(emp => {
    if (emp.department) depts.add(emp.department);
  });
  return Array.from(depts).sort();
});

const selectedEmployeeData = computed(() => {
  if (!selectedEmployee.value) return null;
  return employees.value.get(selectedEmployee.value);
});

// Methods
const initSocket = () => {
  const socketUrl = "http://localhost:5000";
  
  // Set loading to false after timeout if connection fails
  const connectionTimeout = setTimeout(() => {
    if (!connected.value) {
      loading.value = false;
      ElMessage.error("Failed to connect to live tracking server");
    }
  }, 10000); // 10 second timeout
  
  socket.value = io(socketUrl, {
    transports: ["websocket", "polling"],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 5,
  });
  
  socket.value.on("connect", () => {
    console.log("✅ Socket connected");
    connected.value = true;
    clearTimeout(connectionTimeout);
    
    // Join manager room
    const managerId = authStore.user?.id || "manager_1";
    socket.value?.emit("manager:join", { manager_id: managerId });
  });
  
  socket.value.on("connect_error", (error) => {
    console.error("❌ Socket connection error:", error);
    loading.value = false;
    clearTimeout(connectionTimeout);
    ElMessage.error("Cannot connect to live tracking server. Please check if backend is running.");
  });

  socket.value.on("manager:joined", (data: any) => {
    console.log("✅ Joined managers room:", data);
    loading.value = false;
    
    // Load initial active employees
    if (data.active_employees && Array.isArray(data.active_employees)) {
      data.active_employees.forEach((emp: EmployeeLocation) => {
        updateEmployee(emp);
      });
    }
    
    ElMessage.success("Connected to live tracking");
  });
  
  socket.value.on("employee:location", (data: EmployeeLocation) => {
    console.log("📍 Employee location update:", data);
    updateEmployee(data);
  });
  
  socket.value.on("error", (error: any) => {
    console.error("❌ Socket error:", error);
    ElMessage.error(error.message || "Socket error occurred");
  });
  
  socket.value.on("disconnect", () => {
    console.log("⚠️ Socket disconnected");
    connected.value = false;
  });
};

const updateEmployee = (data: EmployeeLocation) => {
  employees.value.set(data.employee_id, data);
  
  // Update or create marker on map
  if (map.value) {
    updateMarker(data);
  }
  
  // Remove inactive employees after 30 seconds
  if (data.status === "inactive") {
    setTimeout(() => {
      const emp = employees.value.get(data.employee_id);
      if (emp && emp.status === "inactive") {
        removeEmployee(data.employee_id);
      }
    }, 30000);
  }
};

const removeEmployee = (employeeId: string) => {
  employees.value.delete(employeeId);
  
  // Remove marker
  const marker = markers.value.get(employeeId);
  if (marker && map.value) {
    map.value.removeLayer(marker);
    markers.value.delete(employeeId);
  }
  
  // Clear selection if this employee was selected
  if (selectedEmployee.value === employeeId) {
    selectedEmployee.value = null;
  }
};

const initMap = async () => {
  try {
    // Load Leaflet dynamically
    if (typeof window !== "undefined" && !(window as any).L) {
      // Load CSS
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
      document.head.appendChild(link);
      
      // Load JS
      await new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
        
        // Timeout after 10 seconds
        setTimeout(() => reject(new Error("Leaflet loading timeout")), 10000);
      });
    }
    
    if (!mapContainer.value) {
      console.error("Map container not found");
      return;
    }
    
    const L = (window as any).L;
    
    // Create map
    map.value = L.map(mapContainer.value).setView([OFFICE_LAT, OFFICE_LNG], 15);
    
    // Add tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map.value);
    
    // Add office marker
    const officeIcon = L.divIcon({
      className: "office-marker",
      html: `<div style="background: #4CAF50; width: 40px; height: 40px; border-radius: 50%; border: 4px solid white; box-shadow: 0 3px 8px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 18px;">🏢</div>`,
      iconSize: [40, 40],
      iconAnchor: [20, 40],
    });
    
    L.marker([OFFICE_LAT, OFFICE_LNG], { icon: officeIcon })
      .addTo(map.value)
      .bindPopup("<b>PPIU - Phnom Penh International University</b><br>169 Czech Republic Blvd, Phnom Penh");
    
    // Add geofence circle
    L.circle([OFFICE_LAT, OFFICE_LNG], {
      color: "#4CAF50",
      fillColor: "#4CAF50",
      fillOpacity: 0.1,
      radius: GEOFENCE_RADIUS,
    }).addTo(map.value);
    
    console.log("✅ Map initialized successfully");
  } catch (error) {
    console.error("❌ Failed to initialize map:", error);
    ElMessage.error("Failed to load map. Please refresh the page.");
  }
};

const updateMarker = (data: EmployeeLocation) => {
  if (!map.value) return;
  
  const L = (window as any).L;
  const existingMarker = markers.value.get(data.employee_id);
  
  if (existingMarker) {
    // Update existing marker
    existingMarker.setLatLng([data.lat, data.lng]);
    existingMarker.setPopupContent(createPopupContent(data));
    existingMarker.setOpacity(data.status === "active" ? 1.0 : 0.5);
  } else {
    // Create new marker
    const icon = createEmployeeIcon(data);
    const marker = L.marker([data.lat, data.lng], { icon })
      .addTo(map.value)
      .bindPopup(createPopupContent(data));
    
    marker.on("click", () => {
      selectedEmployee.value = data.employee_id;
    });
    
    markers.value.set(data.employee_id, marker);
  }
};

const createEmployeeIcon = (data: EmployeeLocation) => {
  const L = (window as any).L;
  const color = data.status === "active" ? "#2196F3" : "#9E9E9E";
  const initial = (data.employee_name || "E").charAt(0).toUpperCase();
  
  return L.divIcon({
    className: "employee-marker",
    html: `
      <div style="position: relative;">
        <div style="
          background: ${color};
          width: 50px;
          height: 50px;
          border-radius: 50%;
          border: 3px solid white;
          box-shadow: 0 3px 8px rgba(0,0,0,0.4);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-weight: bold;
          font-size: 18px;
        ">
          ${initial}
        </div>
        ${data.status === "active" ? '<div style="position: absolute; top: -2px; right: -2px; width: 14px; height: 14px; background: #4CAF50; border: 2px solid white; border-radius: 50%; animation: pulse 2s infinite;"></div>' : ''}
      </div>
    `,
    iconSize: [50, 50],
    iconAnchor: [25, 50],
  });
};

const createPopupContent = (data: EmployeeLocation) => {
  const lastSeen = data.last_seen_at ? new Date(data.last_seen_at).toLocaleTimeString() : "Unknown";
  const shiftStarted = data.shift_started_at ? new Date(data.shift_started_at).toLocaleTimeString() : "N/A";
  const duration = data.shift_started_at ? calculateDuration(data.shift_started_at) : "N/A";
  const photoUrl = data.photo_url || '';
  const accuracyColor = data.accuracy < 50 ? '#4CAF50' : data.accuracy < 100 ? '#FF9800' : '#F44336';
  const distanceColor = data.distance_from_office_m < 50 ? '#4CAF50' : data.distance_from_office_m < 100 ? '#FF9800' : '#F44336';
  
  return `
    <div style="min-width: 280px; font-family: system-ui;">
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
        ${photoUrl ? `
          <img src="${photoUrl}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 2px solid #ddd;">
        ` : `
          <div style="width: 60px; height: 60px; border-radius: 50%; background: #2196F3; color: white; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; border: 2px solid #ddd;">
            ${(data.employee_name || 'E').charAt(0).toUpperCase()}
          </div>
        `}
        <div>
          <h3 style="margin: 0; color: #333; font-size: 16px;">${data.employee_name || "Unknown"}</h3>
          <div style="font-size: 12px; color: #666;">${data.employee_code || "N/A"}</div>
        </div>
      </div>
      
      <div style="display: grid; gap: 8px; font-size: 13px; border-top: 1px solid #eee; padding-top: 12px;">
        <div style="display: flex; justify-content: space-between;">
          <strong>Department:</strong>
          <span>${data.department || "N/A"}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <strong>Position:</strong>
          <span>${data.position || "N/A"}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <strong>Status:</strong>
          <span style="color: ${data.status === "active" ? "#4CAF50" : "#9E9E9E"}; font-weight: bold;">
            ${data.status.toUpperCase()}
          </span>
        </div>
      </div>
      
      <div style="display: grid; gap: 8px; font-size: 13px; border-top: 1px solid #eee; padding-top: 12px; margin-top: 12px;">
        <div style="display: flex; justify-content: space-between;">
          <strong>Shift Started:</strong>
          <span>${shiftStarted}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <strong>Duration:</strong>
          <span style="color: #2196F3; font-weight: 600;">${duration}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <strong>Last Seen:</strong>
          <span>${lastSeen}</span>
        </div>
      </div>
      
      <div style="display: grid; gap: 8px; font-size: 13px; border-top: 1px solid #eee; padding-top: 12px; margin-top: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <strong>GPS Accuracy:</strong>
          <span style="color: ${accuracyColor}; font-weight: 600;">
            ${data.accuracy?.toFixed(0)}m
            ${data.accuracy < 50 ? '✓' : data.accuracy < 100 ? '⚠' : '✗'}
          </span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <strong>Distance from Office:</strong>
          <span style="color: ${distanceColor}; font-weight: 600;">
            ${data.distance_from_office_m?.toFixed(0)}m
            ${data.distance_from_office_m < 50 ? '✓' : data.distance_from_office_m < 100 ? '⚠' : '✗'}
          </span>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <strong>Coordinates:</strong>
          <span style="font-size: 11px; color: #666;">
            ${data.lat.toFixed(6)}, ${data.lng.toFixed(6)}
          </span>
        </div>
      </div>
      
      ${data.status === 'active' ? `
        <div style="margin-top: 12px; padding: 8px; background: #E3F2FD; border-radius: 4px; font-size: 12px; text-align: center; color: #1976D2;">
          🟢 Currently Active
        </div>
      ` : `
        <div style="margin-top: 12px; padding: 8px; background: #F5F5F5; border-radius: 4px; font-size: 12px; text-align: center; color: #757575;">
          ⚫ Shift Ended
        </div>
      `}
    </div>
  `;
};

const calculateDuration = (startTime: string): string => {
  const start = new Date(startTime);
  const now = new Date();
  const diff = now.getTime() - start.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${hours}h ${minutes}m`;
};

const focusEmployee = (employeeId: string) => {
  selectedEmployee.value = employeeId;
  const employee = employees.value.get(employeeId);
  
  if (employee && map.value) {
    map.value.setView([employee.lat, employee.lng], 17);
    const marker = markers.value.get(employeeId);
    if (marker) {
      marker.openPopup();
    }
  }
};

const resetMapView = () => {
  if (map.value) {
    map.value.setView([OFFICE_LAT, OFFICE_LNG], 15);
  }
};

const refreshData = () => {
  if (socket.value && socket.value.connected) {
    ElMessage.info("Refreshing data...");
    socket.value.disconnect();
    socket.value.connect();
  }
};

const formatTime = (dateStr: string | null) => {
  if (!dateStr) return "-";
  return new Date(dateStr).toLocaleTimeString();
};

const getStatusColor = (status: string) => {
  return status === "active" ? "success" : "info";
};

const getAccuracyColor = (accuracy: number) => {
  if (accuracy < 50) return "#4CAF50"; // Good
  if (accuracy < 100) return "#FF9800"; // Fair
  return "#F44336"; // Poor
};

const getDistanceColor = (distance: number) => {
  if (distance < 50) return "#4CAF50"; // Very close
  if (distance < 100) return "#FF9800"; // Close
  return "#F44336"; // Far
};

const showMyLocation = async () => {
  gettingLocation.value = true;
  
  try {
    if (!navigator.geolocation) {
      ElMessage.error("Geolocation is not supported by your browser");
      return;
    }
    
    const position = await new Promise<GeolocationPosition>((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject, {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      });
    });
    
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;
    const accuracy = position.coords.accuracy;
    
    userLocation.value = { lat, lng };
    
    if (!map.value) {
      ElMessage.error("Map not initialized");
      return;
    }
    
    const L = (window as any).L;
    
    // Remove existing user location marker if any
    if (userLocationMarker.value) {
      map.value.removeLayer(userLocationMarker.value);
    }
    
    // Calculate distance from office
    const R = 6371e3; // Earth radius in meters
    const φ1 = (OFFICE_LAT * Math.PI) / 180;
    const φ2 = (lat * Math.PI) / 180;
    const Δφ = ((lat - OFFICE_LAT) * Math.PI) / 180;
    const Δλ = ((lng - OFFICE_LNG) * Math.PI) / 180;
    
    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = R * c;
    
    // Create user location icon
    const userIcon = L.divIcon({
      className: "user-location-marker",
      html: `
        <div style="position: relative;">
          <div style="
            background: #FF5722;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 3px 8px rgba(0,0,0,0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 20px;
          ">
            📍
          </div>
          <div style="position: absolute; top: -2px; right: -2px; width: 14px; height: 14px; background: #4CAF50; border: 2px solid white; border-radius: 50%; animation: pulse 2s infinite;"></div>
        </div>
      `,
      iconSize: [50, 50],
      iconAnchor: [25, 50],
    });
    
    // Add user location marker
    userLocationMarker.value = L.marker([lat, lng], { icon: userIcon })
      .addTo(map.value)
      .bindPopup(`
        <div style="min-width: 250px; font-family: system-ui;">
          <h3 style="margin: 0 0 12px 0; color: #FF5722; font-size: 16px;">📍 Your Location</h3>
          <div style="display: grid; gap: 8px; font-size: 13px;">
            <div style="display: flex; justify-content: space-between;">
              <strong>Coordinates:</strong>
              <span style="font-size: 11px; color: #666;">${lat.toFixed(6)}, ${lng.toFixed(6)}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <strong>GPS Accuracy:</strong>
              <span style="color: ${accuracy < 50 ? '#4CAF50' : accuracy < 100 ? '#FF9800' : '#F44336'}; font-weight: 600;">
                ${accuracy.toFixed(0)}m
              </span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <strong>Distance from PPIU:</strong>
              <span style="color: ${distance < 50 ? '#4CAF50' : distance < 100 ? '#FF9800' : '#F44336'}; font-weight: 600;">
                ${distance.toFixed(0)}m
              </span>
            </div>
            ${distance <= GEOFENCE_RADIUS ? `
              <div style="margin-top: 8px; padding: 8px; background: #E8F5E9; border-radius: 4px; font-size: 12px; text-align: center; color: #2E7D32;">
                ✓ Within office geofence
              </div>
            ` : `
              <div style="margin-top: 8px; padding: 8px; background: #FFEBEE; border-radius: 4px; font-size: 12px; text-align: center; color: #C62828;">
                ✗ Outside office geofence (${GEOFENCE_RADIUS}m)
              </div>
            `}
          </div>
        </div>
      `)
      .openPopup();
    
    // Add accuracy circle
    L.circle([lat, lng], {
      color: "#FF5722",
      fillColor: "#FF5722",
      fillOpacity: 0.1,
      radius: accuracy,
    }).addTo(map.value);
    
    // Center map on user location
    map.value.setView([lat, lng], 17);
    
    ElMessage.success(`Your location: ${distance.toFixed(0)}m from PPIU`);
    
  } catch (error: any) {
    let message = "Unable to get your location";
    if (error.code === 1) {
      message = "Location permission denied. Please enable location access in your browser.";
    } else if (error.code === 2) {
      message = "Location unavailable. Please try again.";
    } else if (error.code === 3) {
      message = "Location request timed out. Please try again.";
    }
    ElMessage.error(message);
    console.error("Geolocation error:", error);
  } finally {
    gettingLocation.value = false;
  }
};

// Lifecycle
onMounted(async () => {
  try {
    await initMap();
    initSocket();
  } catch (error) {
    console.error("Failed to initialize page:", error);
    loading.value = false;
    ElMessage.error("Failed to initialize live tracking page");
  }
});

onUnmounted(() => {
  if (socket.value) {
    socket.value.disconnect();
  }
});
</script>

<template>
  <div class="live-tracking-page">
    <OverviewHeader
      title="Live Employee Tracking"
      :description="`Monitoring ${activeEmployees.length} active employee${activeEmployees.length !== 1 ? 's' : ''}`"
    >
      <template #actions>
        <div class="header-actions">
          <el-tag v-if="currentUserId" type="info" size="small" class="user-tag">
            <el-icon><User /></el-icon>
            {{ authStore.user?.username || 'Manager' }}
          </el-tag>
          <BaseButton
            :icon="Refresh"
            :loading="!connected"
            @click="refreshData"
          >
            Refresh
          </BaseButton>
        </div>
      </template>
    </OverviewHeader>

    <div class="content-wrapper">
      <!-- Connection Status -->
      <el-alert
        v-if="!connected && !loading"
        type="warning"
        :closable="false"
        show-icon
        class="mb-4"
      >
        <template #title>
          Disconnected from live tracking server
        </template>
        Attempting to reconnect...
      </el-alert>

      <el-row :gutter="16">
        <!-- Map Section -->
        <el-col :xs="24" :lg="16">
          <el-card shadow="hover" class="map-card">
            <template #header>
              <div class="card-header">
                <span class="card-title">
                  <el-icon><MapLocation /></el-icon>
                  Live Location Map
                </span>
                <div class="map-actions">
                  <BaseButton
                    size="small"
                    plain
                    :loading="gettingLocation"
                    @click="showMyLocation"
                  >
                    <el-icon><Location /></el-icon>
                    My Location
                  </BaseButton>
                  <BaseButton
                    size="small"
                    plain
                    @click="resetMapView"
                  >
                    Reset View
                  </BaseButton>
                </div>
              </div>
            </template>
            
            <div
              ref="mapContainer"
              class="map-container"
              v-loading="loading"
            ></div>
          </el-card>
        </el-col>

        <!-- Employee List Section -->
        <el-col :xs="24" :lg="8">
          <el-card shadow="hover" class="employee-list-card">
            <template #header>
              <div class="card-header">
                <span class="card-title">
                  <el-icon><User /></el-icon>
                  Active Employees
                </span>
                <el-tag :type="connected ? 'success' : 'info'" size="small">
                  {{ connected ? 'Live' : 'Offline' }}
                </el-tag>
              </div>
            </template>

            <!-- Filters -->
            <div class="filters-section">
              <el-input
                v-model="searchQuery"
                placeholder="Search employees..."
                clearable
                class="mb-3"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>

              <el-row :gutter="8" class="mb-3">
                <el-col :span="12">
                  <el-select
                    v-model="statusFilter"
                    placeholder="Status"
                    style="width: 100%"
                    size="small"
                  >
                    <el-option label="All Status" value="all" />
                    <el-option label="Active" value="active" />
                    <el-option label="Inactive" value="inactive" />
                  </el-select>
                </el-col>
                <el-col :span="12">
                  <el-select
                    v-model="departmentFilter"
                    placeholder="Department"
                    style="width: 100%"
                    size="small"
                  >
                    <el-option label="All Departments" value="all" />
                    <el-option
                      v-for="dept in departments"
                      :key="dept"
                      :label="dept"
                      :value="dept"
                    />
                  </el-select>
                </el-col>
              </el-row>
            </div>

            <!-- Employee List -->
            <div class="employee-list" v-loading="loading">
              <div
                v-for="employee in filteredEmployees"
                :key="employee.employee_id"
                class="employee-item"
                :class="{ selected: selectedEmployee === employee.employee_id }"
                @click="focusEmployee(employee.employee_id)"
              >
                <div class="employee-avatar">
                  <img
                    v-if="employee.photo_url"
                    :src="employee.photo_url"
                    :alt="employee.employee_name"
                  />
                  <div v-else class="avatar-placeholder">
                    {{ (employee.employee_name || 'E').charAt(0).toUpperCase() }}
                  </div>
                  <div
                    v-if="employee.status === 'active'"
                    class="status-indicator active"
                  ></div>
                </div>

                <div class="employee-info">
                  <div class="employee-name">{{ employee.employee_name }}</div>
                  <div class="employee-meta">
                    <span class="employee-code">{{ employee.employee_code }}</span>
                    <el-tag
                      :type="getStatusColor(employee.status)"
                      size="small"
                    >
                      {{ employee.status }}
                    </el-tag>
                  </div>
                  <div class="employee-details">
                    <div class="detail-item">
                      <el-icon><Location /></el-icon>
                      <span :style="{ color: getDistanceColor(employee.distance_from_office_m) }">
                        {{ employee.distance_from_office_m?.toFixed(0) }}m from office
                      </span>
                      <span v-if="employee.distance_from_office_m < 50">✓</span>
                      <span v-else-if="employee.distance_from_office_m < 100">⚠</span>
                    </div>
                    <div class="detail-item">
                      <el-icon><Clock /></el-icon>
                      {{ formatTime(employee.last_seen_at) }}
                    </div>
                    <div class="detail-item" v-if="employee.accuracy">
                      <span style="font-size: 11px;">
                        GPS: {{ employee.accuracy.toFixed(0) }}m
                        <span :style="{ color: getAccuracyColor(employee.accuracy) }">
                          {{ employee.accuracy < 50 ? '●' : employee.accuracy < 100 ? '●' : '●' }}
                        </span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <el-empty
                v-if="filteredEmployees.length === 0 && !loading"
                description="No employees found"
              />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style scoped>
.live-tracking-page {
  padding: 0;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

.content-wrapper {
  margin-top: 16px;
  width: 100%;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.user-tag {
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.map-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;
}

.map-card {
  height: calc(100vh - 200px);
  min-height: 600px;
  overflow: hidden;
}

.map-card :deep(.el-card__body) {
  padding: 16px;
  height: calc(100% - 60px);
  overflow: hidden;
}

.map-container {
  width: 100%;
  height: 100%;
  min-height: 520px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.employee-list-card {
  height: calc(100vh - 200px);
  min-height: 600px;
  display: flex;
  flex-direction: column;
}

.employee-list-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 16px;
}

.filters-section {
  margin-bottom: 16px;
  flex-shrink: 0;
}

.employee-list {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-right: 4px;
}

.employee-list::-webkit-scrollbar {
  width: 6px;
}

.employee-list::-webkit-scrollbar-track {
  background: var(--el-fill-color-light);
  border-radius: 3px;
}

.employee-list::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 3px;
}

.employee-list::-webkit-scrollbar-thumb:hover {
  background: var(--el-border-color-dark);
}

.employee-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border: 1px solid var(--el-border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  background: var(--el-bg-color);
  min-width: 0;
}

.employee-item:hover {
  border-color: var(--el-color-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.employee-item.selected {
  border-color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
}

.employee-avatar {
  position: relative;
  width: 60px;
  height: 60px;
  flex-shrink: 0;
}

.employee-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--el-border-color);
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--el-color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  border: 2px solid var(--el-border-color);
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid white;
}

.status-indicator.active {
  background: #4CAF50;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(76, 175, 80, 0);
  }
}

.employee-info {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.employee-name {
  font-weight: 600;
  font-size: 15px;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.employee-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.employee-code {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.employee-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--el-text-color-regular);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.detail-item .el-icon {
  font-size: 14px;
  flex-shrink: 0;
}

.mb-3 {
  margin-bottom: 12px;
}

.mb-4 {
  margin-bottom: 16px;
}

/* Leaflet popup custom styles */
:deep(.leaflet-popup-content-wrapper) {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-width: 300px;
}

:deep(.leaflet-popup-content) {
  margin: 16px;
  max-width: 280px;
}

/* Mobile responsive */
@media (max-width: 992px) {
  .map-card,
  .employee-list-card {
    height: auto;
    min-height: 400px;
  }
  
  .map-container {
    height: 400px;
    min-height: 400px;
  }
  
  .employee-list {
    max-height: 500px;
  }
}

@media (max-width: 768px) {
  .employee-item {
    padding: 10px;
  }
  
  .employee-avatar {
    width: 50px;
    height: 50px;
  }
  
  .avatar-placeholder {
    font-size: 20px;
  }
}
</style>
