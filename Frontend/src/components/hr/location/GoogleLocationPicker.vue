<template>
  <div class="google-location-picker">
    <!-- Search Input -->
    <div class="search-section mb-3">
      <el-input
        v-model="searchQuery"
        placeholder="Search for a place or address..."
        :prefix-icon="Search"
        clearable
        :disabled="disabled || !isMapReady"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button 
            @click="handleSearch" 
            :loading="isSearching"
            :disabled="disabled || !isMapReady"
          >
            Search
          </el-button>
        </template>
      </el-input>
    </div>

    <!-- Action Buttons -->
    <div class="actions-section mb-3">
      <el-button
        @click="handleGetCurrentLocation"
        :loading="isGettingLocation || isAutoDetecting"
        :icon="Location"
        :disabled="disabled || !isMapReady"
        type="primary"
        plain
        size="default"
      >
        {{ isAutoDetecting ? 'Detecting...' : 'Use Current Location' }}
      </el-button>
      
      <el-button
        v-if="hasValidCoordinates"
        @click="handleOpenInGoogleMaps"
        :icon="Link"
        :disabled="disabled"
        type="success"
        plain
        size="default"
      >
        Open in Google Maps
      </el-button>
    </div>

    <!-- Auto-detecting indicator -->
    <div v-if="isAutoDetecting" class="auto-detect-status mb-3">
      <el-alert
        type="info"
        :closable="false"
        show-icon
      >
        <template #default>
          <div class="flex items-center gap-2">
            <el-icon class="is-loading"><Loading /></el-icon>
            <span>Detecting your current location...</span>
          </div>
        </template>
      </el-alert>
    </div>

    <!-- Map Container -->
    <div class="map-wrapper" :style="{ height }">
      <div
        v-show="isMapReady && !mapError"
        ref="mapContainer"
        class="map-container"
      ></div>
      
      <!-- Loading State -->
      <div v-if="isMapLoading" class="map-overlay">
        <el-icon class="is-loading" :size="40">
          <Loading />
        </el-icon>
        <p class="mt-2">Loading map...</p>
      </div>
      
      <!-- Error State -->
      <div v-if="mapError" class="map-overlay error">
        <el-icon :size="40" color="#f56c6c">
          <CircleClose />
        </el-icon>
        <p class="mt-2 text-center px-4">{{ mapError }}</p>
        <el-button @click="retryMapInit" type="primary" plain class="mt-2">
          Retry Loading Map
        </el-button>
      </div>
    </div>

    <!-- Coordinates Display -->
    <div class="coordinates-section mt-3">
      <el-row :gutter="12">
        <el-col :span="12">
          <el-input
            :model-value="displayLatitude"
            @input="handleLatitudeInput"
            placeholder="Latitude"
            :disabled="disabled"
          >
            <template #prepend>Lat</template>
          </el-input>
        </el-col>
        <el-col :span="12">
          <el-input
            :model-value="displayLongitude"
            @input="handleLongitudeInput"
            placeholder="Longitude"
            :disabled="disabled"
          >
            <template #prepend>Lng</template>
          </el-input>
        </el-col>
      </el-row>
    </div>

    <!-- Address Display -->
    <div v-if="displayAddress" class="address-section mt-3">
      <el-input
        :model-value="displayAddress"
        placeholder="Address"
        readonly
        :disabled="disabled"
      >
        <template #prepend>
          <el-icon><MapLocation /></el-icon>
        </template>
      </el-input>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { setOptions, importLibrary } from '@googlemaps/js-api-loader';
import { ElMessage, ElMessageBox } from 'element-plus';
import {
  Search,
  Location,
  Loading,
  MapLocation,
  Link,
  CircleClose,
} from '@element-plus/icons-vue';

// Props
interface Props {
  latitude?: number | null;
  longitude?: number | null;
  radiusMeters?: number;
  height?: string;
  disabled?: boolean;
  address?: string;
  autoDetectLocation?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  latitude: null,
  longitude: null,
  radiusMeters: 100,
  height: '400px',
  disabled: false,
  address: '',
  autoDetectLocation: true,
});

// Emits
interface Emits {
  (e: 'update:latitude', value: number): void;
  (e: 'update:longitude', value: number): void;
  (e: 'update:address', value: string): void;
  (e: 'picked', value: { latitude: number; longitude: number; address?: string }): void;
}

