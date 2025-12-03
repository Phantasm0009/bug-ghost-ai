"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bug, Menu, X } from "lucide-react";
import { useState } from "react";
import LoginWithGitHub from "@/components/LoginWithGitHub";

export default function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  const isActive = (href: string) => (pathname === href ? "text-blue-600 dark:text-blue-400" : "text-gray-700 dark:text-gray-300");

  return (
    <nav className="border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center space-x-2">
            <Bug className="w-6 h-6 text-blue-600" />
            <span className="font-bold text-xl">Bug Ghost AI</span>
          </Link>

          <button aria-label="Open menu" className="md:hidden p-2" onClick={() => setOpen((v) => !v)}>
            {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>

          <div className="hidden md:flex items-center space-x-6">
            <Link href="/" className={`${isActive("/")} hover:text-blue-600 dark:hover:text-blue-400 transition-colors`}>
              Home
            </Link>
            <Link href="/sessions" className={`${isActive("/sessions")} hover:text-blue-600 dark:hover:text-blue-400 transition-colors`}>
              Sessions
            </Link>
            <Link href="/teams" className={`${pathname?.startsWith("/teams") ? "text-purple-600 dark:text-purple-400" : "text-gray-700 dark:text-gray-300"} hover:text-purple-600 dark:hover:text-purple-400 transition-colors`}>
              Teams
            </Link>
            <Link href="/sandbox" className={`${pathname === "/sandbox" ? "text-green-600 dark:text-green-400" : "text-gray-700 dark:text-gray-300"} hover:text-green-600 dark:hover:text-green-400 transition-colors`}>
              Sandbox
            </Link>
            <LoginWithGitHub />
          </div>
        </div>

        {open && (
          <div className="md:hidden pb-4 space-y-3">
            <div className="flex flex-col space-y-3">
              <Link href="/" className={`${isActive("/")} hover:text-blue-600`} onClick={() => setOpen(false)}>
                Home
              </Link>
              <Link href="/sessions" className={`${isActive("/sessions")} hover:text-blue-600`} onClick={() => setOpen(false)}>
                Sessions
              </Link>
              <Link href="/teams" className={`${pathname?.startsWith("/teams") ? "text-purple-600" : "text-gray-700 dark:text-gray-300"} hover:text-purple-600`} onClick={() => setOpen(false)}>
                Teams
              </Link>
              <Link href="/sandbox" className={`${pathname === "/sandbox" ? "text-green-600" : "text-gray-700 dark:text-gray-300"} hover:text-green-600`} onClick={() => setOpen(false)}>
                Sandbox
              </Link>
              <div className="pt-2">
                <LoginWithGitHub />
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
