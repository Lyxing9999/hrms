<template>
  <div class="google-location-picker">
    <!-- Search Input -->
    <div class="mb-4">
      <el-input
        v-model="searchQuery"
        placeholder="Search for a place or address..."
        :prefix-icon="Search"
        clearable
        @keyup.enter="searchPlaces"
        @clear="clearSearch"
      >
        <template #append>
          <el-button @click="searchPlaces" :loading="isSearching">
            Search
          </el-button>
        </template>
      </el-input>
    </div>

    <!-- Current Location Button -->
    <div class="mb-4">
      <el-button
        @click="getCurrentLocation"
        :loading="isGettingLocation"
        :icon="Location"
        type="primary"
        plain
      >
        Use Current Location
      </el-button>
      
      <!-- Help text for geolocation -->
      <div class="geolocation-help mt-2">
        <el-text size="small" type="info">
          <el-icon><InfoFilled /></el-icon>
          Click to detect your location. You'll be asked to allow location access.
        </el-text>
      </div>
      
      <!-- Permission status indicator -->
      <div v-if="locationPermissionStatus" class="permission-status mt-1">
        <el-text 
          size="small" 
          :type="locationPermissionStatus.type"
          :class="{ 'cursor-pointer': locationPermissionStatus.type === 'danger' }"
          @click="locationPermissionStatus.type === 'danger' ? showPermissionDeniedDialog() : null"
        >
          <el-icon>
            <component :is="locationPermissionStatus.icon" />
          </el-icon>
          {{ locationPermissionStatus.message }}
        </el-text>
      </div>
    </div>

    <!-- Map Container -->
    <div class="map-container">
      <div
        v-if="!mapLoadError"
        ref="mapContainer"
        class="map-element"
        :style="{ height: mapHeight }"
      ></div>
      
      <!-- Fallback when map fails to load -->
      <div v-else class="map-fallback" :style="{ height: mapHeight }">
        <div class="fallback-content">
          <el-icon size="48" color="#909399">
            <MapLocation />
          </el-icon>
          <h3>Map Unavailable</h3>
          <p>Google Maps failed to load. You can still enter coordinates manually.</p>
          <el-button @click="retryMapLoad" type="primary" plain>
            Retry Loading Map
          </el-button>
        </div>
      </div>
      
      <!-- Loading Overlay -->
      <div v-if="isMapLoading && !mapLoadError" class="map-loading">
        <el-icon class="is-loading">
          <Loading />
        </el-icon>
        <span>Loading map...</span>
      </div>
    </div>

    <!-- Coordinates Display -->
    <div class="coordinates-display mt-4">
      <el-row :gutter="16">
        <el-col :span="12">
          <el-input
            v-model="displayLatitude"
            label="Latitude"
            placeholder="Latitude"
            @input="onCoordinateInput"
          >
            <template #prepend>Lat</template>
          </el-input>
        </el-col>
        <el-col :span="12">
          <el-input
            v-model="displayLongitude"
            label="Longitude"
            placeholder="Longitude"
            @input="onCoordinateInput"
          >
            <template #prepend>Lng</template>
          </el-input>
        </el-col>
      </el-row>
    </div>

    <!-- Address Display -->
    <div v-if="selectedAddress" class="address-display mt-3">
      <el-input
        v-model="selectedAddress"
        placeholder="Address will appear here..."
        readonly
      >
        <template #prepend>
          <el-icon><MapLocation /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- Open in Google Maps -->
    <div v-if="selectedLocation" class="mt-3">
      <el-button
        @click="openInGoogleMaps"
        :icon="Link"
        type="success"
        plain
        size="small"
      >
        Open in Google Maps
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
import { Loader } from '@googlemaps/js-api-loader';
import { ElMessage, ElMessageBox } from 'element-plus';
import {
  Search,
  Location,
  Loading,
  MapLocation,
  Link,
  InfoFilled,
  SuccessFilled,
  WarningFilled,
  CircleCloseFilled,
} from '@element-plus/icons-vue';
import type { GooglePlaceResult } from '~/types/hr/work-location.dto';

interface Props {
  modelValue?: {
    latitude: number;
    longitude: number;
    address?: string;
  };
  radius?: number;
  mapHeight?: string;
  zoom?: number;
}

