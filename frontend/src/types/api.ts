export type PredictionItem = {
  class_name?: string;
  class?: string;
  confidence: number;
};

export type PredictionResponse = {
  predicted_class: string;
  diagnosis_name: string;
  confidence: number;
  top_3_predictions: PredictionItem[];
  gradcam_url: string | null;
  inference_time_ms: number;
  model_version: string;
  timestamp: string;
  disclaimer: string;
  model_ready: boolean;
};

export type HistoryEntry = {
  id: number;
  filename: string;
  predicted_class: string;
  confidence: number;
  model_version: string;
  created_at: string;
  gradcam_url: string | null;
};

export type ModelInfo = {
  model_version: string;
  model_ready: boolean;
  model_name: string;
  class_labels: Record<string, string>;
  device: string;
};
