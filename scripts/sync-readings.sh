#!/bin/bash
# Manual sync script for updating readings page
# Usage: ./sync-readings.sh

echo "To sync your Reader books to the blog:"
echo ""
echo "1. Run this command to see your current books:"
echo "   opencode --mcp-call Reader reader_list_documents --category epub --limit 100"
echo ""
echo "2. Update content/readings.md manually with the reading progress"
echo ""
echo "3. Or ask me (opencode) to update it by saying:"
echo "   'sync my readings from Reader'"
echo ""
echo "Last updated: $(date)"
