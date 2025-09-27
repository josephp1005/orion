import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { getCollections } from '../lib/api';

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [collections, setCollections] = useState([]);

  useEffect(() => {
    const fetchCollections = async () => {
      const data = await getCollections();
      setCollections(data);
    };
    fetchCollections();
  }, []);

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
                        ? 'bg-muted border-l-2 border-primary text-text'
                        : 'text-text-muted hover:bg-muted'
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
    </aside>
  );
};

export default Sidebar;
