import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import {ReactNode} from "react";
import StandardNavigation from "@/app/components/navigation/StandardNavigation";

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'ACH Dashboard',
  description: 'An ACH Dashboard',
}

export default function RootLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
