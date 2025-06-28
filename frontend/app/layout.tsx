import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "CogniCart - AI-Powered Shopping Assistant",
  description: "Find the perfect products with our multi-agent AI system. Natural language search, review analysis, and deal discovery all in one place.",
  keywords: ["AI shopping", "product search", "e-commerce", "deals", "reviews", "comparison"],
  authors: [{ name: "CogniCart Team" }],
  openGraph: {
    title: "CogniCart - AI-Powered Shopping Assistant",
    description: "Revolutionize your shopping experience with AI-powered product recommendations",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
