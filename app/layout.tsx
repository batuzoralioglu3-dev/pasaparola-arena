import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Pasaparola Arena",
  description: "Türkçe ve İngilizce kelime oyunu, günlük mücadele ve kelime defteri.",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr">
      <body className="antialiased">{children}</body>
    </html>
  );
}
