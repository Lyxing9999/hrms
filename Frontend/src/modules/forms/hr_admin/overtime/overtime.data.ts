import type {
  OvertimeRequestCreateDTO,
  OvertimeRequestUpdateDTO,
  OvertimeRequestDTO,
} from "~/api/hr_admin/overtimeRequest";
import dayjs from "dayjs";
import { reactive } from "vue";

export const getOvertimeFormData = (): OvertimeRequestCreateDTO => ({
  request_date: dayjs().format("YYYY-MM-DD"),
  start_time: "",
  end_time: "",
  reason: "",
});

export const getOvertimeUpdateFormData = (
  data?: Partial<OvertimeRequestUpdateDTO>,
): OvertimeRequestUpdateDTO =>
  reactive({
    request_date: "",
    start_time: "",
    end_time: "",
    reason: "",
    ...data,
  });

export const getOvertimeReviewFormData = () =>
  reactive({
    approved: true,
    comment: "",
  });
