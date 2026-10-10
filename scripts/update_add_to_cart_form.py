import os

filepath = os.path.join("src", "components", "product", "AddToCartForm.tsx")

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add isWorkShirt and state
old_vars = """  const isJersey = product.id.startsWith('axiom-jersey');
  const isSweatshirt = product.id === 'axiom-sweatshirt-01';
  const isPersonalizable = isJersey || isSweatshirt;

  const [sweatshirtSleeveOption, setSweatshirtSleeveOption] = useState<'left' | 'right' | 'both'>('left');"""

new_vars = """  const isJersey = product.id.startsWith('axiom-jersey');
  const isSweatshirt = product.id === 'axiom-sweatshirt-01';
  const isWorkShirt = product.id === 'krown-work-01';
  const isPersonalizable = isJersey || isSweatshirt || isWorkShirt;

  const [sweatshirtSleeveOption, setSweatshirtSleeveOption] = useState<'left' | 'right' | 'both'>('left');
  const [workShirtBadgePlacement, setWorkShirtBadgePlacement] = useState<'left' | 'right'>('left');

  React.useEffect(() => {
    if (typeof window !== 'undefined' && currentVariant?.image) {
      window.dispatchEvent(new CustomEvent('krown:variant-changed', {
        detail: { color: selectedColor, size: selectedSize, image: currentVariant.image }
      }));
    }
  }, []);"""

content = content.replace(old_vars, new_vars)

# 2. Add isWorkShirt summary to handleAddToCart
old_add_cart_block = """    } else if (isSweatshirt) {
      if (sweatshirtSleeveOption === 'left') addOnsSummary.push('Gothic Sleeve Print: Left Sleeve (Standard)');
      if (sweatshirtSleeveOption === 'right') addOnsSummary.push('Gothic Sleeve Print: Right Sleeve');
      if (sweatshirtSleeveOption === 'both') addOnsSummary.push('Gothic Sleeve Print: Both Sleeves (+$4.99)');
    }"""

new_add_cart_block = """    } else if (isSweatshirt) {
      if (sweatshirtSleeveOption === 'left') addOnsSummary.push('Gothic Sleeve Print: Left Sleeve (Standard)');
      if (sweatshirtSleeveOption === 'right') addOnsSummary.push('Gothic Sleeve Print: Right Sleeve');
      if (sweatshirtSleeveOption === 'both') addOnsSummary.push('Gothic Sleeve Print: Both Sleeves (+$4.99)');
    } else if (isWorkShirt) {
      addOnsSummary.push(workShirtBadgePlacement === 'left' ? 'Badge: Left Chest (Standard)' : 'Badge: Right Chest');
    }"""

content = content.replace(old_add_cart_block, new_add_cart_block)

# 3. Update onChange handlers for color and size selects
old_color_change = """            onChange={(e) => {
              const newColor = e.target.value;
              setSelectedColor(newColor);
              const newSizes = product.variants.filter(v => v.color === newColor).map(v => v.size);
              const nextSize = newSizes.length > 0 ? newSizes[0] : selectedSize;
              if (newSizes.length > 0) setSelectedSize(newSizes[0]);
              if (typeof window !== 'undefined') {
                window.dispatchEvent(new CustomEvent('krown:color-changed', { detail: { color: newColor } }));
                window.dispatchEvent(new CustomEvent('krown:variant-changed', { detail: { color: newColor, size: nextSize } }));
              }
            }}"""

new_color_change = """            onChange={(e) => {
              const newColor = e.target.value;
              setSelectedColor(newColor);
              const newSizes = product.variants.filter(v => v.color === newColor).map(v => v.size);
              const nextSize = newSizes.length > 0 ? (newSizes.includes(selectedSize) ? selectedSize : newSizes[0]) : selectedSize;
              if (newSizes.length > 0 && !newSizes.includes(selectedSize)) setSelectedSize(newSizes[0]);
              const matchingVariant = product.variants.find(v => v.color === newColor && v.size === nextSize) || product.variants.find(v => v.color === newColor);
              if (typeof window !== 'undefined') {
                window.dispatchEvent(new CustomEvent('krown:color-changed', { detail: { color: newColor, image: matchingVariant?.image } }));
                window.dispatchEvent(new CustomEvent('krown:variant-changed', { detail: { color: newColor, size: nextSize, image: matchingVariant?.image } }));
              }
            }}"""

content = content.replace(old_color_change, new_color_change)

old_size_change = """            onChange={(e) => {
              const newSize = e.target.value;
              setSelectedSize(newSize);
              if (typeof window !== 'undefined') {
                window.dispatchEvent(new CustomEvent('krown:variant-changed', { detail: { color: selectedColor, size: newSize } }));
              }
            }}"""

