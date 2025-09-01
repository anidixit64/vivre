# Vivre Logo Setup Guide

This guide explains how to add the Vivre logo to all platforms: GitHub, ReadTheDocs, and PyPI.

## Logo Description

The Vivre logo features:
- A stylized blue globe with a grid pattern
- Mounted on a light brown stand with grey support
- The stand rests on a horizontally oriented book
- The book has a red spine on the left and white pages with thin grey lines
- To the right, the word "Vivre" in dark blue serif font (capitalized V)

## Required Actions

### 1. Create the Logo Image

You need to create the actual PNG image file based on the description above and save it as:
```
docs/source/_static/vivre-logo.png
```

**Recommended specifications:**
- **Format**: PNG with transparency
- **Dimensions**: 300x150 pixels (2:1 aspect ratio)
- **Resolution**: 72 DPI for web use
- **File size**: Under 100KB for fast loading

### 2. GitHub Repository

The logo is already configured in the README.md file. Once you add the actual image file, it will automatically appear:
- At the top of the repository README
- In the repository header when viewing files
- In GitHub's social media previews

### 3. ReadTheDocs

The logo is configured in `docs/source/conf.py` and will appear:
- In the documentation header
- As the favicon in browser tabs
- In the documentation navigation

### 4. PyPI

The logo is configured in `pyproject.toml` and will appear:
- On the PyPI package page
- In search results
- In package listings

## File Locations

The logo should be placed in these locations:

```
vivre/
├── docs/
│   └── source/
│       └── _static/
│           └── vivre-logo.png  ← MAIN LOGO FILE
├── README.md                    ← GitHub display
├── docs/source/conf.py         ← ReadTheDocs config
├── docs/source/index.rst       ← Documentation header
└── pyproject.toml              ← PyPI config
```

## Verification Steps

After adding the logo image:

1. **GitHub**: Check that the logo appears in the README
2. **ReadTheDocs**: Build and deploy documentation to see the logo
3. **PyPI**: Upload a new package version to see the logo on PyPI

## Building Documentation Locally

To test the logo locally:

```bash
cd docs
make html
open _build/html/index.html
```

## Notes

- The logo will automatically scale to fit different display sizes
- All platforms support PNG format with transparency
- The logo is configured to be 300px wide in the README for optimal display
- The favicon will use the same logo for consistency across platforms
