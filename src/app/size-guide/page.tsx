import React from 'react';
import Link from 'next/link';
import './SizeGuide.css';

export const metadata = {
  title: 'Official Size Guide | KrowN Supply Co.',
  description: 'Measurement charts for tees, hoodies, arm sleeves, hats, and athletic shorts across KrowN Supply Co., KrowN Construction, and Axiom Gaming.',
};

export default function SizeGuidePage() {
  return (
    <div className="size-guide-page container">
      <div className="size-guide-header">
        <h1>Official Fit &amp; Size Guide</h1>
        <p>Find your perfect fit across all apparel, compression gear, and accessories.</p>
      </div>

      {/* 1. Axiom Gaming Arm Sleeve */}
      <section className="size-guide-section">
        <h2>⚡ Axiom Pro Gaming Compression Arm Sleeve</h2>
        <p className="size-guide-desc">Measure the circumference of your bicep unbent, and the length from your wrist bone to mid-bicep.</p>
        <div className="size-table-wrapper">
          <table className="size-table">
            <thead>
              <tr>
                <th>Size</th>
                <th>Bicep Circumference</th>
                <th>Wrist Circumference</th>
                <th>Total Length</th>
                <th>Recommended Build</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>S / M</strong></td>
                <td>9.5&quot; – 12.5&quot; (24–32 cm)</td>
                <td>5.5&quot; – 7.0&quot; (14–18 cm)</td>
                <td>16.5&quot; (42 cm)</td>
                <td>Slim to athletic builds, youth, small to medium frames</td>
              </tr>
              <tr>
                <td><strong>L / XL</strong></td>
                <td>12.5&quot; – 16.5&quot; (32–42 cm)</td>
                <td>7.0&quot; – 8.5&quot; (18–22 cm)</td>
                <td>18.0&quot; (46 cm)</td>
                <td>Athletic to muscular builds, broad forearms</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div className="size-tip-box">
          💡 <strong>Pro Tip:</strong> Second-skin compression fit. If you are between sizes and prefer a tighter tournament compression feel, size down. For relaxed daily wear, size up.
        </div>
      </section>

      {/* 2. Comfort Colors 1717 Vintage Tee */}
      <section className="size-guide-section">
        <h2>👑 Comfort Colors 1717 Vintage Garment-Dyed Tee</h2>
        <p className="size-guide-desc">100% ring-spun cotton with authentic vintage boxy drape. Measurements in inches (laid flat).</p>
        <div className="size-table-wrapper">
          <table className="size-table">
            <thead>
              <tr>
                <th>Size</th>
                <th>Chest Width (Pit to Pit)</th>
                <th>Body Length</th>
                <th>Sleeve Length</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>S</strong></td>
                <td>18.25&quot;</td>
                <td>26.6&quot;</td>
                <td>16.2&quot;</td>
              </tr>
              <tr>
                <td><strong>M</strong></td>
                <td>20.25&quot;</td>
                <td>28.0&quot;</td>
                <td>17.7&quot;</td>
              </tr>
              <tr>
                <td><strong>L</strong></td>
                <td>22.0&quot;</td>
                <td>29.4&quot;</td>
                <td>19.0&quot;</td>
              </tr>
              <tr>
                <td><strong>XL</strong></td>
                <td>24.0&quot;</td>
                <td>30.7&quot;</td>
                <td>20.5&quot;</td>
              </tr>
              <tr>
                <td><strong>2XL</strong></td>
                <td>26.0&quot;</td>
                <td>31.6&quot;</td>
                <td>21.7&quot;</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div className="size-tip-box">
          💡 <strong>Pro Tip:</strong> Pre-shrunk vintage garment dye. True to size for a classic relaxed fit. Size up one full size for an oversized 90s streetwear drape.
        </div>
      </section>

      {/* 3. Hoodies & Crewnecks */}
      <section className="size-guide-section">
        <h2>🔥 Heavyweight Hoodies &amp; Crewneck Sweatshirts</h2>
        <p className="size-guide-desc">10 oz heavy fleece with reinforced split-stitch seams and athletic sport-lace closures.</p>
        <div className="size-table-wrapper">
          <table className="size-table">
            <thead>
              <tr>
                <th>Size</th>
                <th>Chest Width</th>
                <th>Body Length</th>
                <th>Sleeve (from center back)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>S</strong></td>
                <td>20.5&quot;</td>
                <td>28.0&quot;</td>
                <td>34.5&quot;</td>
              </tr>
              <tr>
                <td><strong>M</strong></td>
                <td>22.5&quot;</td>
                <td>29.0&quot;</td>
                <td>35.5&quot;</td>
              </tr>
              <tr>
                <td><strong>L</strong></td>
                <td>24.5&quot;</td>
                <td>30.0&quot;</td>
                <td>36.5&quot;</td>
              </tr>
              <tr>
                <td><strong>XL</strong></td>
                <td>26.5&quot;</td>
                <td>31.0&quot;</td>
                <td>37.5&quot;</td>
              </tr>
              <tr>
                <td><strong>2XL</strong></td>
                <td>28.5&quot;</td>
                <td>32.0&quot;</td>
                <td>38.5&quot;</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* 4. Shorts */}
      <section className="size-guide-section">
        <h2>🩳 Athletic Mesh &amp; French Terry Shorts</h2>
        <p className="size-guide-desc">Elastic drawcord waistband with above-the-knee modern styling.</p>
        <div className="size-table-wrapper">
          <table className="size-table">
            <thead>
              <tr>
                <th>Size</th>
                <th>Waist (Relaxed – Stretched)</th>
                <th>Inseam</th>
                <th>Outseam Length</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>S</strong></td>
                <td>28&quot; – 31&quot;</td>
                <td>6.5&quot;</td>
                <td>17.5&quot;</td>
              </tr>
              <tr>
                <td><strong>M</strong></td>
                <td>32&quot; – 34&quot;</td>
                <td>6.5&quot;</td>
                <td>18.0&quot;</td>
              </tr>
              <tr>
                <td><strong>L</strong></td>
                <td>35&quot; – 37&quot;</td>
                <td>7.0&quot;</td>
                <td>18.5&quot;</td>
              </tr>
              <tr>
                <td><strong>XL</strong></td>
                <td>38&quot; – 41&quot;</td>
                <td>7.0&quot;</td>
                <td>19.0&quot;</td>
              </tr>
              <tr>
                <td><strong>2XL</strong></td>
                <td>42&quot; – 45&quot;</td>
                <td>7.5&quot;</td>
                <td>19.5&quot;</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* 5. Headwear */}
      <section className="size-guide-section">
        <h2>🧢 Headwear &amp; Beanies</h2>
        <p className="size-guide-desc">Richardson 112 snapbacks, vintage dad hats, and cuffed beanies.</p>
        <div className="size-table-wrapper">
          <table className="size-table">
            <thead>
              <tr>
                <th>Style</th>
                <th>Sizing Type</th>
                <th>Head Circumference</th>
                <th>Closure / Fit</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Richardson 112 Snapback</strong></td>
                <td>One Size Fits All (OSFA)</td>
                <td>21.5&quot; – 24.5&quot; (7 to 7 3/4)</td>
                <td>7-position adjustable plastic snapback</td>
              </tr>
              <tr>
                <td><strong>KrowN Vintage Dad Hat</strong></td>
                <td>One Size Fits All (OSFA)</td>
                <td>21.0&quot; – 24.0&quot; (6 7/8 to 7 5/8)</td>
                <td>Self-fabric tuck-in strap with antique brass buckle</td>
              </tr>
              <tr>
                <td><strong>Jobsite Cuffed Beanie</strong></td>
                <td>One Size Fits All (OSFA)</td>
                <td>20.5&quot; – 25.0&quot;</td>
                <td>100% High-stretch ribbed knit with 3&quot; foldover cuff</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <div style={{ textAlign: 'center', marginTop: '2rem' }}>
        <Link href="/collections/all" className="btn-primary">
          Return to Shopping →
        </Link>
      </div>
    </div>
  );
}
