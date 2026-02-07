# AGENTS.md

This file provides guidance for AI agents working on this Hugo static site repository.

## Project Overview

This is a Hugo static site using the `hugo-coder` theme. The site is deployed to GitHub Pages via GitHub Actions.

- **Hugo Version**: Extended v0.151.0 (see `.github/workflows/hugo.yaml`)
- **Node Version**: 22.18.0
- **Go Version**: 1.25.1
- **Primary Theme**: hugo-coder (located in `themes/hugo-coder/`)
- **Secondary Theme**: terminal (located in `themes/terminal/`)

## Build Commands

```bash
# Development server (local)
hugo server -D

# Build site
hugo --gc --minify

# Build with base URL
hugo --gc --minify --baseURL "https://example.com/"
```

## Theme-Specific Commands (hugo-coder)

```bash
# Build theme demo
cd themes/hugo-coder && make build

# Run theme demo server
cd themes/hugo-coder && make demo
```

## Testing

This project has minimal test infrastructure:
- Terminal theme has placeholder test: `cd themes/terminal && npm test`
- No actual test suite exists for the main site
- Verify changes by running `hugo server -D` and checking for build errors

## Linting

The terminal theme includes linting configurations:

```bash
# JavaScript linting (in themes/terminal/)
cd themes/terminal && npx eslint .

# SCSS/CSS linting (in themes/terminal/)
cd themes/terminal && npx stylelint "**/*.css" "**/*.scss"
```

## Code Style Guidelines

### Hugo Templates

- Use lowercase for template filenames (e.g., `baseof.html`, `single.html`)
- Use snake_case for partials and shortcodes
- Indent with 2 spaces
- Use `{{ }}` for variables and actions with spaces inside braces
- Quote all string attributes in HTML

### SCSS/CSS

- Use kebab-case for class names (e.g., `.my-class-name`)
- Use 2-space indentation
- Group related properties together
- Use `!default` for SCSS variables to allow overriding
- Import order: normalize, variables, components
- Example structure from `themes/hugo-coder/assets/scss/coder.scss`:
  ```scss
  @import "css/normalize";
  @import "variables";
  @import "base";
  @import "content";
  ```

### JavaScript

- Follow Airbnb style guide (ESLint config in `themes/terminal/.eslintrc.yml`)
- Use double quotes for strings
- Use semicolons
- Use arrow functions with parentheses as needed
- No console.log in production code

### Content (Markdown)

- Use TOML frontmatter format
- Format:
  ```toml
  +++
  draft = false
  date = 2026-02-06T00:00:00+05:30
  title = "Post Title"
  description = ""
  slug = ""
  authors = []
  tags = []
  categories = []
  +++
  ```
- Place content in `content/posts/` or `content/pages/`
- Use descriptive slugs

### Naming Conventions

- **Files/Directories**: kebab-case (e.g., `my-first-post.md`)
- **SCSS Variables**: kebab-case with `$` prefix (e.g., `$bg-color`)
- **CSS Classes**: kebab-case (e.g., `.navigation-subtitle`)
- **Hugo Partials**: snake_case with leading underscore (e.g., `_partials/head.html`)

## Configuration

- Site config: `hugo.toml`
- Key settings:
  - `baseurl`: Production URL
  - `theme`: Active theme name
  - `languagecode`: Default language
  - `markup.highlight.style`: Code highlighting theme

## Customization

- Custom CSS: Add to `assets/css/custom.css`
- Custom SCSS: Uncomment `customSCSS` in `hugo.toml` and add files
- Custom JS: Uncomment `customJS` in `hugo.toml`
- Override layouts: Create files in `layouts/` directory

## Error Handling

- Always check Hugo build output for warnings/errors
- Validate TOML syntax in `hugo.toml` and frontmatter
- Ensure image paths are relative to `static/` directory
- Test responsive design at multiple breakpoints

## Deployment

- Automatic deployment on push to `main` branch
- GitHub Actions workflow: `.github/workflows/hugo.yaml`
- Output directory: `public/` (do not commit)
- Cache directory: `resources/_gen/` (do not commit)

## Git

DO NOT commit:
- `/public/` (build output)
- `/resources/_gen/` (Hugo cache)
- `/.hugo_build.lock`
