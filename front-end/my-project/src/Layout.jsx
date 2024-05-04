// Layout.js

import React from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";

function Layout({ children }) {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex flex-col w-full">
        <Header />
        <main className="flex-grow overflow-y-auto">
          {/* Set overflow-y-auto to allow vertical scrolling if content overflows */}
          {children}
        </main>
      </div>
    </div>
  );
}

export default Layout;
