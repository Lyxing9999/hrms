import { ref, computed } from "vue";
import type {
  HrCreateEmployeeDTO,
  HrEmployeeDTO,
  HrUpdateEmployeeDTO,
  HrCreateEmployeeAccountDTO,
} from "~/api/hr_admin/employees/dto";
import type { Field } from "~/components/types/form";
import { ElInput, ElInputNumber, ElOption, ElSelect } from "element-plus";
import { Role } from "~/api/types/enums/role.enum";

export function useHrEmployeeForms() {
  const createVisible = ref(false);
  const editVisible = ref(false);
  const createAccountVisible = ref(false);

  const createLoading = ref(false);
  const editLoading = ref(false);
  const createAccountLoading = ref(false);
  const detailLoadingMap = ref<Record<string, boolean>>({});

  const editingEmployeeId = ref<string>("");

  const createData = ref<Partial<HrCreateEmployeeDTO>>({
    employee_code: "",
    full_name: "",
    department: "",
    position: "",
    employment_type: "contract",
    basic_salary: 0,
    status: "active",
  });

  const editData = ref<Partial<HrUpdateEmployeeDTO>>({});
  const createAccountData = ref<Partial<HrCreateEmployeeAccountDTO>>({
    username: "",
    email: "",
    password: "",
    role: Role.EMPLOYEE,
  });

  const employeeFields = computed<Field<HrCreateEmployeeDTO>[]>(() => [
    {
      key: "employee_code",
      label: "Employee Code",
      component: ElInput,
      componentProps: { placeholder: "Enter employee code", clearable: true },
    },
    {
      key: "full_name",
      label: "Full Name",
      component: ElInput,
      componentProps: { placeholder: "Enter full name", clearable: true },
    },
    {
      key: "department",
      label: "Department",
      component: ElInput,
      componentProps: { placeholder: "Enter department", clearable: true },
    },
    {
      key: "position",
      label: "Position",
      component: ElInput,
      componentProps: { placeholder: "Enter position", clearable: true },
    },
    {
      key: "employment_type",
      label: "Employment Type",
      component: ElSelect,
      childComponent: ElOption,
      childComponentProps: {
        options: [
          { label: "Contract", value: "contract" },
          { label: "Permanent", value: "permanent" },
        ],
        valueKey: "value",
        labelKey: "label",
      },
    },
    {
      key: "basic_salary",
      label: "Basic Salary",
      component: ElInputNumber,
      componentProps: { min: 0, style: { width: "100%" } },
    },
    {
      key: "status",
      label: "Status",
      component: ElSelect,
      childComponent: ElOption,
      childComponentProps: {
        options: [
          { label: "Active", value: "active" },
          { label: "Inactive", value: "inactive" },
        ],
        valueKey: "value",
        labelKey: "label",
      },
    },
  ]);

  const createAccountFields = computed<Field<HrCreateEmployeeAccountDTO>[]>(
    () => [
      {
        key: "email",
        label: "Email",
        component: ElInput,
        componentProps: { placeholder: "Enter email", clearable: true },
      },
      {
        key: "username",
        label: "Username",
        component: ElInput,
        componentProps: { placeholder: "Enter username", clearable: true },
      },
      {
        key: "password",
        label: "Password",
        component: ElInput,
        componentProps: {
          placeholder: "Enter password",
          type: "password",
          showPassword: true,
        },
      },
    ],
  );

  function openCreate() {
    createVisible.value = true;
    createData.value = {
      employee_code: "",
      full_name: "",
      department: "",
      position: "",
      employment_type: "contract",
      basic_salary: 0,
      status: "active",
    };
  }

  function openEdit(row: HrEmployeeDTO) {
    editingEmployeeId.value = row.id;
    editVisible.value = true;
    editData.value = { ...row };
  }

  function openCreateAccount(employee: HrEmployeeDTO) {
    editingEmployeeId.value = employee.id;
    createAccountVisible.value = true;
    createAccountData.value = {
      username: employee.full_name.toLowerCase().replace(/\s+/g, "."),
      email: "",
      password: "",
      role: Role.EMPLOYEE,
    };
  }

  function detailLoading(id: string | number) {
    return !!detailLoadingMap.value[String(id)];
  }

  return {
    openCreate,
    openEdit,
    openCreateAccount,
    detailLoading,
    editingEmployeeId,

    createVisible,
    createData,
    createSchema: employeeFields,
    createLoading,

    editVisible,
    editData,
    editSchema: employeeFields,
    editLoading,

    createAccountVisible,
    createAccountData,
    createAccountSchema: createAccountFields,
    createAccountLoading,
  };
}