const emit = defineEmits<Emits>();

// Refs
const mapContainer = ref<HTMLDivElement>();
const searchQuery = ref('');
const displayLatitude = ref('');
const displayLongitude = ref('');
const displayAddress = ref('');

// State
const isMapLoading = ref(true);
const isMapReady = ref(false);
const isSearching = ref(false);
const isGettingLocation = ref(false);
const isAutoDetecting = ref(false);
const mapError = ref('');
const hasAttemptedAutoDetect = ref(false);

// Google Maps instances
let map: google.maps.Map | null = null;
let marker: google.maps.Marker | null = null;
let circle: google.maps.Circle | null = null;
let geocoder: google.maps.Geocoder | null = null;
let placesService: google.maps.places.PlacesService | null = null;
let clickListener: google.maps.MapsEventListener | null = null;

// Computed
const hasValidCoordinates = computed(() => {
  const lat = parseFloat(displayLatitude.value);
  const lng = parseFloat(displayLongitude.value);
  return !isNaN(lat) && !isNaN(lng) && lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180;
});

// Watch props
watch(
  () => [props.latitude, props.longitude, props.address] as const,
  ([lat, lng, addr]) => {
    if (lat !== null && lng !== null && !isNaN(lat) && !isNaN(lng)) {
      displayLatitude.value = lat.toFixed(6);
      displayLongitude.value = lng.toFixed(6);
      
      if (isMapReady.value && map) {
        updateMapLocation(lat, lng, addr);
      }
    }
    
    if (addr) {
      displayAddress.value = addr;
    }
  },
  { immediate: true }
);

watch(
  () => props.radiusMeters,
  (newRadius) => {
    if (circle && newRadius && newRadius > 0) {
      circle.setRadius(newRadius);
    }
  }
);

// Lifecycle
onMounted(() => {
  if (process.client) {
    initializeMap();
  }
});

onBeforeUnmount(() => {
  cleanup();
});

// Methods
async function initializeMap() {
  if (!process.client) return;
  
  isMapLoading.value = true;
  mapError.value = '';
  isMapReady.value = false;

  try {
    const config = useRuntimeConfig();
    const apiKey = config.public.googleMapsApiKey as string;

    if (!apiKey) {
      throw new Error('Google Maps API key not configured');
    }

    // Set global options
    setOptions({
      apiKey,
      version: 'weekly',
    });

    // Import required libraries
    const [mapsLib, placesLib, geocodingLib] = await Promise.all([
      importLibrary('maps') as Promise<google.maps.MapsLibrary>,
      importLibrary('places') as Promise<google.maps.PlacesLibrary>,
      importLibrary('geocoding') as Promise<google.maps.GeocodingLibrary>,
    ]);

    await nextTick();

    if (!mapContainer.value) {
      throw new Error('Map container not found');
    }

    // Determine initial center
    const hasProvidedCoords = props.latitude !== null && props.longitude !== null;
    const defaultCenter = {
      lat: hasProvidedCoords ? props.latitude! : 11.5564,
      lng: hasProvidedCoords ? props.longitude! : 104.9282,
    };

    // Initialize map
    map = new mapsLib.Map(mapContainer.value, {
      center: defaultCenter,
      zoom: 15,
      disableDefaultUI: false,
      zoomControl: true,
      streetViewControl: false,
      fullscreenControl: true,
      gestureHandling: 'cooperative',
      mapTypeControl: false,
    });

    // Initialize services
    geocoder = new geocodingLib.Geocoder();
    placesService = new placesLib.PlacesService(map);

    // Add click listener
    clickListener = map.addListener('click', async (event: google.maps.MapMouseEvent) => {
      if (props.disabled || !event.latLng) return;
      
      const lat = event.latLng.lat();
      const lng = event.latLng.lng();
      
      updateMapLocation(lat, lng);
      const address = await reverseGeocode(lat, lng);
      emitUpdate(lat, lng, address);
    });

    isMapReady.value = true;
    isMapLoading.value = false;

    // Handle initial location
    if (hasProvidedCoords) {
      // Use provided coordinates
      updateMapLocation(props.latitude!, props.longitude!, props.address);
    } else if (props.autoDetectLocation && !hasAttemptedAutoDetect.value) {
      // Auto-detect location only once
      hasAttemptedAutoDetect.value = true;
      setTimeout(() => {
        autoDetectLocation();
      }, 300);
    }
  } catch (error: any) {
    console.error('Map initialization error:', error);
    handleMapError(error);
  }
}

