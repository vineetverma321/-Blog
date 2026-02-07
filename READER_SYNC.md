# Reader Sync Setup

This document explains how to set up automatic syncing of your Reader books to the Hugo blog.

## How It Works

A GitHub Actions workflow runs daily at midnight UTC to:
1. Fetch your books from Reader via API
2. Check reading progress for each book
3. Update `content/readings.md` automatically
4. Commit and push changes to your repository

## Setup Instructions

### 1. Get Your Reader API Token

1. Log in to [Readwise Reader](https://read.readwise.io/)
2. Go to [Settings > Account](https://readwise.io/account)
3. Scroll down to "Readwise API" section
4. Click "Get API Token" or copy your existing token

### 2. Add Token to GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Name: `READER_API_TOKEN`
5. Value: Paste your API token
6. Click **Add secret**

### 3. Enable GitHub Actions

The workflow is already in `.github/workflows/sync-readings.yml`. It will:
- Run automatically every day at midnight UTC
- Can be triggered manually from the Actions tab

### 4. Manual Sync

You can also sync manually:

**Option A: Via GitHub Actions**
1. Go to **Actions** tab in your repository
2. Click **Sync Reader Books** workflow
3. Click **Run workflow**

**Option B: Local sync (requires Python)**
```bash
export READER_API_TOKEN="your-token-here"
python scripts/sync-reader-api.py
```

**Option C: Ask me**
Just say: "Sync my readings from Reader" and I'll update the page for you!

## Book Categories

Books are automatically categorized based on reading progress:

- **Currently Reading**: Progress between 1% and 99%
- **Future Reads**: Progress is 0% (haven't started)
- **Already Read**: Progress is 100%

## Troubleshooting

**Workflow fails with "READER_API_TOKEN not set"**
- Make sure you added the secret correctly in GitHub

**Books not appearing**
- Check that your books are in EPUB or PDF format in Reader
- The API only returns books, not articles

**Sync not running**
- Check the Actions tab for any errors
- Make sure Actions are enabled in your repository settings
