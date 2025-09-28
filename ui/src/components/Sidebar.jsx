import React, { useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useData } from '../contexts/DataContext';

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { collections } = useData();
  const fileInputRef = useRef(null);

  const handleUploadClick = () => {
    fileInputRef.current.click(); // trigger hidden file input
  };
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const response = await fetch("http://localhost:5050/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      const data = await response.json();
      console.log("Uploaded:", data);

      // TODO: optionally refresh collections or trigger UI update
    } catch (err) {
      console.error("Error uploading PDF:", err);
    } finally {
      e.target.value = ""; // reset input so same file can be re-uploaded if needed
    }
  };


  return (
    <aside className="w-[280px] bg-panel border-r border-border flex flex-col p-6">
      <h1 className="text-xl font-semibold text-primary mb-6">Orion</h1>
      <button
        className="w-full bg-primary text-primary-foreground hover:bg-primary/90 text-left px-4 py-2 rounded-md mb-6"
        onClick={() => navigate('/ask')}
      >
        Ask a question
      </button>
      <nav>
        {collections.map((collection) => (
          <div key={collection.id} className="mb-4">
            <h2 className="text-sm font-semibold text-accent mb-2">{collection.label}</h2>
            <ul>
              {collection.pages.map((page) => (
                <li key={page.id}>
                  <a
                    href={`/docs/${collection.slug}/${page.slug}`}
                    onClick={(e) => {
                      e.preventDefault();
                      navigate(`/docs/${collection.slug}/${page.slug}`);
                    }}
                    className={`block text-sm py-1.5 px-2 rounded-md ${
                      location.pathname === `/docs/${collection.slug}/${page.slug}`
                        ? 'bg-muted border-l-2 border-primary text-text hover:text-text'
                        : 'text-text-muted hover:bg-muted hover:text-text'
                    }`}
                  >
                    {page.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>
      {/* Floating circle upload button inside sidebar */}
      <div className="absolute bottom-6 left-20 transform -translate-x-1/2">
        <button
          onClick={handleUploadClick}
          className="w-16 h-16 p-0 rounded-full bg-primary text-primary-foreground flex items-center justify-center shadow-lg hover:bg-primary/90"
          aria-label="Upload PDF"
        >
          <svg  
            className="w-8 h-8"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            stroke="currentColor"
            strokeWidth="4" 
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >            <path d="M12 5v14" />
            <path d="M5 12h14" />
          </svg>
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={handleFileChange}
        />
      </div>
    </aside>
  );
};

export default Sidebar;
