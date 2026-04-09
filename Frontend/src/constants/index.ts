/**
 * Re-export all route constants with icon references
 */

export { ROUTES } from "./routes";
export { ICONS, NAVIGATION_STRUCTURE } from "./icons";

/**
 * Helper to get route with icon mapping
 */
import { ROUTES } from "./routes";
import { ICONS } from "./icons";

export const getRouteIcon = (routeName: string): string | undefined => {
  const routeKey = routeName.toUpperCase().replace(/\//g, "_");
  return ICONS[routeKey as keyof typeof ICONS];
};

/**
 * Get all routes for a specific role
 */
export const getRoleRoutes = (role: string) => {
  const roleKey = role.toUpperCase() as keyof typeof ROUTES;
  return ROUTES[roleKey] || {};
};