interface Emits {
  (e: 'update:modelValue', value: {
    latitude: number;
    longitude: number;
    address?: string;
  }): void;
  (e: 'update:address', address: string): void;
}

const props = withDefaults(defineProps<Props>(), {
  mapHeight: '400px',
  zoom: 15,
  radius: 100,
});

const emit = defineEmits<Emits>();

// Refs
const mapContainer = ref<HTMLDivElement>();
const searchQuery = ref('');
const selectedLocation = ref<{ latitude: number; longitude: number } | null>(null);
const selectedAddress = ref('');
const displayLatitude = ref('');
const displayLongitude = ref('');

// State
const isMapLoading = ref(true);
const isSearching = ref(false);
const isGettingLocation = ref(false);
const mapLoadError = ref(false);
const locationPermissionStatus = ref<{
  type: 'success' | 'warning' | 'danger' | 'info';
  icon: string;
  message: string;
} | null>(null);

// Google Maps objects
let map: google.maps.Map | null = null;
let marker: google.maps.Marker | null = null;
let circle: google.maps.Circle | null = null;
let geocoder: google.maps.Geocoder | null = null;
let placesService: google.maps.places.PlacesService | null = null;

// Initialize map
onMounted(async () => {
  await initializeMap();
  checkLocationPermissionStatus();
});

// Watch for prop changes
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue && map) {
      updateMapLocation(newValue.latitude, newValue.longitude, newValue.address);
    }
  },
  { immediate: true }
);

watch(
  () => props.radius,
  (newRadius) => {
    if (circle && newRadius) {
      circle.setRadius(newRadius);
    }
  }
);

async function initializeMap() {
  try {
    const config = useRuntimeConfig();
    
    if (!config.public.googleMapsApiKey) {
      throw new Error('Google Maps API key is not configured');
    }

    const loader = new Loader({
      apiKey: config.public.googleMapsApiKey,
      version: 'weekly',
      libraries: ['places', 'geometry'],
    });

    await loader.load();

    if (!mapContainer.value) {
      throw new Error('Map container not found');
    }

    // Default location (you can change this to your preferred default)
    const defaultLocation = { lat: 37.7749, lng: -122.4194 }; // San Francisco

    // Initialize map
    map = new google.maps.Map(mapContainer.value, {
      center: defaultLocation,
      zoom: props.zoom,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      disableDefaultUI: false,
      zoomControl: true,
      streetViewControl: true,
      fullscreenControl: true,
      gestureHandling: 'cooperative', // Better mobile experience
    });

    // Initialize services
    geocoder = new google.maps.Geocoder();
    placesService = new google.maps.places.PlacesService(map);

    // Add click listener to map
    map.addListener('click', (event: google.maps.MapMouseEvent) => {
      if (event.latLng) {
        const lat = event.latLng.lat();
        const lng = event.latLng.lng();
        updateMapLocation(lat, lng);
        reverseGeocode(lat, lng);
      }
    });

    // Set initial location if provided
    if (props.modelValue) {
      updateMapLocation(
        props.modelValue.latitude,
        props.modelValue.longitude,
        props.modelValue.address
      );
    }

    isMapLoading.value = false;
    ElMessage.success('Map loaded successfully');
  } catch (error: any) {
    console.error('Error initializing map:', error);
    
    let errorMessage = 'Failed to load Google Maps';
    if (error.message.includes('API key')) {
      errorMessage = 'Google Maps API key is missing or invalid';
    } else if (error.message.includes('quota') || error.message.includes('billing')) {
      errorMessage = 'Google Maps API quota exceeded or billing not enabled';
    } else if (error.message.includes('network') || error.message.includes('fetch')) {
      errorMessage = 'Network error loading Google Maps. Please check your internet connection.';
    }
    
    ElMessage.error(errorMessage);
    isMapLoading.value = false;
    mapLoadError.value = true;
  }
}

