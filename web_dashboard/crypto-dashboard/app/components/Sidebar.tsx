"use client";

import {
  LayoutDashboard,
  TrendingUp,
  Settings,
  Sparkles,
  Radio,
  Menu,
  X,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";

type MenuItem = {
  name: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
  href: string;
};

const menuItems: MenuItem[] = [
  { name: "Dashboard", icon: LayoutDashboard, href: "/" },
  { name: "Market", icon: TrendingUp, href: "/market" },
  { name: "Live Monitor", icon: Radio, href: "/live" },
  { name: "AI Playground", icon: Sparkles, href: "/playground" },
  { name: "Settings", icon: Settings, href: "/settings" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  // Check if we're on mobile
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  const MenuItemComponent = ({ item }: { item: MenuItem }) => {
    const Icon = item.icon;
    const isActive = pathname === item.href;

    return (
      <Link
        href={item.href}
        onClick={closeMobileMenu}
        className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all-fast ${
          isActive
            ? "bg-blue-600 text-white shadow-md"
            : "text-slate-300 hover:bg-slate-700 hover:text-white hover:shadow-sm"
        }`}
      >
        <Icon size={20} className="flex-shrink-0" />
        <span className="font-medium truncate">{item.name}</span>
      </Link>
    );
  };

  // Desktop sidebar
  if (!isMobile) {
    return (
      <aside className="w-64 bg-slate-800 border-r border-slate-700 min-h-screen p-6 sticky top-0">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Crypto Sentiment</h1>
          <p className="text-sm text-slate-400 mt-1">Analytics Dashboard</p>
        </div>

        <nav className="space-y-2">
          {menuItems.map((item) => (
            <MenuItemComponent key={item.name} item={item} />
          ))}
        </nav>
      </aside>
    );
  }

  // Mobile sidebar (drawer)
  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={toggleMobileMenu}
        className="fixed top-4 left-4 z-50 p-2 bg-slate-800 rounded-lg shadow-lg touch-target"
        aria-label="Toggle menu"
      >
        {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Mobile sidebar drawer */}
      <div
        className={`
        fixed inset-y-0 left-0 z-40 w-64 bg-slate-800 border-r border-slate-700
        transform transition-transform duration-300 ease-in-out
        ${isMobileMenuOpen ? "translate-x-0" : "-translate-x-full"}
      `}
      >
        <div className="p-6 h-full flex flex-col">
          <div className="mb-8 mt-12">
            <h1 className="text-2xl font-bold text-white">Crypto Sentiment</h1>
            <p className="text-sm text-slate-400 mt-1">Analytics Dashboard</p>
          </div>

          <nav className="space-y-2 flex-1">
            {menuItems.map((item) => (
              <MenuItemComponent key={item.name} item={item} />
            ))}
          </nav>
        </div>
      </div>

      {/* Overlay */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={closeMobileMenu}
        />
      )}
    </>
  );
}
