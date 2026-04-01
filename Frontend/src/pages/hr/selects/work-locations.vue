<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { ElSelect, ElOption } from "element-plus";
import { hrmsAdminService } from "~/api/hr_admin";
import type { SelectOptionDTO } from "~/api/types/common/select-option.type";

interface Props {
  modelValue?: string | null;
  placeholder?: string;
  clearable?: boolean;
  disabled?: boolean;
  filterable?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  placeholder: "Select work location",
  clearable: true,
  disabled: false,
  filterable: true,
});

const emit = defineEmits<{
  (e: "update:modelValue", value: string | null): void;
  (e: "change", value: string | null): void;
}>();

const workLocationService = hrmsAdminService().workLocation;

const loading = ref(false);
const options = ref<SelectOptionDTO[]>([]);

const innerValue = computed({
  get: () => props.modelValue ?? null,
  set: (value: string | null) => {
    emit("update:modelValue", value);
    emit("change", value);
  },
});

const fetchOptions = async () => {
  loading.value = true;
  try {
    options.value = await workLocationService.getWorkLocationSelectOptions();
  } finally {
    loading.value = false;
  }
};

onMounted(fetchOptions);
</script>

<template>
  <ElSelect
    v-model="innerValue"
    :loading="loading"
    :placeholder="placeholder"
    :clearable="clearable"
    :disabled="disabled"
    :filterable="filterable"
    class="w-full"
  >
    <ElOption
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </ElSelect>
</template>