function handleMapError(error: any) {
  let errorMessage = 'Failed to load Google Maps';
  
  if (error.message?.includes('API key') || error.message?.includes('not configured')) {
    errorMessage = 'Google Maps API key is missing. Please configure NUXT_PUBLIC_GOOGLE_MAPS_API_KEY in your .env file.';
  } else if (error.message?.includes('quota') || error.message?.includes('billing')) {
    errorMessage = 'Google Maps API quota exceeded or billing not enabled. Please check your Google Cloud Console.';
  } else if (error.message?.includes('RefererNotAllowedMapError')) {
    errorMessage = 'API key domain restrictions are blocking this site. Please update restrictions in Google Cloud Console.';
  } else if (error.message?.includes('ApiNotActivatedMapError')) {
    errorMessage = 'Required APIs not enabled. Please enable Maps JavaScript API, Places API, and Geocoding API.';
  } else if (error.message) {
    errorMessage = error.message;
  }
  
  mapError.value = errorMessage;
  isMapLoading.value = false;
}

function retryMapInit() {
  hasAttemptedAutoDetect.value = false;
  initializeMap();
}

async function autoDetectLocation() {
  if (!navigator.geolocation || isAutoDetecting.value) return;
  
  // Check HTTPS requirement
  const isSecure = location.protocol === 'https:' || 
                   location.hostname === 'localhost' || 
                   location.hostname === '127.0.0.1';
  
  if (!isSecure) {
    console.warn('Auto-detect skipped: HTTPS required');
    return;
  }

  isAutoDetecting.value = true;

  try {
    const position = await new Promise<GeolocationPosition>((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        resolve,
        reject,
        {
          enableHighAccuracy: false, // Faster response
          timeout: 10000,
          maximumAge: 600000, // 10 minutes cache
        }
      );
    });

    const lat = position.coords.latitude;
    const lng = position.coords.longitude;
    
    updateMapLocation(lat, lng);
    const address = await reverseGeocode(lat, lng);
    emitUpdate(lat, lng, address);
    
    console.log('✅ Auto-detected location:', { lat, lng, accuracy: position.coords.accuracy });
  } catch (error: any) {
    // Silent fail for auto-detect
    console.warn('Auto-detect failed (silent):', error.code, error.message);
  } finally {
    isAutoDetecting.value = false;
  }
}

function updateMapLocation(lat: number, lng: number, address?: string) {
  if (!map) return;

  const position = { lat, lng };

  // Update map center
  map.panTo(position);

  // Update or create marker
  if (marker) {
    marker.setPosition(position);
  } else {
    createMarker(position);
  }

  // Update or create circle
  if (circle) {
    circle.setCenter(position);
    circle.setRadius(props.radiusMeters);
  } else {
    circle = new google.maps.Circle({
      center: position,
      radius: props.radiusMeters,
      map,
      fillColor: '#4285f4',
      fillOpacity: 0.2,
      strokeColor: '#4285f4',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      clickable: false,
    });
  }

  // Update display
  displayLatitude.value = lat.toFixed(6);
  displayLongitude.value = lng.toFixed(6);
  
  if (address) {
    displayAddress.value = address;
  }
}

function createMarker(position: google.maps.LatLngLiteral) {
  if (!map) return;

  marker = new google.maps.Marker({
    map,
    position,
    draggable: !props.disabled,
    title: 'Selected Location',
    animation: google.maps.Animation.DROP,
  });

  marker.addListener('dragend', async (event: google.maps.MapMouseEvent) => {
    if (props.disabled || !event.latLng) return;
    
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    
    updateMapLocation(lat, lng);
    const address = await reverseGeocode(lat, lng);
    emitUpdate(lat, lng, address);
  });
}

async function reverseGeocode(lat: number, lng: number): Promise<string | undefined> {
  if (!geocoder) return undefined;

  try {
    const response = await geocoder.geocode({
      location: { lat, lng },
    });

    if (response.results && response.results.length > 0) {
      const address = response.results[0].formatted_address;
      displayAddress.value = address;
      return address;
    }
  } catch (error) {
    console.error('Reverse geocoding failed:', error);
  }
  
  return undefined;
}

