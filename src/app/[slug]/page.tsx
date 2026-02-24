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
    <>
      <nav className="breadcrumb">
        <Link href="/">Accueil</Link> &rsaquo; <span>{page.category}</span> &rsaquo;{' '}
        <span>{page.title}</span>
      </nav>

      <article>
        <header className="article-header">
          <h1>{page.title}</h1>
          {page.description && <p style={{ color: 'var(--gray-600)' }}>{page.description}</p>}
          <div className="article-tags" style={{ marginTop: '0.75rem' }}>
            <span className="tag">{page.category}</span>
            <span className="tag">priorite : {page.priority}</span>
            {page.haloscan_volume != null && typeof page.haloscan_volume === 'number' && (
              <span className="tag">{page.haloscan_volume.toLocaleString('fr-FR')} rech./mois</span>
            )}
            {page.haloscan_kd != null && typeof page.haloscan_kd === 'number' && (
              <span className="tag">KD : {page.haloscan_kd}</span>
            )}
          </div>
        </header>

        <div className="article-placeholder">
          <p>
            Contenu a venir &mdash; cette page sera enrichie avec des comparatifs produits, guides
            d&apos;achat et liens d&apos;affiliation.
          </p>
        </div>
      </article>

      {related.length > 0 && (
        <section className="related-section">
          <h2>Dans la meme categorie</h2>
          <ul className="page-list">
            {related.map((r) => (
              <li key={r.slug}>
                <Link href={`/${r.slug}`}>{r.title}</Link>
              </li>
            ))}
          </ul>
        </section>
      )}
    </>
  );
}
