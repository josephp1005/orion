import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const collections = [
  {
    name: 'Getting Started',
    pages: [
      { name: 'Introduction', path: '/docs/getting-started/introduction' },
      { name: 'Installation', path: '/docs/getting-started/installation' },
    ],
  },
  {
    name: 'System Design',
    pages: [
      { name: 'Architecture', path: '/docs/system-design/architecture' },
      { name: 'Components', path: '/docs/system-design/components' },
    ],
  },
];

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

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
          <div key={collection.name} className="mb-4">
            <h2 className="text-sm font-semibold text-accent mb-2">{collection.name}</h2>
            <ul>
              {collection.pages.map((page) => (
                <li key={page.path}>
                  <a
                    href={page.path}
                    onClick={(e) => {
                      e.preventDefault();
                      navigate(page.path);
                    }}
                    className={`block text-sm py-1.5 px-2 rounded-md ${
                      location.pathname === page.path
                        ? 'bg-muted border-l-2 border-primary text-text'
                        : 'text-text-muted hover:bg-muted'
                    }`}
                  >
                    {page.name}
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
