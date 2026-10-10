# KrowN Supply Co. Workspace Directives

## Brand & Catalog Image Integrity Rules

See [.agents/rules/brand_guidelines.md](file:///.agents/rules/brand_guidelines.md) for the complete Brand & Asset Contract.

### Core Commandments
1. **Strict Brand Silos**:
   - **Axiom Allegiance**: Owl mascot only, royal purple & toxic neon green. **ZERO gold crowns**.
   - **KrowN Construction**: Industrial workbench, KC mark, "BUILT TO REIGN". **ZERO gaming desks or owls**.
   - **KrowN Supply Co.**: Luxury studio, 3D gold crown monogram. **ZERO gaming setups, olive arches, or pillarboxes**.

2. **Master Assets Vault**:
   - Master approved assets are vaulted in `public/images/products/masters/`.
   - Never run bulk scripts that overwrite these files without visual inspection.
   - Run `python scripts/verify_catalog_integrity.py` before building or deploying.
