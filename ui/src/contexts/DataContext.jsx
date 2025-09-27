import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import { getCollections, getPageContent } from '@/lib/api';
import { supabase } from '@/lib/supabaseClient';

const DataContext = createContext();

export const useData = () => useContext(DataContext);

export const DataProvider = ({ children }) => {
  const [collections, setCollections] = useState([]);
  const [pages, setPages] = useState({});
  const [loading, setLoading] = useState(true);

  const fetchCollections = useCallback(async () => {
    const data = await getCollections();
    setCollections(data || []);
  }, []);

  const fetchPage = useCallback(async (collectionSlug, pageSlug) => {
    const pageKey = `${collectionSlug}/${pageSlug}`;
    if (pages[pageKey]) {
      return pages[pageKey];
    }
    const pageData = await getPageContent(collectionSlug, pageSlug);
    if (pageData) {
      pageData.page_blocks.sort((a, b) => a.position - b.position);
      setPages(prev => ({ ...prev, [pageKey]: pageData }));
      return pageData;
    }
    return null;
  }, [pages]);

  useEffect(() => {
    const initialFetch = async () => {
      setLoading(true);
      await fetchCollections();
      setLoading(false);
    };
    initialFetch();

    const channel = supabase
      .channel('global-changes')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'collections' }, () => fetchCollections())
      .on('postgres_changes', { event: '*', schema: 'public', table: 'pages' }, () => fetchCollections())
      .on('postgres_changes', { event: '*', schema: 'public', table: 'page_blocks' }, (payload) => {
          // Invalidate cache for the specific page
          console.log('A block changed, invalidating page cache if needed.', payload);
          // This is a simple invalidation. A more complex app might update the cache directly.
          setPages({}); 
      })
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [fetchCollections]);

  const value = {
    collections,
    getPage: fetchPage,
    loadingInitialData: loading,
  };

  return <DataContext.Provider value={value}>{children}</DataContext.Provider>;
};