function updateMapLocation(lat: number, lng: number, address?: string) {
  if (!map) return;

  const position = { lat, lng };

  // Update map center
  map.setCenter(position);

  // Update or create marker
  if (marker) {
    marker.setPosition(position);
  } else {
    marker = new google.maps.Marker({
      position,
      map,
      draggable: true,
      title: 'Selected Location',
    });

    // Add drag listener to marker
    marker.addListener('dragend', (event: google.maps.MapMouseEvent) => {
      if (event.latLng) {
        const newLat = event.latLng.lat();
        const newLng = event.latLng.lng();
        updateSelectedLocation(newLat, newLng);
        reverseGeocode(newLat, newLng);
      }
    });
  }

  // Update or create radius circle
  if (circle) {
    circle.setCenter(position);
    circle.setRadius(props.radius);
  } else {
    circle = new google.maps.Circle({
      center: position,
      radius: props.radius,
      map,
      fillColor: '#4285f4',
      fillOpacity: 0.2,
      strokeColor: '#4285f4',
      strokeOpacity: 0.8,
      strokeWeight: 2,
    });
  }

  // Update internal state
  updateSelectedLocation(lat, lng, address);
}

function updateSelectedLocation(lat: number, lng: number, address?: string) {
  selectedLocation.value = { latitude: lat, longitude: lng };
  displayLatitude.value = lat.toFixed(6);
  displayLongitude.value = lng.toFixed(6);
  
  if (address) {
    selectedAddress.value = address;
  }

  // Emit the update
  emit('update:modelValue', {
    latitude: lat,
    longitude: lng,
    address: selectedAddress.value,
  });

  if (selectedAddress.value) {
    emit('update:address', selectedAddress.value);
  }
}

async function reverseGeocode(lat: number, lng: number) {
  if (!geocoder) {
    console.warn('Geocoder not available');
    return;
  }

  try {
    const response = await geocoder.geocode({
      location: { lat, lng },
    });

    if (response.results && response.results.length > 0) {
      const address = response.results[0].formatted_address;
      selectedAddress.value = address;
      emit('update:address', address);
    } else {
      console.warn('No address found for coordinates:', lat, lng);
      selectedAddress.value = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
    }
  } catch (error: any) {
    console.error('Reverse geocoding failed:', error);
    // Don't show error to user for reverse geocoding failures
    // Just use coordinates as fallback
    selectedAddress.value = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
  }
}

async function searchPlaces() {
  if (!searchQuery.value.trim()) {
    ElMessage.warning('Please enter a search term');
    return;
  }
  
  if (!placesService) {
    ElMessage.error('Places service not available. Please wait for map to load.');
    return;
  }

  isSearching.value = true;

  try {
    const request: google.maps.places.TextSearchRequest = {
      query: searchQuery.value.trim(),
    };

    placesService.textSearch(request, (results, status) => {
      isSearching.value = false;

      if (status === google.maps.places.PlacesServiceStatus.OK && results && results.length > 0) {
        const place = results[0];
        if (place.geometry?.location) {
          const lat = place.geometry.location.lat();
          const lng = place.geometry.location.lng();
          const address = place.formatted_address || searchQuery.value;
          
          updateMapLocation(lat, lng, address);
          searchQuery.value = '';
          ElMessage.success(`Found: ${place.name || address}`);
        } else {
          ElMessage.warning('Location coordinates not available for this place');
        }
      } else {
        let errorMessage = 'No places found for your search';
        
        switch (status) {
          case google.maps.places.PlacesServiceStatus.ZERO_RESULTS:
            errorMessage = 'No places found matching your search';
            break;
          case google.maps.places.PlacesServiceStatus.OVER_QUERY_LIMIT:
            errorMessage = 'Search quota exceeded. Please try again later.';
            break;
          case google.maps.places.PlacesServiceStatus.REQUEST_DENIED:
            errorMessage = 'Search request denied. Please check API configuration.';
            break;
          case google.maps.places.PlacesServiceStatus.INVALID_REQUEST:
            errorMessage = 'Invalid search request. Please try a different search term.';
            break;
          default:
            errorMessage = 'Search failed. Please try again.';
            break;
        }
        
        ElMessage.warning(errorMessage);
      }
    });
  } catch (error: any) {
    console.error('Places search failed:', error);
    ElMessage.error('Search failed: ' + (error.message || 'Unknown error'));
    isSearching.value = false;
  }
}

function clearSearch() {
  searchQuery.value = '';
}

