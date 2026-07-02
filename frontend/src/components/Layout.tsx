import { PropsWithChildren } from "react";
import { Navigation } from "./Navigation";

type Props = PropsWithChildren<{
  dark: boolean;
  onToggleTheme: () => void;
}>;

export function Layout({ children, dark, onToggleTheme }: Props) {
  return (
    <div className="min-h-screen bg-sand bg-halo text-ink transition-colors dark:bg-ink dark:text-sand">
      <Navigation dark={dark} onToggleTheme={onToggleTheme} />
      <main className="mx-auto max-w-7xl px-4 py-8">{children}</main>
    </div>
  );
}
