# API Layer Documentation

This project uses a 3-file structure per API domain to keep networking, application behavior, and UI logic separated.

## Folder Structure

Each API module contains 3 files:

- `*.dto.ts` — Data Transfer Objects (types)
- `*.api.ts` — Low-level HTTP calls (Axios/Http)
- `*.service.ts` — High-level wrapper (app policy & behavior)

---

## Responsibilities

### 1) DTO (`*.dto.ts`) — "What data looks like"

Defines types/interfaces for:

- request payloads (create/update)
- query params
- response shapes (including `ApiResponse<T>`)
- pagination structures

Only types.  
No HTTP calls. No UI logic.

---

### 2) API (`*.api.ts`) — "How to talk to the server"

Responsible for:

- building endpoint URLs
- choosing HTTP method (GET/POST/PUT/PATCH/DELETE)
- passing query params / request body
- returning raw backend response (usually `ApiResponse<T>`)

Pure network layer.  
No toast messages. No caching. No business rules.

Example:

```ts
// api.ts
getClasses(params) {
  return this.$api.get("/api/admin/classes", { params }).then(r => r.data);
}
```
