import Link from 'next/link';
import { getAllCategories, getPagesByPriority } from '@/lib/pages';

function formatCategoryName(cat: string): string {
  return cat
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

export default function HomePage() {
  const categories = getAllCategories();
  const topPages = getPagesByPriority('top');
  const highPages = getPagesByPriority('high').slice(0, 12);

  return (
    <>
      <section className="hero">
        <h1>Mister Bin</h1>
        <p>
          Le guide complet des poubelles, tri selectif et compost &mdash;{' '}
          {categories.reduce((sum, c) => sum + c.count, 0).toLocaleString('fr-FR')} pages
        </p>
      </section>

      {topPages.length > 0 && (
        <section>
          <h2 className="section-title">Pages prioritaires</h2>
          <div className="card-grid">
            {topPages.map((p) => (
              <Link key={p.slug} href={`/${p.slug}`} style={{ textDecoration: 'none' }}>
                <div className="card">
                  <div className="card-title">{p.title}</div>
                  {p.description && (
                    <div className="card-meta" style={{ marginTop: '0.3rem' }}>
                      {p.description.length > 90
                        ? p.description.slice(0, 90) + '...'
                        : p.description}
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}

      {highPages.length > 0 && (
        <section>
          <h2 className="section-title">A decouvrir</h2>
          <ul className="page-list">
            {highPages.map((p) => (
              <li key={p.slug}>
                <Link href={`/${p.slug}`}>{p.title}</Link>
                {p.haloscan_volume != null && typeof p.haloscan_volume === 'number' && (
                  <span className="card-meta" style={{ marginLeft: '0.75rem' }}>
                    {p.haloscan_volume.toLocaleString('fr-FR')} rech./mois
                  </span>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      <section id="categories">
        <h2 className="section-title">Categories ({categories.length})</h2>
        <div className="category-grid">
          {categories.map((c) => (
            <div key={c.category} className="category-pill">
              <span>{formatCategoryName(c.category)}</span>
              <span className="category-count">{c.count}</span>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
