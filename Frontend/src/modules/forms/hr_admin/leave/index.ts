// frontend/src/modules/forms/hr_admin/leave/index.ts
import type { FormField } from "~/components/types/form";
import type { LeaveCreateDTO, LeaveUpdateDTO } from "~/api/hr_admin/leave/leave.dto";
import dayjs from "dayjs";

export function getLeaveFormData(): Partial<LeaveCreateDTO> {
  return {
    leave_type: "annual",
    start_date: dayjs().format("YYYY-MM-DD"),
    end_date: dayjs().add(1, "day").format("YYYY-MM-DD"),
    reason: "",
  };
}

export function getLeaveUpdateFormData(leave: any): Partial<LeaveUpdateDTO> {
  return {
    leave_type: leave.leave_type,
    start_date: leave.start_date,
    end_date: leave.end_date,
    reason: leave.reason,
  };
}

export const leaveFormSchema: FormField[] = [
  {
    name: "leave_type",
    label: "Leave Type",
    type: "select",
    required: true,
    options: [
      { label: "Annual Leave", value: "annual" },
      { label: "Sick Leave", value: "sick" },
      { label: "Unpaid Leave", value: "unpaid" },
      { label: "Other", value: "other" },
    ],
    placeholder: "Select leave type",
    rules: [{ required: true, message: "Leave type is required" }],
  },
  {
    name: "start_date",
    label: "Start Date",
    type: "date",
    required: true,
    placeholder: "Select start date",
    rules: [{ required: true, message: "Start date is required" }],
  },
  {
    name: "end_date",
    label: "End Date",
    type: "date",
    required: true,
    placeholder: "Select end date",
    rules: [
      { required: true, message: "End date is required" },
      {
        validator: (rule: any, value: any, callback: any, source: any) => {
          if (value && source.start_date && value < source.start_date) {
            callback(new Error("End date must be after start date"));
          } else {
            callback();
          }
        },
      },
    ],
  },
  {
    name: "reason",
    label: "Reason",
    type: "textarea",
    required: true,
    placeholder: "Enter reason for leave",
    rows: 4,
    maxlength: 500,
    showWordLimit: true,
    rules: [
      { required: true, message: "Reason is required" },
      { max: 500, message: "Reason cannot exceed 500 characters" },
    ],
  },
];

export const leaveReviewFormSchema: FormField[] = [
  {
    name: "comment",
    label: "Comment",
    type: "textarea",
    required: false,
    placeholder: "Add a comment (optional)",
    rows: 4,
    maxlength: 500,
    showWordLimit: true,
    rules: [{ max: 500, message: "Comment cannot exceed 500 characters" }],
  },
];
