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
                src="/images/products/krown-r112-flagship-leather-patch-snapback.jpg" 
                alt="Richardson 112 Saddle Leather Patch Snapback" 
                className={styles.headwearImg}
              />
              <span className={styles.headwearTag}>KrowN Supply Co. Snapback</span>
            </div>
            <div className={styles.headwearCard}>
              <img 
                src="/images/products/krown-r112-flagship-leather-patch-hero.jpg" 
                alt="Richardson 112 Leather Patch Angle" 
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
            <div className={styles.gamingVideoWrap}>
              <video 
                src="/media/axiom-intro.mp4" 
                controls 
                poster="/images/branding/gaming/axiom-owl-display.png"
                className={styles.gamingVideo}
                preload="metadata"
              >
                Your browser does not support the video tag.
              </video>
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

            <Link href="/products/axiom-sweatpants-pro" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axiom-sweatpants-pro-model-clean.jpg" 
                  alt="Axiom Allegiance Pro Heavyweight Joggers" 
                />
                <span className={styles.gearPill}>450 GSM FLEECE</span>
              </div>
              <div className={styles.gamingGearBody}>
                <h4>Axiom Pro Heavyweight Joggers</h4>
                <p>Dual Purple/Green Cords • S to 3XL • $68.00</p>
              </div>
            </Link>

            <Link href="/products/krown-mat-01" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axiom-owl-desk-mat-photorealistic.jpg" 
                  alt="Axiom Owl Extended Gaming Desk Mat" 
                />
                <span className={styles.gearPill}>5 CUSTOM SIZES</span>
              </div>
              <div className={styles.gamingGearBody}>
                <h4>Axiom Extended Gaming Desk Mat</h4>
                <p>Micro-Weave Precision Cloth • From $19.99</p>
              </div>
            </Link>

            <Link href="/products/axiom-wrist-rest-01" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axiom-keyboard-wrist-rest-tournament-edition.jpg" 
                  alt="Axiom Pro Cooling Gel Keyboard Wrist Rest" 
                />
                <span className={styles.gearPill}>COOLING GEL</span>
              </div>
              <div className={styles.gamingGearBody}>
                <h4>Pro Cooling Gel Keyboard Wrist Rest</h4>
                <p>Ergonomic Slope • 60%, TKL &amp; Full • $19.99</p>
              </div>
            </Link>

            <Link href="/products/axiom-mug-01" className={styles.gamingGearCard}>
              <div className={styles.gamingGearThumb}>
                <img 
                  src="/images/products/axiom-mug-clean-photoreal-15oz.jpg" 
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
