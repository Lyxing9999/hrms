/// <reference types="@types/google.maps" />

declare global {
  interface Window {
    google?: typeof google;
  }
}

export interface LocationPickerResult {
  latitude: number;
  longitude: number;
  address?: string;
}

export {};