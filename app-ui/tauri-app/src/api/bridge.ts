// src/api/bridge.ts
import { getJSON, putJSON } from "./http";
import type { Settings, DashboardSummary } from "../types/bridge";

export const BridgeAPI = {
  summary(): Promise<DashboardSummary> {
    return getJSON("/dashboard/summary");
  },
  getSettings(): Promise<Settings> {
    return getJSON("/settings");
  },
  putSettings(payload: Settings): Promise<Settings> {
    return putJSON("/settings", payload);
  },
};
