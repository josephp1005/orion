// src/components/Layout.jsx
import React from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";

const Layout = () => {
  const { pathname } = useLocation();
  const isAsk = pathname.startsWith("/ask");
  const isWelcome = pathname === "/";

  return (
    <div className="flex min-h-screen bg-bg text-text">
      <Sidebar />
      <main className="flex-1 flex flex-col min-h-0 w-full">
        {isAsk ? (
          <div className="flex-1 flex flex-col h-full w-full">
            <Outlet />
          </div>
        ) : (
          isWelcome ? (
            <div className="h-full w-full flex items-center justify-center">
              <div className="text-center max-w-4xl px-6">
                <Outlet />
              </div>
            </div>
          ) : (
            <div className="mx-auto max-w-3xl px-6 py-8 prose prose-invert h-full w-full">
              <Outlet />
            </div>
          )
        )}
      </main>
    </div>
  );
};

export default Layout;