new_size_change = """            onChange={(e) => {
              const newSize = e.target.value;
              setSelectedSize(newSize);
              const matchingVariant = product.variants.find(v => v.color === selectedColor && v.size === newSize);
              if (typeof window !== 'undefined') {
                window.dispatchEvent(new CustomEvent('krown:variant-changed', { detail: { color: selectedColor, size: newSize, image: matchingVariant?.image } }));
              }
            }}"""

content = content.replace(old_size_change, new_size_change)

# 4. Add UI for work shirt badge placement right before Quantity
work_shirt_ui = """      {/* Work Shirt Chest Badge Placement Option */}
      {isWorkShirt && (
        <div className="form-group" style={{ marginBottom: '1.25rem', background: 'rgba(212, 175, 55, 0.05)', padding: '0.85rem', borderRadius: '6px', border: '1px solid rgba(212, 175, 55, 0.2)' }}>
          <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--accent-gold)', display: 'block', marginBottom: '0.45rem' }}>
            KrowN Construction Chest Badge Placement:
          </label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
            <button
              type="button"
              onClick={() => setWorkShirtBadgePlacement('left')}
              style={{
                padding: '0.5rem',
                fontSize: '0.78rem',
                fontWeight: workShirtBadgePlacement === 'left' ? 700 : 400,
                background: workShirtBadgePlacement === 'left' ? 'rgba(212, 175, 55, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                border: workShirtBadgePlacement === 'left' ? '1px solid var(--accent-gold)' : '1px solid rgba(255, 255, 255, 0.1)',
                color: workShirtBadgePlacement === 'left' ? 'var(--accent-gold)' : 'var(--text-muted)',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Left Chest (Standard)
            </button>
            <button
              type="button"
              onClick={() => setWorkShirtBadgePlacement('right')}
              style={{
                padding: '0.5rem',
                fontSize: '0.78rem',
                fontWeight: workShirtBadgePlacement === 'right' ? 700 : 400,
                background: workShirtBadgePlacement === 'right' ? 'rgba(212, 175, 55, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                border: workShirtBadgePlacement === 'right' ? '1px solid var(--accent-gold)' : '1px solid rgba(255, 255, 255, 0.1)',
                color: workShirtBadgePlacement === 'right' ? 'var(--accent-gold)' : 'var(--text-muted)',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Right Chest
            </button>
          </div>
          <p style={{ margin: '0.4rem 0 0 0', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
            Includes bold &ldquo;BUILT TO REIGN&rdquo; back statement piece &amp; &ldquo;KrowN Construction&rdquo; sleeve lettering.
          </p>
        </div>
      )}

      <div className="form-group">
        <label htmlFor="quantity">Quantity</label>"""

content = content.replace('      <div className="form-group">\n        <label htmlFor="quantity">Quantity</label>', work_shirt_ui)

# 5. Dynamic contextual Size Guide Modal
old_size_guide_content = """            <div className="size-guide-content" style={{ marginTop: '1rem', color: 'var(--foreground)' }}>
              <p className="text-muted" style={{ marginBottom: '1rem', fontSize: '0.85rem' }}>All measurements are in inches. Tolerance +/- 0.5&quot;.</p>
              
              <h3 style={{ marginTop: '1rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Pro Esports Jersey</h3>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', marginBottom: '1rem', fontSize: '0.9rem' }}>
                <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Chest</th><th style={{ padding: '0.5rem' }}>Length</th></tr></thead>
                <tbody>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>19.5&quot;</td><td style={{ padding: '0.5rem' }}>27.5&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>20.5&quot;</td><td style={{ padding: '0.5rem' }}>28.5&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>21.5&quot;</td><td style={{ padding: '0.5rem' }}>29.5&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>22.5&quot;</td><td style={{ padding: '0.5rem' }}>30.5&quot;</td></tr>
                  <tr><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>23.5&quot;</td><td style={{ padding: '0.5rem' }}>31.5&quot;</td></tr>
                </tbody>
              </table>

              <h3 style={{ marginTop: '1.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Heavyweight Hoodies & Tees</h3>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
                <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Chest</th><th style={{ padding: '0.5rem' }}>Length</th></tr></thead>
                <tbody>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>22.0&quot;</td><td style={{ padding: '0.5rem' }}>28.0&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>23.0&quot;</td><td style={{ padding: '0.5rem' }}>29.0&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>24.0&quot;</td><td style={{ padding: '0.5rem' }}>30.0&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>25.0&quot;</td><td style={{ padding: '0.5rem' }}>31.0&quot;</td></tr>
                  <tr><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>26.0&quot;</td><td style={{ padding: '0.5rem' }}>32.0&quot;</td></tr>
                </tbody>
              </table>
            </div>"""

