import type { Metadata } from 'next';

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
      <body>{children}</body>
    </html>
  );
}