async function handleSearch() {
  const query = searchQuery.value.trim();
  
  if (!query) {
    ElMessage.warning('Please enter a search term');
    return;
  }
  
  if (!placesService || !map) {
    ElMessage.error('Map not ready. Please wait.');
    return;
  }

  isSearching.value = true;

  try {
    const request: google.maps.places.TextSearchRequest = {
      query,
    };

    placesService.textSearch(request, (results, status) => {
      isSearching.value = false;

      if (status === google.maps.places.PlacesServiceStatus.OK && results && results.length > 0) {
        const place = results[0];
        
        if (place.geometry?.location) {
          const lat = place.geometry.location.lat();
          const lng = place.geometry.location.lng();
          const address = place.formatted_address || query;
          
          updateMapLocation(lat, lng, address);
          emitUpdate(lat, lng, address);
          
          searchQuery.value = '';
          ElMessage.success(`Found: ${place.name || address}`);
        } else {
          ElMessage.warning('Location coordinates not available');
        }
      } else {
        ElMessage.warning('No places found. Try a different search term.');
      }
    });
  } catch (error) {
    console.error('Search failed:', error);
    ElMessage.error('Search failed. Please try again.');
    isSearching.value = false;
  }
}

async function handleGetCurrentLocation() {
  if (!navigator.geolocation) {
    ElMessageBox.alert(
      'Your browser doesn\'t support geolocation.\n\nYou can:\n• Search for places\n• Click on the map\n• Enter coordinates manually',
      'Geolocation Not Supported',
      { confirmButtonText: 'OK', type: 'info' }
    );
    return;
  }

  // Check HTTPS
  const isSecure = location.protocol === 'https:' || 
                   location.hostname === 'localhost' || 
                   location.hostname === '127.0.0.1';
  
  if (!isSecure) {
    ElMessageBox.alert(
      `Location access requires HTTPS or localhost.\n\nCurrent: ${location.protocol}//${location.hostname}\n\nPlease use HTTPS in production.`,
      'Secure Connection Required',
      { confirmButtonText: 'OK', type: 'warning' }
    );
    return;
  }

  isGettingLocation.value = true;

  // Log for debugging
  console.log('🔍 Attempting to get current location...');
  console.log('🔍 Protocol:', location.protocol);
  console.log('🔍 Hostname:', location.hostname);

  try {
    const position = await new Promise<GeolocationPosition>((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          console.log('✅ Location obtained:', {
            lat: pos.coords.latitude,
            lng: pos.coords.longitude,
            accuracy: pos.coords.accuracy
          });
          resolve(pos);
        },
        (err) => {
          console.error('❌ Geolocation error:', {
            code: err.code,
            message: err.message,
            PERMISSION_DENIED: err.code === 1,
            POSITION_UNAVAILABLE: err.code === 2,
            TIMEOUT: err.code === 3
          });
          reject(err);
        },
        {
          enableHighAccuracy: true,
          timeout: 15000,
          maximumAge: 0, // Force fresh location
        }
      );
    });

    const lat = position.coords.latitude;
    const lng = position.coords.longitude;
    
    console.log('✅ Updating map with location:', { lat, lng });
    
    updateMapLocation(lat, lng);
    const address = await reverseGeocode(lat, lng);
    emitUpdate(lat, lng, address);
    
    ElMessage.success(`Location detected (±${Math.round(position.coords.accuracy)}m accuracy)`);
  } catch (error: any) {
    handleGeolocationError(error);
  } finally {
    isGettingLocation.value = false;
  }
}

function handleGeolocationError(error: GeolocationPositionError) {
  const browser = getBrowserName();
  const instructions = getBrowserInstructions(browser);
  
  switch (error.code) {
    case 1: // PERMISSION_DENIED
      ElMessageBox.alert(
        `Location permission issue detected.\n\n🔧 Quick Fix:\n1. Hard refresh this page: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)\n2. Click "Use Current Location" again\n\nIf that doesn't work:\n${instructions}\n\n💡 Check browser console (F12) for detailed error info.\n\nAlternatives:\n• Search for a place\n• Click on the map\n• Enter coordinates manually`,
        'Location Permission Issue',
        { confirmButtonText: 'Got It', type: 'warning' }
      );
      break;
    case 2: // POSITION_UNAVAILABLE
      ElMessage.error('Location unavailable. Check device GPS/location settings and try again.');
      break;
    case 3: // TIMEOUT
      ElMessage.error('Location request timed out. Please try again.');
      break;
    default:
      ElMessage.error('Failed to get location. Please try again.');
  }
}

