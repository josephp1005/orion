import { supabase } from './supabaseClient';

export const getCollections = async () => {
  const { data, error } = await supabase
    .from('collections')
    .select('*, pages(*)')
    .order('position', { ascending: true })
    .order('position', { foreignTable: 'pages', ascending: true });

  if (error) {
    console.error('Error fetching collections:', error);
    return [];
  }
  return data;
};

export const getPageContent = async (collectionSlug, pageSlug) => {
  const { data, error } = await supabase
    .from('collections')
    .select('*, pages!inner(*, page_blocks(*))')
    .eq('slug', collectionSlug)
    .eq('pages.slug', pageSlug)
    .single();

  if (error) {
    console.error('Error fetching page content:', error);
    return null;
  }
  
  if (data && data.pages.length > 0) {
    return data.pages[0];
  }

  return null;
};