async function getCurrentLocation() {
  if (!navigator.geolocation) {
    showLocationNotSupportedDialog();
    return;
  }

  // Check if we're on HTTPS or localhost (required for geolocation)
  if (location.protocol !== 'https:' && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
    showHttpsRequiredDialog();
    return;
  }

  isGettingLocation.value = true;

  try {
    // Check permissions first if supported
    if ('permissions' in navigator) {
      try {
        const permission = await navigator.permissions.query({ name: 'geolocation' });
        
        if (permission.state === 'denied') {
          showPermissionDeniedDialog();
          return;
        }
      } catch (permError) {
        // Some browsers don't support permissions.query for geolocation
        console.warn('Permission query not supported:', permError);
      }
    }

    const position = await new Promise<GeolocationPosition>((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        resolve,
        (error) => {
          reject(error);
        },
        {
          enableHighAccuracy: true,
          timeout: 15000,
          maximumAge: 300000, // 5 minutes cache
        }
      );
    });

    const lat = position.coords.latitude;
    const lng = position.coords.longitude;
    
    updateMapLocation(lat, lng);
    reverseGeocode(lat, lng);
    
    ElMessage.success(`Current location detected (±${Math.round(position.coords.accuracy)}m accuracy)`);
    
    // Update permission status
    checkLocationPermissionStatus();
  } catch (error: any) {
    console.error('Geolocation failed:', error);
    handleGeolocationError(error);
  } finally {
    isGettingLocation.value = false;
    // Always refresh permission status after attempt
    setTimeout(checkLocationPermissionStatus, 100);
  }
}

function handleGeolocationError(error: GeolocationPositionError) {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      showPermissionDeniedDialog();
      break;
    case error.POSITION_UNAVAILABLE:
      ElMessage.error('Location information unavailable. Please check your device settings and try again.');
      break;
    case error.TIMEOUT:
      ElMessage.error('Location request timed out. Please try again or check your internet connection.');
      break;
    default:
      ElMessage.error(`Location error: ${error.message}`);
      break;
  }
}

function showPermissionDeniedDialog() {
  const browserName = getBrowserName();
  const instructions = getBrowserSpecificInstructions(browserName);
  
  ElMessageBox.alert(
    `Location access has been denied. To enable location access:

${instructions}

Alternative options:
• Search for places using the search box above
• Click directly on the map to select a location  
• Enter coordinates manually in the input fields

Note: You may need to refresh the page after changing permissions.`,
    'Enable Location Access',
    {
      confirmButtonText: 'Got it',
      type: 'warning',
      dangerouslyUseHTMLString: false,
    }
  );
}

function getBrowserName(): string {
  const userAgent = navigator.userAgent;
  if (userAgent.includes('Chrome')) return 'Chrome';
  if (userAgent.includes('Firefox')) return 'Firefox';
  if (userAgent.includes('Safari')) return 'Safari';
  if (userAgent.includes('Edge')) return 'Edge';
  return 'Browser';
}

function getBrowserSpecificInstructions(browser: string): string {
  switch (browser) {
    case 'Chrome':
      return `Chrome Instructions:
1. Click the location/lock icon (🔒) in the address bar
2. Select "Site settings" or click on "Location"
3. Change from "Block" to "Allow"
4. Refresh this page`;
    
    case 'Firefox':
      return `Firefox Instructions:
1. Click the shield or lock icon in the address bar
2. Click on "Permissions" or the location icon
3. Select "Allow" for location access
4. Refresh this page`;
    
    case 'Safari':
      return `Safari Instructions:
1. Go to Safari > Preferences > Websites
2. Click on "Location" in the left sidebar
3. Find this website and change to "Allow"
4. Refresh this page`;
    
    case 'Edge':
      return `Edge Instructions:
1. Click the lock icon in the address bar
2. Click on "Permissions for this site"
3. Change Location from "Block" to "Allow"
4. Refresh this page`;
    
    default:
      return `General Instructions:
1. Look for a location or lock icon in your address bar
2. Click it and find location/geolocation settings
3. Change the setting from "Block" to "Allow"
4. Refresh this page`;
  }
}

function showHttpsRequiredDialog() {
  ElMessageBox.alert(
    `Location access requires a secure connection (HTTPS) or localhost.

Current URL: ${location.protocol}//${location.hostname}

To fix this:
• Use HTTPS in production
• Use localhost for development

Alternative: You can manually enter coordinates or search for a place.`,
    'Secure Connection Required',
    {
      confirmButtonText: 'Understood',
      type: 'warning',
      dangerouslyUseHTMLString: false,
    }
  );
}

