import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getPageContent } from '@/lib/api';
import Block from '@/components/Block';

export default function DocPage() {
  const [page, setPage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { collection: collectionSlug, slug: pageSlug } = useParams();

  useEffect(() => {
    const fetchPage = async () => {
      try {
        setLoading(true);
        const pageData = await getPageContent(collectionSlug, pageSlug);
        if (pageData) {
          // Sort blocks by position
          pageData.page_blocks.sort((a, b) => a.position - b.position);
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

    fetchPage();
  }, [collectionSlug, pageSlug]);

  if (loading) {
    return <div className="mx-auto max-w-3xl px-6 py-8 text-white">Loading...</div>;
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

