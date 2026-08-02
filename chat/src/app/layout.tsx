import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = { title: "旅 Canvas — AI Journey Studio", description: "会話から旅を描くAI旅行プランナー" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="ja"><body>{children}</body></html>; }
