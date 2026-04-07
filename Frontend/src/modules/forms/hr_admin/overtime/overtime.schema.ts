import type { Field } from "~/components/types/form";
import {
  ElInput,
  ElDatePicker,
  ElTimePicker,
  ElInputNumber,
} from "element-plus";
import {
  Calendar,
  Clock,
  Document,
  Clock as ClockIcon,
} from "@element-plus/icons-vue";
import type {
  OvertimeRequestCreateDTO,
  OvertimeRequestUpdateDTO,
} from "~/api/hr_admin/overtimeRequest";

export const overtimeFormSchema: Field<OvertimeRequestCreateDTO>[] = [
  {
    row: [
      {
        key: "request_date",
        label: "Date",
        component: ElDatePicker,
        componentProps: {
          type: "date",
          placeholder: "Select date",
          valueFormat: "YYYY-MM-DD",
          suffixIcon: Calendar,
          disabledDate: (time: Date) => {
            // Cannot request overtime for past dates or more than 30 days in advance
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const maxDate = new Date(today);
            maxDate.setDate(maxDate.getDate() + 30);
            return time < today || time > maxDate;
          },
        },
        formItemProps: {
          rules: [
            { required: true, message: "Date is required", trigger: "change" },
          ],
        },
      },
    ],
  },
  {
    row: [
      {
        key: "start_time",
        label: "Start Time",
        component: ElTimePicker,
        componentProps: {
          format: "HH:mm",
          placeholder: "Select start time",
          suffixIcon: Clock,
        },
        formItemProps: {
          rules: [
            {
              required: true,
              message: "Start time is required",
              trigger: "change",
            },
          ],
        },
      },
      {
        key: "end_time",
        label: "End Time",
        component: ElTimePicker,
        componentProps: {
          format: "HH:mm",
          placeholder: "Select end time",
          suffixIcon: Clock,
        },
        formItemProps: {
          rules: [
            {
              required: true,
              message: "End time is required",
              trigger: "change",
            },
            {
              validator: (rule, value, callback) => {
                const form = (rule as any).form || {};
                if (form.start_time && value) {
                  if (value <= form.start_time) {
                    callback(new Error("End time must be after start time"));
                  } else {
                    callback();
                  }
                } else {
                  callback();
                }
              },
              trigger: "change",
            },
          ],
        },
      },
    ],
  },
  {
    row: [
      {
        key: "reason",
        label: "Reason",
        component: ElInput,
        componentProps: {
          type: "textarea",
          placeholder: "Enter reason for overtime",
          maxlength: 500,
          showWordLimit: true,
          rows: 4,
          suffixIcon: Document,
        },
        formItemProps: {
          rules: [
            {
              required: true,
              message: "Reason is required",
              trigger: "change",
            },
            {
              min: 10,
              message: "Reason must be at least 10 characters",
              trigger: "change",
            },
          ],
        },
      },
    ],
  },
];

export const overtimeUpdateFormSchema: Field<OvertimeRequestUpdateDTO>[] = [
  {
    row: [
      {
        key: "request_date",
        label: "Date",
        component: ElDatePicker,
        componentProps: {
          type: "date",
          placeholder: "Select date",
          valueFormat: "YYYY-MM-DD",
          suffixIcon: Calendar,
          disabledDate: (time: Date) => {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const maxDate = new Date(today);
            maxDate.setDate(maxDate.getDate() + 30);
            return time < today || time > maxDate;
          },
        },
        formItemProps: {
          rules: [
            { required: false, message: "Date is required", trigger: "change" },
          ],
        },
      },
    ],
  },
  {
    row: [
      {
        key: "start_time",
        label: "Start Time",
        component: ElTimePicker,
        componentProps: {
          format: "HH:mm",
          placeholder: "Select start time",
          suffixIcon: Clock,
        },
        formItemProps: {
          rules: [
            {
              required: false,
              message: "Start time is required",
              trigger: "change",
            },
          ],
        },
      },
      {
        key: "end_time",
        label: "End Time",
        component: ElTimePicker,
        componentProps: {
          format: "HH:mm",
          placeholder: "Select end time",
          suffixIcon: Clock,
        },
        formItemProps: {
          rules: [
            {
              required: false,
              message: "End time is required",
              trigger: "change",
            },
          ],
        },
      },
    ],
  },
  {
    row: [
      {
        key: "reason",
        label: "Reason",
        component: ElInput,
        componentProps: {
          type: "textarea",
          placeholder: "Enter reason for overtime",
          maxlength: 500,
          showWordLimit: true,
          rows: 4,
          suffixIcon: Document,
        },
        formItemProps: {
          rules: [
            {
              required: false,
              message: "Reason is required",
              trigger: "change",
            },
          ],
        },
      },
    ],
  },
];

export const overtimeReviewFormSchema: Field<{
  approved: boolean;
  comment?: string;
}>[] = [
  {
    row: [
      {
        key: "approved",
        label: "Action",
        component: ElInput,
        componentProps: {
          disabled: true,
          modelValue: "Will be set automatically",
        },
      },
    ],
  },
  {
    row: [
      {
        key: "comment",
        label: "Manager Comment",
        component: ElInput,
        componentProps: {
          type: "textarea",
          placeholder: "Add your comment (optional)",
          maxlength: 500,
          showWordLimit: true,
          rows: 4,
          suffixIcon: Document,
        },
        formItemProps: {
          rules: [
            {
              required: false,
              message: "Comment is not required",
              trigger: "change",
            },
          ],
        },
      },
    ],
  },
];
