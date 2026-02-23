import pagesData from '../../data/pages.json';

export interface PageData {
  slug: string;
  category: string;
  title: string;
  description: string;
  priority: string;
  haloscan_volume: number | string | null;
  haloscan_kd: number | string | null;
  haloscan_cpc: number | string | null;
}

const pages = pagesData as unknown as Record<string, PageData>;

export function getAllSlugs(): string[] {
  return Object.keys(pages);
}

export function getPage(slug: string): PageData | undefined {
  return pages[slug];
}

export function getPagesByCategory(category: string): PageData[] {
  return Object.values(pages).filter((p) => p.category === category);
}

export function getPagesByPriority(priority: PageData['priority']): PageData[] {
  return Object.values(pages).filter((p) => p.priority === priority);
}

export function getAllCategories(): { category: string; count: number }[] {
  const cats: Record<string, number> = {};
  for (const p of Object.values(pages)) {
    cats[p.category] = (cats[p.category] || 0) + 1;
  }
  return Object.entries(cats)
    .map(([category, count]) => ({ category, count }))
    .sort((a, b) => b.count - a.count);
}

export function getAllPages(): PageData[] {
  return Object.values(pages);
}
