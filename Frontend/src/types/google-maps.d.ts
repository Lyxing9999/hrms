declare global {
  interface Window {
    google: typeof google;
    initMap?: () => void;
  }
}

export interface GoogleMapsConfig {
  apiKey: string;
  libraries: string[];
}

export interface MapOptions {
  center: google.maps.LatLngLiteral;
  zoom: number;
  mapTypeId?: google.maps.MapTypeId;
  disableDefaultUI?: boolean;
  zoomControl?: boolean;
  streetViewControl?: boolean;
  fullscreenControl?: boolean;
}

export interface MarkerOptions {
  position: google.maps.LatLngLiteral;
  map: google.maps.Map;
  draggable?: boolean;
  title?: string;
}

export interface CircleOptions {
  center: google.maps.LatLngLiteral;
  radius: number;
  map: google.maps.Map;
  fillColor?: string;
  fillOpacity?: number;
  strokeColor?: string;
  strokeOpacity?: number;
  strokeWeight?: number;
}

export interface PlaceSearchRequest {
  query: string;
  fields: string[];
}

export interface GeolocationPosition {
  coords: {
    latitude: number;
    longitude: number;
    accuracy: number;
  };
}

export {};