# Vivre Logo Setup Guide

This guide explains how to add the Vivre logo to all platforms: GitHub, ReadTheDocs, and PyPI.

## Logo Assets

You have two logo assets that should be used in different contexts:

### 1. Full Logo (with "Vivre" text)
**File:** `docs/source/_static/vivre-logo.png`
**Use for:** Main branding, documentation headers, README, PyPI
**Features:**
- Stylized blue globe with grid pattern
- Mounted on light brown stand with grey support
- Stand rests on horizontally oriented books
- Books have red spine and white pages
- "Vivre" text in dark blue serif font (capitalized V)

### 2. Icon Only (globe + books)
**File:** `docs/source/_static/vivre-icon.png`
**Use for:** Favicon, small displays, navigation icons
**Features:**
- Same globe and books design
- No text - just the visual icon
- Optimized for small sizes

## Required Actions

### 1. Create the Logo Images

You need to create two PNG image files and save them as:

```
docs/source/_static/vivre-logo.png    # Full logo with text
docs/source/_static/vivre-icon.png    # Icon only (no text)
```

**Full Logo Specifications:**
- **Format**: PNG with transparency
- **Dimensions**: 300x150 pixels (2:1 aspect ratio)
- **Resolution**: 72 DPI for web use
- **File size**: Under 100KB for fast loading

**Icon Specifications:**
- **Format**: PNG with transparency
- **Dimensions**: 32x32 pixels (square)
- **Resolution**: 72 DPI for web use
- **File size**: Under 20KB for fast loading

### 2. GitHub Repository

The logo is already configured in the README.md file. Once you add the actual image file, it will automatically appear:
- At the top of the repository README
- In the repository header when viewing files
- In GitHub's social media previews

### 3. ReadTheDocs

The logos are configured in `docs/source/conf.py` and will appear:
- **Full logo**: In the documentation header
- **Icon**: As the favicon in browser tabs
- Both in the documentation navigation

### 4. PyPI

The logo is configured in `pyproject.toml` and will appear:
- On the PyPI package page
- In search results
- In package listings

## File Locations

The logos should be placed in these locations:

```
vivre/
├── docs/
│   └── source/
│       └── _static/
│           ├── vivre-logo.png  ← FULL LOGO (with text)
│           └── vivre-icon.png  ← ICON ONLY (favicon)
├── README.md                    ← GitHub display (full logo)
├── docs/source/conf.py         ← ReadTheDocs config (both)
├── docs/source/index.rst       ← Documentation header (full logo)
└── pyproject.toml              ← PyPI config (full logo)
```

## Verification Steps

After adding the logo images:

1. **GitHub**: Check that the full logo appears in the README
2. **ReadTheDocs**: Build and deploy documentation to see both logos
3. **PyPI**: Upload a new package version to see the full logo on PyPI
4. **Browser**: Check that the icon appears as favicon in browser tabs

## Building Documentation Locally

To test the logo locally:

```bash
cd docs
make html
open _build/html/index.html
```

## Notes

- Both logos will automatically scale to fit different display sizes
- All platforms support PNG format with transparency
- The full logo is configured to be 300px wide in the README for optimal display
- The icon is optimized for small sizes (32x32px) and will be used as favicon
- Using separate assets ensures optimal display quality at all sizes