function showLocationNotSupportedDialog() {
  ElMessageBox.alert(
    `Your browser doesn't support geolocation.

You can still:
• Search for places using the search box
• Click on the map to select a location
• Enter coordinates manually

Most modern browsers support geolocation. Consider updating your browser for the best experience.`,
    'Geolocation Not Supported',
    {
      confirmButtonText: 'OK',
      type: 'info',
      dangerouslyUseHTMLString: false,
    }
  );
}

function onCoordinateInput() {
  const lat = parseFloat(displayLatitude.value);
  const lng = parseFloat(displayLongitude.value);

  // Validate coordinate ranges
  if (isNaN(lat) || isNaN(lng)) {
    return; // Don't update if invalid numbers
  }

  if (lat < -90 || lat > 90) {
    ElMessage.warning('Latitude must be between -90 and 90');
    return;
  }

  if (lng < -180 || lng > 180) {
    ElMessage.warning('Longitude must be between -180 and 180');
    return;
  }

  updateMapLocation(lat, lng);
  
  // Debounce reverse geocoding to avoid too many API calls
  clearTimeout(reverseGeocodeTimeout);
  reverseGeocodeTimeout = setTimeout(() => {
    reverseGeocode(lat, lng);
  }, 1000);
}

// Add timeout variable
let reverseGeocodeTimeout: ReturnType<typeof setTimeout>;

function openInGoogleMaps() {
  if (!selectedLocation.value) return;

  const url = `https://www.google.com/maps?q=${selectedLocation.value.latitude},${selectedLocation.value.longitude}`;
  window.open(url, '_blank');
}

function retryMapLoad() {
  mapLoadError.value = false;
  isMapLoading.value = true;
  initializeMap();
}

async function checkLocationPermissionStatus() {
  if (!navigator.geolocation) {
    locationPermissionStatus.value = {
      type: 'warning',
      icon: 'WarningFilled',
      message: 'Geolocation not supported by this browser'
    };
    return;
  }

  // Check HTTPS requirement
  if (location.protocol !== 'https:' && location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
    locationPermissionStatus.value = {
      type: 'warning',
      icon: 'WarningFilled',
      message: 'HTTPS required for location access'
    };
    return;
  }

  // Check permission status if supported
  if ('permissions' in navigator) {
    try {
      const permission = await navigator.permissions.query({ name: 'geolocation' });
      
      switch (permission.state) {
        case 'granted':
          locationPermissionStatus.value = {
            type: 'success',
            icon: 'SuccessFilled',
            message: 'Location access granted'
          };
          break;
        case 'denied':
          locationPermissionStatus.value = {
            type: 'danger',
            icon: 'CircleCloseFilled',
            message: 'Location access denied - click for help'
          };
          break;
        case 'prompt':
          locationPermissionStatus.value = {
            type: 'info',
            icon: 'InfoFilled',
            message: 'Location permission will be requested'
          };
          break;
      }

      // Listen for permission changes
      permission.addEventListener('change', () => {
        checkLocationPermissionStatus();
      });
    } catch (error) {
      // Permissions API not fully supported
      locationPermissionStatus.value = {
        type: 'info',
        icon: 'InfoFilled',
        message: 'Click to request location access'
      };
    }
  } else {
    locationPermissionStatus.value = {
      type: 'info',
      icon: 'InfoFilled',
      message: 'Click to request location access'
    };
  }
}
</script>

<style scoped>
.google-location-picker {
  width: 100%;
}

.map-container {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--el-border-color);
}

.map-element {
  width: 100%;
  min-height: 300px;
}

.map-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.coordinates-display {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.address-display {
  font-size: 14px;
}

.geolocation-help {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--el-text-color-regular);
}

.geolocation-help .el-icon {
  font-size: 14px;
}

.map-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border: 2px dashed #dcdfe6;
}

.fallback-content {
  text-align: center;
  color: var(--el-text-color-regular);
}

.fallback-content h3 {
  margin: 16px 0 8px 0;
  color: var(--el-text-color-primary);
}

.fallback-content p {
  margin: 0 0 16px 0;
  font-size: 14px;
}

.cursor-pointer {
  cursor: pointer;
}

.cursor-pointer:hover {
  opacity: 0.8;
}

@media (max-width: 768px) {
  .map-element {
    min-height: 250px;
  }
}
</style>