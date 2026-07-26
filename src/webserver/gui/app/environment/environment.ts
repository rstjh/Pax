export const environment = {
  API_VERSION: "1",
  // Origin of the Pax Django backend. The frontend and backend run as
  // separate containers/ports in dev (:3000 vs :8200), so API calls need an
  // absolute origin rather than a relative path.
  API_BASE_URL: "http://localhost:8200",
  // Host:port of the external C2 REST API this app integrates with. No default
  // in this dev environment; set to the real C2 host for a live deployment.
  C2_REST_API: ""
};
