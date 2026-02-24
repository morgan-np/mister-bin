import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: {
    default: 'Mister Bin — Guide poubelles, tri & compost',
    template: '%s | Mister Bin',
  },
  description:
    'Trouvez la poubelle idéale : cuisine, tri sélectif, compost, cache-poubelle, design. Comparatifs, guides et avis.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body>
        <header className="site-header">
          <div className="site-header-inner">
            <Link href="/" className="site-logo">
              Mister Bin
            </Link>
            <nav className="site-nav">
              <Link href="/">Accueil</Link>
              <Link href="/#categories">Categories</Link>
            </nav>
          </div>
        </header>

        <main className="site-main">{children}</main>

        <footer className="site-footer">
          <div className="site-footer-inner">
            <span>&copy; {new Date().getFullYear()} Mister Bin</span>
            <span>Guide poubelles, tri selectif & compost</span>
          </div>
        </footer>
      </body>
    </html>
  );
}
