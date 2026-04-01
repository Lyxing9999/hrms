<template>
  <div class="test-page">
    <div class="container">
      <h1>Google Maps API Diagnostic</h1>
      
      <el-card class="mb-4">
        <template #header>
          <h3>Configuration Status</h3>
        </template>
        
        <div class="status-grid">
          <div class="status-item">
            <strong>API Key Configured:</strong>
            <el-tag :type="apiKeyStatus.type">
              {{ apiKeyStatus.message }}
            </el-tag>
          </div>
          
          <div class="status-item">
            <strong>API Key Preview:</strong>
            <code>{{ apiKeyPreview }}</code>
          </div>
          
          <div class="status-item">
            <strong>Environment:</strong>
            <el-tag>{{ environment }}</el-tag>
          </div>
          
          <div class="status-item">
            <strong>Protocol:</strong>
            <el-tag :type="protocolStatus.type">
              {{ protocolStatus.message }}
            </el-tag>
          </div>
        </div>
      </el-card>

      <el-card class="mb-4">
        <template #header>
          <h3>API Test</h3>
        </template>
        
        <div class="test-section">
          <el-button
            @click="testApiKey"
            :loading="testing"
            type="primary"
          >
            Test API Key
          </el-button>
          
          <el-button
            @click="openGoogleCloudConsole"
            type="info"
            plain
          >
            Open Google Cloud Console
          </el-button>
        </div>
        
        <div v-if="testResult" class="test-result mt-4">
          <el-alert
            :type="testResult.type"
            :title="testResult.title"
            :closable="false"
            show-icon
          >
            <template #default>
              <div v-html="testResult.message"></div>
            </template>
          </el-alert>
        </div>
      </el-card>

      <el-card class="mb-4">
        <template #header>
          <h3>Live Map Test</h3>
        </template>
        
        <ClientOnly>
          <GoogleLocationPicker
            :latitude="11.5564"
            :longitude="104.9282"
            :radius-meters="100"
            height="400px"
            @picked="handlePicked"
          />
          <template #fallback>
            <div class="loading-fallback">
              <el-skeleton :rows="8" animated />
            </div>
          </template>
        </ClientOnly>
        
        <div v-if="pickedLocation" class="mt-4">
          <el-alert type="success" title="Location Picked" :closable="false">
            <pre>{{ JSON.stringify(pickedLocation, null, 2) }}</pre>
          </el-alert>
        </div>
      </el-card>

      <el-card>
        <template #header>
          <h3>Troubleshooting Steps</h3>
        </template>
        
        <el-steps direction="vertical" :active="currentStep">
          <el-step title="Check API Key">
            <template #description>
              <div class="step-content">
                <p>Ensure NUXT_PUBLIC_GOOGLE_MAPS_API_KEY is set in .env file</p>
                <el-button size="small" @click="copyEnvExample">
                  Copy .env Example
                </el-button>
              </div>
            </template>
          </el-step>
          
          <el-step title="Enable APIs">
            <template #description>
              <div class="step-content">
                <p>Enable these APIs in Google Cloud Console:</p>
                <ul>
                  <li>Maps JavaScript API</li>
                  <li>Places API</li>
                  <li>Geocoding API</li>
                </ul>
              </div>
            </template>
          </el-step>
          
          <el-step title="Configure Restrictions">
            <template #description>
              <div class="step-content">
                <p>Set API key restrictions:</p>
                <ul>
                  <li>Application: HTTP referrers</li>
                  <li>Add: localhost:* (development)</li>
                  <li>Add: yourdomain.com/* (production)</li>
                </ul>
              </div>
            </template>
          </el-step>
          
          <el-step title="Enable Billing">
            <template #description>
              <div class="step-content">
                <p>Link billing account (required even for free tier)</p>
                <p>Google provides $200 free credit monthly</p>
              </div>
            </template>
          </el-step>
          
          <el-step title="Restart Server">
            <template #description>
              <div class="step-content">
                <p>After changing .env, restart your dev server:</p>
                <code>pnpm dev</code>
              </div>
            </template>
          </el-step>
        </el-steps>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import GoogleLocationPicker from '~/components/hr/location/GoogleLocationPicker.vue';

definePageMeta({
  title: 'Google Maps Diagnostic',
  layout: 'default',
});

const testing = ref(false);
const testResult = ref<{
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
} | null>(null);
const pickedLocation = ref<any>(null);
const currentStep = ref(0);

const config = useRuntimeConfig();
const apiKey = computed(() => config.public.googleMapsApiKey as string);

const apiKeyStatus = computed(() => {
  if (!apiKey.value) {
    return { type: 'danger' as const, message: 'Not Configured' };
  }
  if (apiKey.value.length < 30) {
    return { type: 'warning' as const, message: 'Invalid Format' };
  }
  return { type: 'success' as const, message: 'Configured' };
});

const apiKeyPreview = computed(() => {
  if (!apiKey.value) return 'Not set';
  return apiKey.value.substring(0, 10) + '...' + apiKey.value.substring(apiKey.value.length - 4);
});

const environment = computed(() => {
  return process.dev ? 'Development' : 'Production';
});

const protocolStatus = computed(() => {
  if (process.client) {
    const isSecure = location.protocol === 'https:' || 
                     location.hostname === 'localhost' || 
                     location.hostname === '127.0.0.1';
    return {
      type: isSecure ? 'success' as const : 'warning' as const,
      message: location.protocol + '//' + location.hostname,
    };
  }
  return { type: 'info' as const, message: 'Server Side' };
});

async function testApiKey() {
  if (!apiKey.value) {
    testResult.value = {
      type: 'error',
      title: 'API Key Missing',
      message: 'Add NUXT_PUBLIC_GOOGLE_MAPS_API_KEY to your .env file',
    };
    return;
  }

  testing.value = true;
  testResult.value = null;

  try {
    // Test by loading the API
    const testUrl = `https://maps.googleapis.com/maps/api/js?key=${apiKey.value}&libraries=places`;
    
    const response = await fetch(testUrl);
    const text = await response.text();

    if (text.includes('Google Maps JavaScript API')) {
      testResult.value = {
        type: 'success',
        title: 'API Key Valid',
        message: 'Your API key is working correctly!<br><br>If the map still doesn\'t load, check:<br>• API restrictions in Google Cloud Console<br>• Billing is enabled<br>• Required APIs are enabled',
      };
      currentStep.value = 5;
    } else if (text.includes('RefererNotAllowedMapError')) {
      testResult.value = {
        type: 'error',
        title: 'Domain Restriction Error',
        message: 'Your API key is restricted to specific domains.<br><br>Fix:<br>1. Go to Google Cloud Console<br>2. Edit API key restrictions<br>3. Add: localhost:* for development<br>4. Or temporarily remove restrictions',
      };
      currentStep.value = 2;
    } else if (text.includes('ApiNotActivatedMapError')) {
      testResult.value = {
        type: 'error',
        title: 'API Not Enabled',
        message: 'Required APIs are not enabled.<br><br>Enable these in Google Cloud Console:<br>• Maps JavaScript API<br>• Places API<br>• Geocoding API',
      };
      currentStep.value = 1;
    } else if (text.includes('InvalidKeyMapError')) {
      testResult.value = {
        type: 'error',
        title: 'Invalid API Key',
        message: 'The API key is invalid or malformed.<br><br>Check:<br>• Copy the entire key from Google Cloud Console<br>• No extra spaces or characters<br>• Key is not expired or deleted',
      };
      currentStep.value = 0;
    } else {
      testResult.value = {
        type: 'warning',
        title: 'Unknown Response',
        message: 'Received unexpected response. Check browser console for details.',
      };
    }
  } catch (error: any) {
    testResult.value = {
      type: 'error',
      title: 'Network Error',
      message: `Failed to test API key: ${error.message}<br><br>Check your internet connection.`,
    };
  } finally {
    testing.value = false;
  }
}

function handlePicked(location: any) {
  pickedLocation.value = location;
  ElMessage.success('Location picked successfully!');
}

function openGoogleCloudConsole() {
  window.open('https://console.cloud.google.com/apis/credentials', '_blank');
}

function copyEnvExample() {
  const example = 'NUXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key_here';
  navigator.clipboard.writeText(example);
  ElMessage.success('Copied to clipboard!');
}

onMounted(() => {
  if (!apiKey.value) {
    currentStep.value = 0;
  } else {
    currentStep.value = 1;
  }
});
</script>

<style scoped>
.test-page {
  padding: 24px;
  background: #f5f5f5;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
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

.status-item code {
  background: #f5f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: monospace;
}

.test-section {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.test-result {
  border-top: 1px solid #ebeef5;
  padding-top: 16px;
}

.step-content {
  padding: 8px 0;
}

.step-content ul {
  margin: 8px 0;
  padding-left: 20px;
}

.step-content code {
  background: #f5f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: monospace;
}

.loading-fallback {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .test-page {
    padding: 16px;
  }
  
  .status-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>