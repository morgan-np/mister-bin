import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getAllSlugs, getPage, getPagesByCategory } from '@/lib/pages';
import type { Metadata } from 'next';

export function generateStaticParams() {
  return getAllSlugs().map((slug) => ({ slug }));
}

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const page = getPage(slug);
  if (!page) return {};
  return {
    title: page.title,
    description: page.description || `${page.title} — guide, comparatif et meilleurs prix.`,
  };
}

export default async function SlugPage({ params }: Props) {
  const { slug } = await params;
  const page = getPage(slug);
  if (!page) notFound();

  const related = getPagesByCategory(page.category)
    .filter((p) => p.slug !== slug)
    .slice(0, 8);

  return (
    <main style={{ maxWidth: 720, margin: '0 auto', padding: '2rem 1rem', fontFamily: 'system-ui, sans-serif' }}>
      <nav style={{ marginBottom: '1.5rem', fontSize: '0.9rem' }}>
        <Link href="/">← Accueil</Link>
      </nav>

      <h1 style={{ fontSize: '1.8rem', marginBottom: '0.5rem' }}>{page.title}</h1>

      {page.description && (
        <p style={{ color: '#555', marginBottom: '1.5rem' }}>{page.description}</p>
      )}

      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '2rem' }}>
        <span style={{ background: '#f0f0f0', padding: '0.25rem 0.75rem', borderRadius: 20, fontSize: '0.85rem' }}>
          {page.category}
        </span>
        <span style={{ background: '#f0f0f0', padding: '0.25rem 0.75rem', borderRadius: 20, fontSize: '0.85rem' }}>
          priorité : {page.priority}
        </span>
        {page.haloscan_volume != null && typeof page.haloscan_volume === 'number' && (
          <span style={{ background: '#f0f0f0', padding: '0.25rem 0.75rem', borderRadius: 20, fontSize: '0.85rem' }}>
            {page.haloscan_volume.toLocaleString('fr-FR')} rech./mois
          </span>
        )}
      </div>

      <section style={{ padding: '1.5rem', background: '#fafafa', borderRadius: 8, marginBottom: '2rem' }}>
        <p style={{ color: '#666' }}>
          Contenu à venir — cette page sera enrichie avec des comparatifs produits,
          guides d&apos;achat et liens d&apos;affiliation.
        </p>
      </section>

      {related.length > 0 && (
        <section>
          <h2 style={{ fontSize: '1.2rem', borderBottom: '1px solid #ddd', paddingBottom: '0.3rem' }}>
            Dans la même catégorie
          </h2>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {related.map((r) => (
              <li key={r.slug} style={{ padding: '0.35rem 0' }}>
                <Link href={`/${r.slug}`}>{r.title}</Link>
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}
