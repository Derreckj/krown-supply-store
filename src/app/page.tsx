import React from "react";
import Link from "next/link";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      {/* HERO SECTION */}
      <section className={styles.hero}>
        <div className={styles.heroContent}>
          {/* Social Proof Pill */}
          <div className={styles.heroRatingPill}>
            <span className={styles.ratingStars}>★★★★★</span>
            <span className={styles.ratingText}><strong>4.9 AVERAGE</strong> • 120+ TRADESMEN & GAMERS</span>
          </div>

          <div className={styles.heroLogoWrap}>
            <img 
              src="/images/branding/krown-definitive-logo.png" 
              alt="KrowN Supply Co. Definitive Brand" 
              className={styles.heroEmblem}
              style={{ borderRadius: '16px', objectFit: 'contain' }} 
            />
          </div>

          <h1 className={styles.heroTitle}>
            WEAR THE <span className={styles.titleHighlight}>KROWN.</span>
          </h1>
          <p className={styles.heroSubtitle}>STREETWEAR &times; WORKWEAR &times; ESPORTS</p>

          <div className={styles.heroCtas}>
            <Link href="/collections/all" className="btn-primary">
              Shop Flagship Drop
            </Link>
            <Link href="/custom-crew" className={styles.btnCustomCrew}>
              Custom Crew Hats ★
            </Link>
          </div>

          {/* Floating New Drop Spotlight Card */}
          <div className={styles.heroFloatingDrop}>
            <Link href="/products/krown-supply-co-480gsm-heavyweight-streetwear-hoodie" className={styles.dropCardInner}>
              <div className={styles.dropThumbWrap}>
                <img 
                  src="/images/products/krown-supply-premium-hoodie-front.jpg" 
                  alt="KrowN 480 GSM Heavyweight Streetwear Hoodie" 
                  className={styles.dropThumb}
                />
              </div>
              <div className={styles.dropInfo}>
                <span className={styles.dropTag}>NEW DROP • 480 GSM FRENCH TERRY</span>
                <span className={styles.dropPrice}>Heavyweight Hoodie $68.00 <span>&rarr;</span></span>
              </div>
            </Link>
          </div>
        </div>
      </section>

      {/* HEADWEAR SPOTLIGHT */}
      <section className={`${styles.headwearSection} container`}>
        <div className={styles.headwearBanner}>
          <div className={styles.headwearText}>
            <div className={styles.headwearBadge}>★ FLAGSHIP HEADWEAR</div>
            <h2 className={styles.headwearTitle}>Authentic Richardson 112 Leather Patch Snapback</h2>
            <p className={styles.headwearDesc}>
              Engineered with genuine laser-etched saddle tan leatherette patches on authentic Richardson 112 truckers.
              Cut on the classic structured mid-profile silhouette featuring breathable nylon mesh, pre-curved visor with contrast double-stitching, and adjustable snapback closure.
            </p>
            <div className={styles.headwearActions}>
              <Link href="/products/custom-krown-works-hat" className="btn-primary">
                Shop Richardson 112 Snapback ($29.99)
              </Link>
            </div>
          </div>
          <div className={styles.headwearImageGrid}>
            <div className={styles.headwearCard}>
              <img 
                src="/images/products/krown-r112-flagship-leather-patch-hero.jpg" 
                alt="KrowN Supply Co. Richardson 112 Leather Patch Trucker Snapback" 
                className={styles.headwearImg}
              />
              <span className={styles.headwearTag}>KrowN Supply Co. Snapback</span>
            </div>
            <div className={styles.headwearCard}>
              <img 
                src="/images/products/krown-r112-flagship-leather-patch-snapback.jpg" 
                alt="Richardson 112 Saddle Leather Patch Snapback Front" 
                className={styles.headwearImg}
              />
              <span className={styles.headwearTag}>Structured 112 Profile</span>
            </div>
          </div>
        </div>
      </section>



      {/* AXIOM ALLEGIANCE GAMING SHOWCASE */}
      <section className={styles.gamingSection}>
        <div className={`container ${styles.gamingGrid}`}>
          <div className={styles.gamingTextContent}>
            <div className={styles.gamingBadge}>
              <span>⚡</span> The Official Esports Division
            </div>
            <h2 className={styles.gamingTitle}>AXA — AXIOM ALLEGIANCE</h2>
            <h3 className={styles.gamingSubtitle}>PLAY TO REIGN. Powered by KrowN.</h3>
            <p className={styles.gamingDesc}>
              Before the jobsites, KrowN started in the arena. Axiom Allegiance (AXA) represents
              the competitive esports organization, featuring our signature razor-sharp 
              <strong> AXA Owl</strong> mascot with intentional A-X-A letterforms embedded in the eyes and beak.
            </p>
            <blockquote className={styles.gamingQuote}>
              &ldquo;YOU CANNOT BE TRULY HUMBLE, UNLESS YOU TRULY BELIEVE THAT LIFE CAN AND WILL GO ON WITHOUT YOU.&rdquo;
            </blockquote>
            <div className={styles.gamingCtas}>
              <Link href="/collections/gaming" className={styles.btnGaming}>
                Shop AXA Pro Jerseys →
              </Link>
            </div>
          </div>

          <div className={styles.gamingMediaCard}>
            <div className={styles.gamingVideoWrap} style={{ position: 'relative', overflow: 'hidden', borderRadius: '12px', background: '#000' }}>
              <img 
                src="/images/branding/gaming/axiom-owl-display.png" 
                alt="Axiom Allegiance Esports Anthem" 
                style={{ width: '100%', height: 'auto', display: 'block' }}
              />
              <div style={{ padding: '0.75rem', background: 'rgba(15, 15, 20, 0.95)', borderTop: '1px solid rgba(138, 43, 226, 0.3)' }}>
                <audio 
                  controls 
                  src="/media/axiom-intro.mp3" 
                  style={{ width: '100%', height: '36px' }}
                  preload="metadata"
                >
                  Your browser does not support the audio element.
                </audio>
              </div>
            </div>
            <div className={styles.gamingMediaMeta}>
              <div className={styles.gamingMetaTrack}>
                <div className={styles.gamingMetaIcon}>♫</div>
                <div className={styles.gamingMetaText}>
                  <h4>Official Axiom Intro</h4>
                  <p>Original DJ Track &amp; Intro Animation</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Pro Esports High-Voltage Gear Showcase */}
        <div className={`container ${styles.gamingGearWrap}`}>
          <div className={styles.gamingGearHeader}>
            <h3>Axiom Allegiance Pro League Loadout</h3>
            <p>Tournament-grade cut-and-sew apparel, custom gamertags &amp; high-voltage accessories.</p>
          </div>
          <div className={styles.gamingGearGrid}>
            <Link href="/products/axiom-jersey-home" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axa-pro-jersey-home.jpg" 
                  alt="AXA Pro League Home Jersey" 
                />
                <span className={styles.gearPill}>HOME EDITION</span>
              </div>
              <div className={styles.gamingGearBody}>
                <h4>AXA Pro League Home Jersey</h4>
                <p>Personalized Name &amp; Number • $54.99</p>
              </div>
            </Link>

            <Link href="/products/axiom-hoodie-01" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axiom-heavyweight-hoodie-studio-v8.jpg" 
                  alt="Axiom Allegiance Legacy Owl Hoodie — Statement Edition" 
                />
                <span className={styles.gearPill}>13.5 OZ FLEECE</span>
              </div>
              <div className={styles.gamingGearBody}>
                <h4>Axiom Legacy Owl Hoodie</h4>
                <p>3-Location DTG Statement Piece • $89.99</p>
              </div>
            </Link>

            <Link href="/products/axiom-shaker-01" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axiom-shaker-signature-tritan-clean.jpg" 
                  alt="Axiom Allegiance Pro Loadout Shaker Bottle" 
                />
                <span className={styles.gearPill}>STEEL &amp; TRITAN</span>
              </div>
              <div className={styles.gamingGearBody}>
                <h4>Pro Loadout Shaker (24–26oz)</h4>
                <p>Lime, Stealth &amp; Pro Double-Wall Steel • From $24.99</p>
              </div>
            </Link>

            <Link href="/products/axiom-sweatshirt-01" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axiom-crewneck-sweatshirt-studio.jpg" 
                  alt="Axiom Allegiance Legacy Owl Crewneck — Statement Edition" 
                />
                <span className={styles.gearPill}>3-LOCATION DTG</span>
              </div>
              <div className={styles.gamingGearBody}>
                <h4>Axiom Legacy Owl Crewneck</h4>
                <p>Arched Chest, Hero Motto &amp; Sleeve • $54.99</p>
              </div>
            </Link>

            <Link href="/products/krown-mat-01" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axiom-owl-banner-v10-official.png" 
                  alt="Axiom Owl Extended Gaming Desk Mat" 
                />
                <span className={styles.gearPill}>5 CUSTOM SIZES</span>
              </div>
              <div className={styles.gamingGearBody}>
                <h4>Axiom Owl Display Gaming Desk Mat</h4>
                <p>Micro-Weave Precision Cloth • From $19.99</p>
              </div>
            </Link>

            <Link href="/products/axiom-r112-patch-01" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axiom-r112-leather-patch-charcoal.jpg" 
                  alt="Axiom Richardson 112 Genuine Leather Patch Snapback" 
                />
                <span className={styles.gearPill}>LEATHER PATCH</span>
              </div>
              <div className={styles.gamingGearBody}>
                <h4>Axiom Richardson 112 Snapback</h4>
                <p>Genuine Leather Hex Patch • $34.99</p>
              </div>
            </Link>

            <Link href="/products/axiom-mug-01" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axiom-mug-single-owl-official.jpg" 
                  alt="Axiom Owl Two-Tone Ceramic Gaming Mug" 
                />
                <span className={styles.gearPill}>15 OZ CERAMIC</span>
              </div>
              <div className={styles.gamingGearBody}>
                <h4>Axiom Two-Tone Ceramic Gamer Mug</h4>
                <p>Midnight Obsidian &amp; Lime Glaze • $19.99</p>
              </div>
            </Link>
          </div>
        </div>
      </section>

      {/* BRAND STORY WITH REAL CRAFTSMANSHIP PHOTO */}
      <section className={styles.storySection}>
        <div className={`container ${styles.storyGrid}`}>
          <div className={styles.storyImageContainer}>
            <img 
              src="/images/branding/construction/KC deck.jpg" 
              alt="Authentic KrowN Craftsmanship" 
              className={styles.storyImg} 
            />
            <span className={styles.storyImageCaption}>Crafted on jobsites. Built to reign.</span>
          </div>
          <div className={styles.storyContent}>
            <span className={styles.storyBadge}>The Heritage</span>
            <h2>The KrowN Story</h2>
            <p>
              The KrowN identity started in gaming before it ever became a company.
              It evolved onto the jobsite with KrowN Construction LLC, earning respect through
              relentless standards and precision building.
            </p>
            <p>
              Now, <strong>KrowN Supply Co.</strong> expands that DNA into a dedicated lifestyle brand.
              Whether you are on a high-stakes jobsite, competing in the lobby, or commanding the street:
            </p>
            <p className={styles.storyQuote}>
              &ldquo;Workwear meets gaming. Built on jobsites. Now you can wear it.&rdquo;
            </p>
            <Link href="/collections/all" className="btn-primary" style={{ marginTop: '1rem' }}>
              Explore The Gear
            </Link>
          </div>
        </div>
      </section>
      
      {/* EMAIL SIGNUP */}
      <section className={`${styles.section} container`}>
        <div className={styles.newsletterCard}>
          <h2>Join the Reign</h2>
          <p>Get new-drop announcements, limited releases and KrowN updates.</p>
          <form className={styles.newsletterForm} action="#">
            <input type="email" placeholder="Enter your email" required aria-label="Email address" />
            <button type="submit" className="btn-primary">Subscribe</button>
          </form>
        </div>
      </section>
    </div>
  );
}
