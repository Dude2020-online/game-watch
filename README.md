# Game Watch Dashboard

Static dashboard for tracking official updates and short community verdicts for:
- Outerplane
- Blue Archive
- Starseed
- Eversoul
- Dragon Traveler
- Star Savior

## Files
- `game-watch-dashboard.html` — main static dashboard
- `data/games.json` — content layer for game updates
- `scripts/update_data.py` — starter update script
- `.github/workflows/daily-update.yml` — scheduled GitHub Actions workflow

## Deploy to Cloudflare Pages
1. Create a GitHub repository and upload all files.
2. In Cloudflare, go to Workers & Pages.
3. Create a new Pages project and import the GitHub repo.
4. Use no framework / static HTML.
5. Set the production branch.
6. Deploy the site.

## Daily updates
The workflow is set to run daily on a cron schedule and can also be run manually.
Replace the starter Python script with source fetch/parsing logic for each game.

## Later privacy
When ready, protect the public site with Cloudflare Access or a Pages Functions / Workers auth layer.
