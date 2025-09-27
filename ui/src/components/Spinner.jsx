import React from 'react';

const Spinner = () => {
  return (
    <div className="absolute inset-0 flex justify-center items-center h-full w-full">
      <div
        className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"
        role="status"
        aria-label="loading"
      >
        <span className="sr-only">Loading...</span>
      </div>
    </div>
  );
};

export default Spinner;