function getBrowserName(): string {
  const ua = navigator.userAgent;
  if (ua.includes('Edg')) return 'Edge';
  if (ua.includes('Chrome')) return 'Chrome';
  if (ua.includes('Firefox')) return 'Firefox';
  if (ua.includes('Safari')) return 'Safari';
  return 'Browser';
}

function getBrowserInstructions(browser: string): string {
  const instructions: Record<string, string> = {
    Chrome: '1. Click lock icon in address bar\n2. Select "Site settings"\n3. Change Location to "Allow"\n4. Refresh page',
    Firefox: '1. Click shield icon\n2. Click Permissions\n3. Allow Location\n4. Refresh page',
    Safari: '1. Safari > Preferences > Websites\n2. Click Location\n3. Allow this site\n4. Refresh page',
    Edge: '1. Click lock icon\n2. Permissions\n3. Allow Location\n4. Refresh page',
  };
  
  return instructions[browser] || instructions.Chrome;
}

function handleLatitudeInput(value: string) {
  const lat = parseFloat(value);
  if (isNaN(lat) || lat < -90 || lat > 90) return;
  
  displayLatitude.value = lat.toFixed(6);
  
  const lng = parseFloat(displayLongitude.value);
  if (!isNaN(lng)) {
    updateMapLocation(lat, lng);
    reverseGeocode(lat, lng);
    emitUpdate(lat, lng, displayAddress.value);
  }
}

function handleLongitudeInput(value: string) {
  const lng = parseFloat(value);
  if (isNaN(lng) || lng < -180 || lng > 180) return;
  
  displayLongitude.value = lng.toFixed(6);
  
  const lat = parseFloat(displayLatitude.value);
  if (!isNaN(lat)) {
    updateMapLocation(lat, lng);
    reverseGeocode(lat, lng);
    emitUpdate(lat, lng, displayAddress.value);
  }
}

function handleOpenInGoogleMaps() {
  const lat = parseFloat(displayLatitude.value);
  const lng = parseFloat(displayLongitude.value);
  
  if (!isNaN(lat) && !isNaN(lng)) {
    window.open(`https://www.google.com/maps?q=${lat},${lng}`, '_blank', 'noopener,noreferrer');
  }
}

function emitUpdate(lat: number, lng: number, address?: string) {
  emit('update:latitude', lat);
  emit('update:longitude', lng);
  
  if (address) {
    emit('update:address', address);
  }
  
  emit('picked', {
    latitude: lat,
    longitude: lng,
    address,
  });
}

function cleanup() {
  if (clickListener) {
    google.maps.event.removeListener(clickListener);
    clickListener = null;
  }
  
  if (marker) {
    marker.setMap(null);
    marker = null;
  }
  
  if (circle) {
    circle.setMap(null);
    circle = null;
  }
  
  map = null;
  geocoder = null;
  placesService = null;
}
</script>

<style scoped>
.google-location-picker {
  width: 100%;
}

.search-section,
.actions-section,
.auto-detect-status,
.coordinates-section,
.address-section {
  width: 100%;
}

.actions-section {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.map-wrapper {
  position: relative;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--el-border-color);
  background: #f5f7fa;
}

.map-container {
  width: 100%;
  height: 100%;
}

.map-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.95);
  z-index: 10;
  padding: 20px;
}

.map-overlay.error {
  background: rgba(255, 255, 255, 0.98);
}

.map-overlay p {
  margin: 0;
  color: var(--el-text-color-regular);
  font-size: 14px;
  max-width: 400px;
}

.flex {
  display: flex;
}

.items-center {
  align-items: center;
}

.gap-2 {
  gap: 8px;
}

.text-center {
  text-align: center;
}

.px-4 {
  padding-left: 16px;
  padding-right: 16px;
}

@media (max-width: 768px) {
  .actions-section {
    flex-direction: column;
  }
  
  .actions-section .el-button {
    width: 100%;
  }
}
</style>
