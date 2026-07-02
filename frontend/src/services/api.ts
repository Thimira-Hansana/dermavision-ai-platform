import axios from "axios";
import type { HistoryEntry, ModelInfo, PredictionResponse } from "../types/api";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
});

export async function fetchModelInfo(): Promise<ModelInfo> {
  const response = await api.get<ModelInfo>("/model-info");
  return response.data;
}

export async function fetchHistory(): Promise<HistoryEntry[]> {
  const response = await api.get<HistoryEntry[]>("/history");
  return response.data;
}

export async function predictImage(file: File): Promise<PredictionResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post<PredictionResponse>("/predict", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}
