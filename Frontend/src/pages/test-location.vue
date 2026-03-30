<template>
  <div class="test-location-page">
    <div class="container">
      <h1>Location Permission Test</h1>
      <p>Use this page to test and troubleshoot location permissions.</p>
      
      <el-card class="mb-4">
        <template #header>
          <h3>Current Status</h3>
        </template>
        
        <div class="status-grid">
          <div class="status-item">
            <strong>Browser Support:</strong>
            <el-tag :type="browserSupport.supported ? 'success' : 'danger'">
              {{ browserSupport.message }}
            </el-tag>
          </div>
          
          <div class="status-item">
            <strong>HTTPS Status:</strong>
            <el-tag :type="httpsStatus.secure ? 'success' : 'warning'">
              {{ httpsStatus.message }}
            </el-tag>
          </div>
          
          <div class="status-item">
            <strong>Permission Status:</strong>
            <el-tag :type="permissionStatus.type">
              {{ permissionStatus.message }}
            </el-tag>
          </div>
        </div>
      </el-card>

      <el-card class="mb-4">
        <template #header>
          <h3>Test Location Access</h3>
        </template>
        
        <div class="test-controls">
          <el-button
            type="primary"
            @click="testLocation"
            :loading="testing"
            :disabled="!canTest"
          >
            Test Current Location
          </el-button>
          
          <el-button
            @click="checkPermissions"
            :loading="checkingPermissions"
          >
            Check Permissions
          </el-button>
        </div>
        
        <div v-if="lastResult" class="test-result mt-4">
          <h4>Last Test Result:</h4>
          <el-alert
            :type="lastResult.success ? 'success' : 'error'"
            :title="lastResult.message"
            :description="lastResult.details"
            show-icon
            :closable="false"
          />
        </div>
      </el-card>

      <el-card>
        <template #header>
          <h3>Troubleshooting Guide</h3>
        </template>
        
        <el-collapse>
          <el-collapse-item title="Location Permission Denied" name="denied">
            <div class="troubleshoot-content">
              <h4>Chrome Instructions:</h4>
              <ol>
                <li>Click the lock/location icon in the address bar</li>
                <li>Select "Site settings" or click "Location"</li>
                <li>Change from "Block" to "Allow"</li>
                <li>Refresh the page</li>
              </ol>
              
              <h4>Firefox Instructions:</h4>
              <ol>
                <li>Click the shield/lock icon in the address bar</li>
                <li>Click "Permissions" or the location icon</li>
                <li>Select "Allow" for location access</li>
                <li>Refresh the page</li>
              </ol>
            </div>
          </el-collapse-item>
          
          <el-collapse-item title="HTTPS Required" name="https">
            <div class="troubleshoot-content">
              <p>Geolocation requires a secure connection (HTTPS) or localhost.</p>
              <ul>
                <li>✅ https://yourdomain.com</li>
                <li>✅ http://localhost:3000</li>
                <li>✅ http://127.0.0.1:3000</li>
                <li>❌ http://yourdomain.com</li>
              </ul>
              <p>For production, ensure your site uses HTTPS.</p>
            </div>
          </el-collapse-item>
          
          <el-collapse-item title="Browser Not Supported" name="browser">
            <div class="troubleshoot-content">
              <p>Your browser doesn't support geolocation. Consider:</p>
              <ul>
                <li>Updating to the latest browser version</li>
                <li>Using a modern browser (Chrome, Firefox, Safari, Edge)</li>
                <li>Enabling JavaScript if disabled</li>
              </ul>
            </div>
          </el-collapse-item>
        </el-collapse>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { ElMessage } from 'element-plus';

definePageMeta({
  title: 'Location Permission Test',
  layout: 'default',
});

// State
const testing = ref(false);
const checkingPermissions = ref(false);
const permissionState = ref<PermissionState | 'unknown'>('unknown');
const lastResult = ref<{
  success: boolean;
  message: string;
  details: string;
} | null>(null);

