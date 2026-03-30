<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from "vue";

interface Props {
  latitude: number | null;
  longitude: number | null;
  radiusMeters?: number;
  height?: string;
  disabled?: boolean;
  address?: string;
}

const props = withDefaults(defineProps<Props>(), {
  radiusMeters: 100,
  height: "420px",
  disabled: false,
  address: "",
});

const emit = defineEmits<{
  (e: "update:latitude", value: number): void;
  (e: "update:longitude", value: number): void;
  (e: "update:address", value: string): void;
  (
    e: "picked",
    payload: { latitude: number; longitude: number; address?: string },
  ): void;
}>();

const mapEl = ref<HTMLDivElement | null>(null);
const searchInput = ref<HTMLInputElement | null>(null);

const map = ref<any>(null);
const marker = ref<any>(null);
const circle = ref<any>(null);
const geocoder = ref<any>(null);
const autocomplete = ref<any>(null);

const loading = ref(true);

const center = computed(() => ({
  lat: props.latitude ?? 11.5564,
  lng: props.longitude ?? 104.9282,
}));

const googleMaps = useScriptGoogleMaps({
  libraries: ["places"],
});

const setPosition = async (
  lat: number,
  lng: number,
  shouldReverseGeocode = true,
) => {
  emit("update:latitude", lat);
  emit("update:longitude", lng);

  const latLng = { lat, lng };

  if (marker.value) {
    marker.value.setPosition(latLng);
  }

  if (circle.value) {
    circle.value.setCenter(latLng);
  }

  if (map.value) {
    map.value.panTo(latLng);
  }

  if (shouldReverseGeocode && geocoder.value) {
    geocoder.value.geocode({ location: latLng }, (results, status) => {
      if (status === "OK" && results?.[0]) {
        emit("update:address", results[0].formatted_address);
        emit("picked", {
          latitude: lat,
          longitude: lng,
          address: results[0].formatted_address,
        });
      } else {
        emit("picked", { latitude: lat, longitude: lng });
      }
    });
  } else {
    emit("picked", { latitude: lat, longitude: lng });
  }
};

const initMap = async () => {
  loading.value = true;

  const google = await googleMaps.onLoaded();
  await nextTick();

  if (!mapEl.value) return;

  geocoder.value = new google.maps.Geocoder();

  map.value = new google.maps.Map(mapEl.value, {
    center: center.value,
    zoom: 15,
    mapTypeControl: false,
    streetViewControl: false,
    fullscreenControl: true,
    clickableIcons: false,
  });

  marker.value = new google.maps.Marker({
    position: center.value,
    map: map.value,
    draggable: !props.disabled,
  });

  circle.value = new google.maps.Circle({
    map: map.value,
    center: center.value,
    radius: props.radiusMeters,
    fillColor: "#409eff",
    fillOpacity: 0.18,
    strokeColor: "#409eff",
    strokeOpacity: 0.8,
    strokeWeight: 1,
  });

  map.value.addListener("click", (event: google.maps.MapMouseEvent) => {
    if (props.disabled) return;
    if (!event.latLng) return;

    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    void setPosition(lat, lng, true);
  });

  marker.value.addListener("dragend", (event: google.maps.MapMouseEvent) => {
    if (!event.latLng) return;

    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    void setPosition(lat, lng, true);
  });

  if (searchInput.value) {
    autocomplete.value = new google.maps.places.Autocomplete(
      searchInput.value,
      {
        fields: ["formatted_address", "geometry", "name"],
      },
    );

    autocomplete.value.addListener("place_changed", () => {
      const place = autocomplete.value?.getPlace();
      const location = place?.geometry?.location;

      if (!location) return;

      const lat = location.lat();
      const lng = location.lng();

      emit("update:address", place?.formatted_address || place?.name || "");
      void setPosition(lat, lng, false);

      if (map.value) {
        map.value.setCenter({ lat, lng });
        map.value.setZoom(17);
      }

      emit("picked", {
        latitude: lat,
        longitude: lng,
        address: place?.formatted_address || place?.name || "",
      });
    });
  }

  loading.value = false;
};

const useCurrentLocation = () => {
  if (!navigator.geolocation) return;

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      await setPosition(
        position.coords.latitude,
        position.coords.longitude,
        true,
      );
      map.value?.setZoom(17);
    },
    () => {},
    { enableHighAccuracy: true, timeout: 10000 },
  );
};

const openExternalMap = () => {
  const lat = props.latitude ?? center.value.lat;
  const lng = props.longitude ?? center.value.lng;
  window.open(`https://www.google.com/maps?q=${lat},${lng}`, "_blank");
};

watch(
  () => props.radiusMeters,
  (val) => {
    if (circle.value && typeof val === "number") {
      circle.value.setRadius(val);
    }
  },
);

watch(
  () => [props.latitude, props.longitude] as const,
  ([lat, lng]) => {
    if (typeof lat === "number" && typeof lng === "number") {
      const pos = { lat, lng };
      marker.value?.setPosition(pos);
      circle.value?.setCenter(pos);
    }
  },
);

onMounted(() => {
  void initMap();
});

defineExpose({
  useCurrentLocation,
  openExternalMap,
});
</script>

<template>
  <div class="space-y-3">
    <div class="flex gap-2">
      <el-input
        ref="searchInput"
        :model-value="address"
        placeholder="Search place or address"
        clearable
      />
      <el-button @click="useCurrentLocation"> Current Location </el-button>
      <el-button plain @click="openExternalMap"> Open Map </el-button>
    </div>

    <div
      class="overflow-hidden rounded-xl border border-gray-200"
      :style="{ height }"
    >
      <div ref="mapEl" class="h-full w-full" />
    </div>

    <div class="grid grid-cols-1 gap-3 md:grid-cols-3">
      <el-card shadow="never">
        <div class="text-xs text-gray-500">Latitude</div>
        <div class="font-medium">{{ latitude ?? "-" }}</div>
      </el-card>

      <el-card shadow="never">
        <div class="text-xs text-gray-500">Longitude</div>
        <div class="font-medium">{{ longitude ?? "-" }}</div>
      </el-card>

      <el-card shadow="never">
        <div class="text-xs text-gray-500">Radius</div>
        <div class="font-medium">{{ radiusMeters }} meters</div>
      </el-card>
    </div>
  </div>
</template>
