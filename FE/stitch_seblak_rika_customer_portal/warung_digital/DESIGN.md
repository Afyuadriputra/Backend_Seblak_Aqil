---
name: Warung Digital
colors:
  surface: '#fcf9f4'
  surface-dim: '#dcdad5'
  surface-bright: '#fcf9f4'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3ee'
  surface-container: '#f0ede8'
  surface-container-high: '#ebe8e3'
  surface-container-highest: '#e5e2dd'
  on-surface: '#1c1c19'
  on-surface-variant: '#5b403d'
  inverse-surface: '#31302d'
  inverse-on-surface: '#f3f0eb'
  outline: '#8f6f6c'
  outline-variant: '#e4beba'
  surface-tint: '#ba1a20'
  primary: '#af101a'
  on-primary: '#ffffff'
  primary-container: '#d32f2f'
  on-primary-container: '#fff2f0'
  inverse-primary: '#ffb3ac'
  secondary: '#106d20'
  on-secondary: '#ffffff'
  secondary-container: '#9df898'
  on-secondary-container: '#1a7425'
  tertiary: '#715300'
  on-tertiary: '#ffffff'
  tertiary-container: '#8f6a00'
  on-tertiary-container: '#fff3e3'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad6'
  primary-fixed-dim: '#ffb3ac'
  on-primary-fixed: '#410003'
  on-primary-fixed-variant: '#930010'
  secondary-fixed: '#9df898'
  secondary-fixed-dim: '#82db7e'
  on-secondary-fixed: '#002204'
  on-secondary-fixed-variant: '#005312'
  tertiary-fixed: '#ffdfa0'
  tertiary-fixed-dim: '#f8bd2a'
  on-tertiary-fixed: '#261a00'
  on-tertiary-fixed-variant: '#5c4300'
  background: '#fcf9f4'
  on-background: '#1c1c19'
  surface-variant: '#e5e2dd'
typography:
  display-price:
    fontFamily: Be Vietnam Pro
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  product-title:
    fontFamily: Be Vietnam Pro
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-main:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-bold:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 20px
  caption:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '500'
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
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  container-margin: 16px
  gutter: 12px
---

## Brand & Style

This design system is built to reflect the heart of local Indonesian street food: warmth, spice, and authenticity. The brand personality is "neighborly and efficient"—it feels like a local stall that has mastered the digital age without losing its soul. 

The visual style leans into **Minimalism with Tactile Accents**. It avoids corporate stiffness by using organic background colors and high-quality, unedited food photography that captures the "steam and spice" of Seblak. The interface is designed to be fast to navigate, ensuring users can go from craving to checkout in under a minute. The emotional response should be one of hunger-inducing warmth and the reliability of a trusted neighborhood cook.

## Colors

The palette is inspired by raw ingredients and traditional food packaging. 
- **Chili Red (Primary):** Stimulates appetite and signals urgency for CTAs and price highlights.
- **Leaf Green (Secondary):** Used for "Available" status, success states, and health-conscious add-ons (like vegetables).
- **Warm Yellow (Accent):** Applied to badges (e.g., "Best Seller") and star ratings to add a cheerful, energetic spark.
- **Off-white/Food Paper (Background):** A soft, non-bleached neutral that reduces eye strain and provides a textured feel compared to pure white.

## Typography

The typography strategy prioritizes immediate recognition of product names and cost. 
- **Be Vietnam Pro** is used for headlines and prices; its contemporary yet friendly terminals feel approachable. 
- **Plus Jakarta Sans** handles the functional body text and labels, providing high legibility even on small mobile screens. 
- Prices should always be the most visually weighted element in a product list, often paired with the Primary Red color.

## Layout & Spacing

This design system utilizes a **Fluid Grid** optimized for mobile-first usage. 
- **Mobile:** A 4-column grid with 16px side margins. Cards typically span 2 columns (side-by-side) or 4 columns (full width).
- **Desktop:** An 8-column centered grid with a max-width of 1024px to keep the food-focused content from feeling sparse.
- **Rhythm:** An 8px base unit drives all padding and margins to ensure a tight, fast-moving layout. Tight spacing (8-12px) is preferred between food photos and their descriptions to maintain a strong visual connection.

## Elevation & Depth

To maintain the "Food Paper" aesthetic, this design system avoids heavy shadows. Instead, it uses **Low-contrast Outlines** and **Tonal Layers**.
- **Cards:** Use a 1px solid border in a slightly darker shade of the background color (#E5E0D8) rather than a shadow.
- **Sticky Elements:** The bottom navigation bar or "Add to Cart" sticky footer uses a soft 8% opacity black shadow with a 10px blur to suggest it is floating above the scrollable content.
- **Active States:** When a button is pressed, it should visually "sink" by removing the subtle border or darkening the background color, providing tactile feedback.

## Shapes

In alignment with the "small card radius" requirement, the shape language is **Soft but disciplined**. 
- **Product Cards:** Fixed at 8px radius to feel modern but structured.
- **Buttons:** Match the 8px radius for consistency.
- **Badges:** Use a pill-shape (fully rounded) to contrast against the rectangular product cards, making status indicators (like "Hot" or "Promo") stand out immediately.
- **Input Fields:** 6px radius to look sharp and easy to tap.

## Components

- **CTA Buttons:** Primary buttons use the Chili Red background with white text. They must be full-width on mobile (minimum height 48px) to ensure accessibility for "on-the-go" ordering.
- **Product Cards:** Images should take up the top 60% of the card area. The bottom 40% contains the product name (bold) and price (Primary Red).
- **Status Badges:** Small, high-contrast pills. "Available" uses Leaf Green; "Out of Stock" uses a neutral grey; "Must Try" uses Warm Yellow.
- **Quantity Selector:** A simple horizontal component with large "+" and "-" targets, using the Secondary Green for the "+" to encourage adding more items.
- **Selection Chips:** Used for spice levels (Level 1, Level 2, etc.). Selected chips turn Primary Red with a thick border; unselected chips remain the background color with a thin border.
- **Food Gallery:** A horizontal swipe component for mobile, allowing users to see different angles of the Seblak toppings.