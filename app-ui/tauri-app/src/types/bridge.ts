// src/types/bridge.ts
export type Strictness = "gentle" | "balanced" | "focused" | "monk";

export interface Settings {
  strictness: Strictness;
  nudge_budget_per_hour: number;
  cooldown_seconds: number;
  quiet_hours: { start: string; end: string }[];
  profiles: Record<string, { switch_rate_threshold: number; idle_ratio_threshold: number }>;
  privacy: { log_keystroke_content: boolean; hash_titles: boolean; camera_enabled: boolean; audio_enabled: boolean };
  policy_limits: { max_dnd_minutes: number; allow_fullscreen_prompts: boolean; meeting_detection_enabled: boolean };
}

export interface DashboardSummary {
  last_hour_counts: Record<string, number>;
  last_events: any[];         // you can refine later
  recent_features: any[];     // you can refine later
}