// Computed
const browserSupport = computed(() => {
  if ('geolocation' in navigator) {
    return {
      supported: true,
      message: 'Geolocation Supported'
    };
  }
  return {
    supported: false,
    message: 'Geolocation Not Supported'
  };
});

const httpsStatus = computed(() => {
  const isSecure = location.protocol === 'https:' || 
                   location.hostname === 'localhost' || 
                   location.hostname === '127.0.0.1';
  
  return {
    secure: isSecure,
    message: isSecure ? 'Secure Connection' : 'Insecure Connection'
  };
});

const permissionStatus = computed(() => {
  switch (permissionState.value) {
    case 'granted':
      return { type: 'success' as const, message: 'Permission Granted' };
    case 'denied':
      return { type: 'danger' as const, message: 'Permission Denied' };
    case 'prompt':
      return { type: 'warning' as const, message: 'Permission Required' };
    default:
      return { type: 'info' as const, message: 'Permission Unknown' };
  }
});

const canTest = computed(() => {
  return browserSupport.value.supported && httpsStatus.value.secure;
});

// Methods
async function checkPermissions() {
  checkingPermissions.value = true;
  
  try {
    if ('permissions' in navigator) {
      const permission = await navigator.permissions.query({ name: 'geolocation' });
      permissionState.value = permission.state;
      
      // Listen for changes
      permission.addEventListener('change', () => {
        permissionState.value = permission.state;
      });
    } else {
      permissionState.value = 'unknown';
    }
  } catch (error) {
    console.error('Permission check failed:', error);
    permissionState.value = 'unknown';
  } finally {
    checkingPermissions.value = false;
  }
}

async function testLocation() {
  if (!canTest.value) {
    ElMessage.error('Cannot test location - check browser support and HTTPS status');
    return;
  }

  testing.value = true;
  lastResult.value = null;

  try {
    const position = await new Promise<GeolocationPosition>((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        resolve,
        reject,
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 60000,
        }
      );
    });

    lastResult.value = {
      success: true,
      message: 'Location Access Successful!',
      details: `Coordinates: ${position.coords.latitude.toFixed(6)}, ${position.coords.longitude.toFixed(6)} (±${Math.round(position.coords.accuracy)}m)`
    };

    ElMessage.success('Location detected successfully!');
    
    // Update permission status
    await checkPermissions();
  } catch (error: any) {
    let message = 'Location Access Failed';
    let details = '';

    if (error.code) {
      switch (error.code) {
        case error.PERMISSION_DENIED:
          message = 'Permission Denied';
          details = 'User denied location access. Check the troubleshooting guide below.';
          break;
        case error.POSITION_UNAVAILABLE:
          message = 'Position Unavailable';
          details = 'Location information is unavailable. Check device settings.';
          break;
        case error.TIMEOUT:
          message = 'Request Timeout';
          details = 'Location request timed out. Try again or check internet connection.';
          break;
        default:
          details = error.message || 'Unknown geolocation error';
      }
    } else {
      details = error.message || 'Unknown error occurred';
    }

    lastResult.value = {
      success: false,
      message,
      details
    };

    ElMessage.error(message);
    
    // Update permission status
    await checkPermissions();
  } finally {
    testing.value = false;
  }
}

// Lifecycle
onMounted(() => {
  checkPermissions();
});
</script>

<style scoped>
.test-location-page {
  padding: 24px;
  background: #f5f5f5;
  min-height: 100vh;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.status-grid {
  display: grid;
  gap: 16px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.test-controls {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.test-result {
  border-top: 1px solid #ebeef5;
  padding-top: 16px;
}

.troubleshoot-content h4 {
  margin: 16px 0 8px 0;
  color: #303133;
}

.troubleshoot-content ol,
.troubleshoot-content ul {
  margin: 8px 0;
  padding-left: 20px;
}

.troubleshoot-content li {
  margin: 4px 0;
}

@media (max-width: 768px) {
  .test-location-page {
    padding: 16px;
  }
  
  .status-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>