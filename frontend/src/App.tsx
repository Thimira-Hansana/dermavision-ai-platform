import { Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { useTheme } from "./hooks/useTheme";
import { AboutPage } from "./pages/AboutPage";
import { DocumentationPage } from "./pages/DocumentationPage";
import { HistoryPage } from "./pages/HistoryPage";
import { LandingPage } from "./pages/LandingPage";
import { PerformancePage } from "./pages/PerformancePage";
import { PredictionPage } from "./pages/PredictionPage";
import { SettingsPage } from "./pages/SettingsPage";

export default function App() {
  const [dark, toggleTheme] = useTheme();

  return (
    <Layout dark={dark} onToggleTheme={toggleTheme}>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/predict" element={<PredictionPage />} />
        <Route path="/performance" element={<PerformancePage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/docs" element={<DocumentationPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Layout>
  );
}
