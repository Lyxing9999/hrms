import { computed, reactive, ref } from "vue";

type Id = string | number;

export interface UseCrudDialogOptions<
  TForm extends Record<string, any>,
  TItem extends Record<string, any>,
  TId extends Id = string,
> {
  initialForm: () => TForm;

  getId: (item: TItem) => TId;

  mapToForm?: (item: TItem) => Partial<TForm>;

  fetchDetail?: (id: TId) => Promise<TItem>;

  createItem: (payload: TForm) => Promise<unknown>;
  updateItem: (id: TId, payload: Partial<TForm>) => Promise<unknown>;

  afterSave?: () => Promise<void> | void;
}

export function useCrudDialog<
  TForm extends Record<string, any>,
  TItem extends Record<string, any>,
  TId extends Id = string,
>(options: UseCrudDialogOptions<TForm, TItem, TId>) {
  const visible = ref(false);
  const isEdit = ref(false);
  const editingId = ref<TId | null>(null);

  const loading = ref(false);
  const initialLoading = ref(false);

  const form = reactive<TForm>(options.initialForm());

  const dialogTitle = computed(() => (isEdit.value ? "Edit" : "Create"));

  function resetForm() {
    const fresh = options.initialForm();

    Object.keys(form).forEach((key) => {
      delete (form as Record<string, any>)[key];
    });

    Object.assign(form, fresh);
  }

  function patchForm(payload: Partial<TForm>) {
    Object.assign(form, payload);
  }

  function openCreateDialog() {
    isEdit.value = false;
    editingId.value = null;
    resetForm();
    visible.value = true;
  }

  async function openEditDialog(item: TItem) {
    isEdit.value = true;
    visible.value = true;

    const id = options.getId(item);
    editingId.value = id;

    resetForm();

    if (options.fetchDetail) {
      initialLoading.value = true;
      try {
        const detail = await options.fetchDetail(id);
        const mapped = options.mapToForm
          ? options.mapToForm(detail)
          : (detail as Partial<TForm>);
        patchForm(mapped);
      } finally {
        initialLoading.value = false;
      }
      return;
    }

    const mapped = options.mapToForm
      ? options.mapToForm(item)
      : (item as Partial<TForm>);
    patchForm(mapped);
  }

  function closeDialog() {
    visible.value = false;
  }

  function cancelDialog() {
    closeDialog();
    resetForm();
    isEdit.value = false;
    editingId.value = null;
  }

  async function save() {
    loading.value = true;
    try {
      if (isEdit.value && editingId.value !== null) {
        await options.updateItem(editingId.value, { ...form });
      } else {
        await options.createItem({ ...form });
      }

      closeDialog();
      resetForm();
      isEdit.value = false;
      editingId.value = null;

      await options.afterSave?.();
    } finally {
      loading.value = false;
    }
  }

  return {
    visible,
    isEdit,
    editingId,
    loading,
    initialLoading,
    form,
    dialogTitle,

    resetForm,
    patchForm,

    openCreateDialog,
    openEditDialog,
    closeDialog,
    cancelDialog,
    save,
  };
}
