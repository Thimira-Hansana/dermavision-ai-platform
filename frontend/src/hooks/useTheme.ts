import { useEffect, useState } from "react";

const STORAGE_KEY = "dermavision-theme";

export function useTheme(): [boolean, () => void] {
  const [dark, setDark] = useState<boolean>(() => localStorage.getItem(STORAGE_KEY) === "dark");

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem(STORAGE_KEY, dark ? "dark" : "light");
  }, [dark]);

  return [dark, () => setDark((current) => !current)];
}
