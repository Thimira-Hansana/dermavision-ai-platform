import { MoonStar, SunMedium } from "lucide-react";
import { Link, NavLink } from "react-router-dom";

const navItems = [
  ["Predict", "/predict"],
  ["Performance", "/performance"],
  ["History", "/history"],
  ["Docs", "/docs"],
  ["About", "/about"],
  ["Settings", "/settings"],
] as const;

type Props = {
  dark: boolean;
  onToggleTheme: () => void;
};

export function Navigation({ dark, onToggleTheme }: Props) {
  return (
    <header className="sticky top-0 z-30 border-b border-white/20 bg-sand/80 backdrop-blur dark:bg-ink/80">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-4 py-4">
        <Link to="/" className="font-display text-2xl text-ink dark:text-sand">
          DermaVision AI
        </Link>
        <nav className="hidden gap-5 md:flex">
          {navItems.map(([label, href]) => (
            <NavLink
              key={href}
              to={href}
              className={({ isActive }) =>
                `text-sm font-medium transition ${
                  isActive ? "text-ember" : "text-slate dark:text-mist"
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>
        <button
          type="button"
          onClick={onToggleTheme}
          className="rounded-full border border-slate/20 p-2 text-slate transition hover:border-ember hover:text-ember dark:border-mist/20 dark:text-mist"
        >
          {dark ? <SunMedium size={18} /> : <MoonStar size={18} />}
        </button>
      </div>
    </header>
  );
}
