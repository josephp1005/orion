import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useData } from '@/contexts/DataContext';
import Block from '@/components/Block';

export default function DocPage() {
  const [page, setPage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { collection: collectionSlug, slug: pageSlug } = useParams();
  const { getPage } = useData();

  useEffect(() => {
    const loadPage = async () => {
      try {
        setLoading(true);
        const pageData = await getPage(collectionSlug, pageSlug);
        if (pageData) {
          setPage(pageData);
        } else {
          setError('Page not found.');
        }
      } catch (err) {
        setError('Failed to load page content.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadPage();
  }, [collectionSlug, pageSlug, getPage]);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
      </div>
    );
  }

  if (error) {
    return <div className="mx-auto max-w-3xl px-6 py-8 text-red-500">{error}</div>;
  }

  if (!page) {
    return null;
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-8">
      <article>
        {page.page_blocks.map((block) => (
          <Block key={block.id} block={block} />
        ))}
      </article>
    </div>
  );
}

