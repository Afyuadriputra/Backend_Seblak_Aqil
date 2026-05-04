---
name: Seblak Rika Operational Dashboard
colors:
  surface: '#fff8f7'
  surface-dim: '#f0d3d3'
  surface-bright: '#fff8f7'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff0f0'
  surface-container: '#ffe9e8'
  surface-container-high: '#ffe1e1'
  surface-container-highest: '#f9dcdb'
  on-surface: '#271718'
  on-surface-variant: '#5b4040'
  inverse-surface: '#3e2c2c'
  inverse-on-surface: '#ffedec'
  outline: '#8f6f6f'
  outline-variant: '#e3bebd'
  surface-tint: '#ba1434'
  primary: '#9e0027'
  on-primary: '#ffffff'
  primary-container: '#c41e3a'
  on-primary-container: '#ffdada'
  inverse-primary: '#ffb3b4'
  secondary: '#5d5f5f'
  on-secondary: '#ffffff'
  secondary-container: '#dfe0e0'
  on-secondary-container: '#616363'
  tertiary: '#005754'
  on-tertiary: '#ffffff'
  tertiary-container: '#00716e'
  on-tertiary-container: '#9cf2ed'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad9'
  primary-fixed-dim: '#ffb3b4'
  on-primary-fixed: '#40000a'
  on-primary-fixed-variant: '#920023'
  secondary-fixed: '#e2e2e2'
  secondary-fixed-dim: '#c6c6c7'
  on-secondary-fixed: '#1a1c1c'
  on-secondary-fixed-variant: '#454747'
  tertiary-fixed: '#9cf1ed'
  tertiary-fixed-dim: '#80d5d1'
  on-tertiary-fixed: '#00201f'
  on-tertiary-fixed-variant: '#00504d'
  background: '#fff8f7'
  on-background: '#271718'
  surface-variant: '#f9dcdb'
typography:
  h1:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  h2:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  table-header:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  container-margin: 24px
  gutter: 16px
---

## Brand & Style

This design system is built for a high-velocity local food business, balancing the appetizing energy of a spicy food brand with the precision required for inventory and order management. The visual style is **Corporate / Modern** with a focus on high-density information display. 

The goal is to evoke a sense of professional reliability and operational efficiency. The interface stays out of the way, using white space purposefully to group data while maintaining a compact footprint that allows managers to see more information without excessive scrolling. The emotional response is one of control and clarity amidst the heat of a busy kitchen environment.

## Colors

The color palette is led by **Chili Red (#C41E3A)**, used strategically for primary actions and brand presence. To ensure the dashboard remains usable for long periods, the background utilizes a soft **Off-white (#F9F9F9)**. 

Status colors are highly functional: **Leaf Green** for successful payments and fulfilled orders, **Warm Yellow** for pending stock or warnings, and **Dark Red** for critical stock shortages or cancelled orders. Neutral tones are used strictly for borders and secondary text to maintain a clean, organized hierarchy.

## Typography

The design system employs **Inter** as a systematic, utilitarian typeface. The typography scales are intentionally tight to support a dense information architecture. 

- **Primary Body:** 14px is the standard for readability in forms and tables.
- **Labels:** 11px uppercase labels are used for metadata and table headers to create clear distinction from data.
- **Weights:** Use Semi-bold (600) for interactive elements and headings to ensure high contrast against the neutral background.

## Layout & Spacing

This design system uses a **Fluid Grid** model with a fixed left sidebar (240px width). The layout philosophy is centered on "Operational Density"—minimizing padding within components like tables and cards to maximize the data visible "above the fold."

A 12-column grid is used for dashboard widgets, while data-heavy pages utilize a full-width container with 24px side margins. Horizontal rhythm is maintained through a 4px base unit, with 16px being the standard gutter between dashboard cards.

## Elevation & Depth

Visual hierarchy is established using **Tonal Layers** and **Low-contrast outlines** rather than heavy shadows. This keeps the interface feeling fast and digital.

- **Level 0 (Background):** #F9F9F9.
- **Level 1 (Cards/Sidebar):** White (#FFFFFF) with a 1px solid border (#E5E7EB).
- **Level 2 (Modals/Drawers):** White with a soft ambient shadow (0px 4px 12px rgba(0,0,0,0.05)) to indicate focus.
- **Interactive:** Hover states on table rows use a subtle background shift to #F3F4F6 to maintain the user's line of sight during data scanning.

## Shapes

The design system adopts a **Soft** shape language to appear professional yet modern. In accordance with the operational nature of the shop, the radius is kept tight to maintain structural integrity.

- **Standard Cards/Inputs:** 6px radius.
- **Status Badges:** 4px radius or fully rounded (pill) for high-visibility tagging.
- **Buttons:** 6px radius to match the input fields.
- **Modals:** 8px radius for a slightly softer appearance when interrupting the workflow.

## Components

### Buttons & Inputs
Buttons use the Primary Chili Red for main actions. Inputs must have a 1px border (#E5E7EB) and a height of 36px to support a dense UI. Focus states use a 1px solid Primary Red border.

### DataTables
Tables are the heart of this system. They feature a high-density row height (40px-48px). Use a light gray bottom border for rows and a subtle background change on hover. Headers should be sticky for long lists of ingredients or orders.

### Status Badges
Consistent tagging for three pillars:
- **Payment:** Paid (Success), Unpaid (Danger), Partial (Warning).
- **Order:** New (Primary Red), Processing (Warning), Completed (Success).
- **Stock:** In Stock (Success), Low (Warning), Out of Stock (Danger).
Use light background tints with dark text for high readability.

### Drawers & Modals
- **Drawers:** Slide from the right. Used for viewing order details or ingredient breakdowns without losing the context of the main list.
- **Modals:** Centered. Reserved for "Create/Edit" forms and confirmation actions.

### Sidebar & Topbar
The sidebar uses a dark-mode-inspired contrast (Gray-900) or clean white to house navigation. The topbar remains white with a thin bottom border, containing breadcrumbs and the user profile.