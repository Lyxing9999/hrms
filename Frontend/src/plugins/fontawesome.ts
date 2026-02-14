import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

// Solid icons you will use
import {
    faIdBadge,
    faUser,
    faBuilding,
    faBriefcase,
    faBarcode,
    faCircleCheck,
    faCalendarDays,
    faMoneyBillWave,
    faFileContract,
    faClock,
    faImage,
} from "@fortawesome/free-solid-svg-icons";

export default defineNuxtPlugin((nuxtApp) => {
    library.add(
        faIdBadge,
        faUser,
        faBuilding,
        faBriefcase,
        faBarcode,
        faCircleCheck,
        faCalendarDays,
        faMoneyBillWave,
        faFileContract,
        faClock,
        faImage
    );

    nuxtApp.vueApp.component("FontAwesomeIcon", FontAwesomeIcon);
});