new_size_guide_content = """            <div className="size-guide-content" style={{ marginTop: '1rem', color: 'var(--foreground)' }}>
              <p className="text-muted" style={{ marginBottom: '1rem', fontSize: '0.85rem' }}>
                Official specifications for {product.name}.
              </p>

              {/* Headwear Guide */}
              {(product.id.includes('hat') || product.id.includes('beanie') || product.id.includes('snapback') || product.id.includes('112')) && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Headwear Specifications</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Style</th><th style={{ padding: '0.5rem' }}>Profile</th><th style={{ padding: '0.5rem' }}>Circumference</th><th style={{ padding: '0.5rem' }}>Closure</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>Richardson 112 Snapback</td><td style={{ padding: '0.5rem' }}>Mid-Pro Structured</td><td style={{ padding: '0.5rem' }}>7&quot; – 7 3/4&quot; (21.5&quot;–24.5&quot;)</td><td style={{ padding: '0.5rem' }}>7-Hole Snapback</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>Washed Chino Dad Hat</td><td style={{ padding: '0.5rem' }}>Low-Pro Unstructured</td><td style={{ padding: '0.5rem' }}>6 7/8&quot; – 7 5/8&quot;</td><td style={{ padding: '0.5rem' }}>Brass Slide Buckle</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>Tradesman Ribbed Beanie</td><td style={{ padding: '0.5rem' }}>Heavy Cuffed Knit</td><td style={{ padding: '0.5rem' }}>Stretch-Fit (One Size)</td><td style={{ padding: '0.5rem' }}>Cuffed Acrylic</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Drinkware Guide */}
              {(product.id.includes('shaker') || product.id.includes('mug') || product.id.includes('tumbler')) && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Drinkware &amp; Capacity Specifications</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Vessel</th><th style={{ padding: '0.5rem' }}>Capacity</th><th style={{ padding: '0.5rem' }}>Height x Base</th><th style={{ padding: '0.5rem' }}>Features</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>Standard Tritan Shaker</td><td style={{ padding: '0.5rem' }}>24 oz / 700 ml</td><td style={{ padding: '0.5rem' }}>8.8&quot; x 3.1&quot;</td><td style={{ padding: '0.5rem' }}>Shatterproof • Whisk Ball</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>Pro Insulated Steel Shaker</td><td style={{ padding: '0.5rem' }}>26 oz / 750 ml</td><td style={{ padding: '0.5rem' }}>9.2&quot; x 3.2&quot;</td><td style={{ padding: '0.5rem' }}>Double-Wall Vacuum • Lock Lid</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>Ceramic Gamer Mug</td><td style={{ padding: '0.5rem' }}>15 oz / 445 ml</td><td style={{ padding: '0.5rem' }}>4.7&quot; x 3.3&quot;</td><td style={{ padding: '0.5rem' }}>Two-Tone Glaze • Microwave Safe</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Work Shirt Guide */}
              {isWorkShirt && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>KrowN Construction Work Shirt Measurements</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Chest</th><th style={{ padding: '0.5rem' }}>Body Length</th><th style={{ padding: '0.5rem' }}>Sleeve Length</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>38&quot; – 40&quot;</td><td style={{ padding: '0.5rem' }}>30.0&quot;</td><td style={{ padding: '0.5rem' }}>33.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>42&quot; – 44&quot;</td><td style={{ padding: '0.5rem' }}>31.0&quot;</td><td style={{ padding: '0.5rem' }}>34.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>46&quot; – 48&quot;</td><td style={{ padding: '0.5rem' }}>32.0&quot;</td><td style={{ padding: '0.5rem' }}>35.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>50&quot; – 52&quot;</td><td style={{ padding: '0.5rem' }}>33.0&quot;</td><td style={{ padding: '0.5rem' }}>36.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>54&quot; – 56&quot;</td><td style={{ padding: '0.5rem' }}>34.0&quot;</td><td style={{ padding: '0.5rem' }}>37.5&quot;</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>3XL</td><td style={{ padding: '0.5rem' }}>58&quot; – 60&quot;</td><td style={{ padding: '0.5rem' }}>35.0&quot;</td><td style={{ padding: '0.5rem' }}>38.5&quot;</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Jersey Guide */}
              {isJersey && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Pro Esports Cut-and-Sew Jersey</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Chest Width</th><th style={{ padding: '0.5rem' }}>Body Length</th><th style={{ padding: '0.5rem' }}>Sleeve (Raglan)</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>19.5&quot;</td><td style={{ padding: '0.5rem' }}>27.5&quot;</td><td style={{ padding: '0.5rem' }}>14.0&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>20.5&quot;</td><td style={{ padding: '0.5rem' }}>28.5&quot;</td><td style={{ padding: '0.5rem' }}>14.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>21.5&quot;</td><td style={{ padding: '0.5rem' }}>29.5&quot;</td><td style={{ padding: '0.5rem' }}>15.0&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>22.5&quot;</td><td style={{ padding: '0.5rem' }}>30.5&quot;</td><td style={{ padding: '0.5rem' }}>15.5&quot;</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>23.5&quot;</td><td style={{ padding: '0.5rem' }}>31.5&quot;</td><td style={{ padding: '0.5rem' }}>16.0&quot;</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Compression Arm Sleeve */}
              {product.id.includes('sleeve') && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Pro Compression Sleeve Sizing</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Bicep Girth</th><th style={{ padding: '0.5rem' }}>Wrist Girth</th><th style={{ padding: '0.5rem' }}>Total Length</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S/M</td><td style={{ padding: '0.5rem' }}>10.0&quot; – 12.5&quot;</td><td style={{ padding: '0.5rem' }}>6.0&quot; – 7.5&quot;</td><td style={{ padding: '0.5rem' }}>16.5&quot;</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>L/XL</td><td style={{ padding: '0.5rem' }}>12.5&quot; – 15.5&quot;</td><td style={{ padding: '0.5rem' }}>7.5&quot; – 9.0&quot;</td><td style={{ padding: '0.5rem' }}>17.5&quot;</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Bottoms: Shorts & Joggers */}
              {(product.id.includes('short') || product.id.includes('jogger') || product.id.includes('sweatpant')) && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Bottoms (Shorts &amp; Joggers) Sizing</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Waist (Inches)</th><th style={{ padding: '0.5rem' }}>Inseam (Joggers)</th><th style={{ padding: '0.5rem' }}>Inseam (Shorts)</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>28&quot; – 30&quot;</td><td style={{ padding: '0.5rem' }}>30.0&quot;</td><td style={{ padding: '0.5rem' }}>6.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>31&quot; – 33&quot;</td><td style={{ padding: '0.5rem' }}>30.5&quot;</td><td style={{ padding: '0.5rem' }}>6.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>34&quot; – 36&quot;</td><td style={{ padding: '0.5rem' }}>31.0&quot;</td><td style={{ padding: '0.5rem' }}>7.0&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>37&quot; – 40&quot;</td><td style={{ padding: '0.5rem' }}>31.5&quot;</td><td style={{ padding: '0.5rem' }}>7.0&quot;</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>41&quot; – 44&quot;</td><td style={{ padding: '0.5rem' }}>32.0&quot;</td><td style={{ padding: '0.5rem' }}>7.5&quot;</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Hoodies & Tops Fallback */}
              {!isWorkShirt && !isJersey && !product.id.includes('hat') && !product.id.includes('beanie') && !product.id.includes('shaker') && !product.id.includes('mug') && !product.id.includes('sleeve') && !product.id.includes('short') && !product.id.includes('jogger') && !product.id.includes('sweatpant') && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Heavyweight Hoodies &amp; Streetwear Tops</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Chest</th><th style={{ padding: '0.5rem' }}>Length</th><th style={{ padding: '0.5rem' }}>Sleeve</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>22.0&quot;</td><td style={{ padding: '0.5rem' }}>28.0&quot;</td><td style={{ padding: '0.5rem' }}>34.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>23.0&quot;</td><td style={{ padding: '0.5rem' }}>29.0&quot;</td><td style={{ padding: '0.5rem' }}>35.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>24.0&quot;</td><td style={{ padding: '0.5rem' }}>30.0&quot;</td><td style={{ padding: '0.5rem' }}>36.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>25.0&quot;</td><td style={{ padding: '0.5rem' }}>31.0&quot;</td><td style={{ padding: '0.5rem' }}>37.5&quot;</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>26.0&quot;</td><td style={{ padding: '0.5rem' }}>32.0&quot;</td><td style={{ padding: '0.5rem' }}>38.5&quot;</td></tr>
                    </tbody>
                  </table>
                </div>
              )}
            </div>"""

content = content.replace(old_size_guide_content, new_size_guide_content)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated AddToCartForm.tsx successfully!")
