import React from "react";
import { useEffect, useMemo, useState } from "react";

const WelcomePage = () => {
  return (
    <div className="relative w-full h-full flex items-center justify-center">

      {/* Welcome Text in the foreground */}
      <div className="relative z-10 flex flex-col items-center text-center ml-60">
        <h1 className="text-4xl font-bold text-white mb-4">
          Welcome to Orion
        </h1>
        <p className="text-lg text-white/80 max-w-2xl">
          Browse topics to learn and ask questions to AI trained on your team's
          work.
        </p>
      </div>
    </div>
  );
};

export default WelcomePage;