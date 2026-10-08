import type { Metadata } from "next";
import { Outfit } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import ClientProviders from "@/components/providers/ClientProviders";

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    template: "%s | KrowN Supply Co.",
    default: "KrowN Supply Co. | Wear the KrowN.",
  },
  description: "Official KrowN Supply Co. store. Premium apparel, workwear, gaming merchandise, and lifestyle products.",
};

import MiniCart from "@/components/cart/MiniCart";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={outfit.variable}>
      <body>
        <ClientProviders>
          <Navbar />
          <MiniCart />
          <main style={{ flex: 1 }}>{children}</main>
          <Footer />
        </ClientProviders>
      </body>
    </html>
  );
}
