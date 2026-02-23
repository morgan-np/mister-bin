import Link from 'next/link';
import { getAllCategories, getPagesByPriority } from '@/lib/pages';

function formatCategoryName(cat: string): string {
  return cat
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' · ');
}

export default function HomePage() {
  const categories = getAllCategories();
  const topPages = getPagesByPriority('top');
  const highPages = getPagesByPriority('high').slice(0, 12);

  return (
    <main style={{ maxWidth: 960, margin: '0 auto', padding: '2rem 1rem', fontFamily: 'system-ui, sans-serif' }}>
      <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
        Mister Bin 🗑️
      </h1>
      <p style={{ color: '#555', marginBottom: '2rem' }}>
        Le guide complet des poubelles, tri sélectif et compost —{' '}
        {categories.reduce((sum, c) => sum + c.count, 0).toLocaleString('fr-FR')} pages
      </p>

      {topPages.length > 0 && (
        <section style={{ marginBottom: '2.5rem' }}>
          <h2 style={{ fontSize: '1.3rem', borderBottom: '2px solid #222', paddingBottom: '0.3rem' }}>
            Pages prioritaires
          </h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {topPages.map((p) => (
              <li key={p.slug} style={{ padding: '0.4rem 0' }}>
                <Link href={`/${p.slug}`}>{p.title}</Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section style={{ marginBottom: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', borderBottom: '2px solid #222', paddingBottom: '0.3rem' }}>
          À découvrir
        </h2>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {highPages.map((p) => (
            <li key={p.slug} style={{ padding: '0.4rem 0' }}>
              <Link href={`/${p.slug}`}>{p.title}</Link>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2 style={{ fontSize: '1.3rem', borderBottom: '2px solid #222', paddingBottom: '0.3rem' }}>
          Catégories ({categories.length})
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '0.5rem', marginTop: '1rem' }}>
          {categories.map((c) => (
            <div key={c.category} style={{ padding: '0.5rem 0.75rem', background: '#f5f5f5', borderRadius: 6 }}>
              <span>{formatCategoryName(c.category)}</span>
              <span style={{ color: '#888', marginLeft: '0.5rem', fontSize: '0.85rem' }}>
                {c.count}
              </span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
