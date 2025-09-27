// src/components/Layout.jsx
import React from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";

const Layout = () => {
  const { pathname } = useLocation();
  const isAsk = pathname.startsWith("/ask");

  return (
    <div className="flex h-screen bg-bg text-text">
      <Sidebar />
      <main className="flex-1 min-h-0 overflow-hidden">
        {isAsk ? (
          <div className="h-full w-full">
            <Outlet />
          </div>
        ) : (
          <div className="mx-auto max-w-3xl px-6 py-8 prose prose-invert">
            <Outlet />
          </div>
        )}
      </main>
    </div>
  );
};

export default Layout;
