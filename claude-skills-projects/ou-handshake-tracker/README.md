# OU Handshake Career Fair Tracker

A Claude Code skill that turns Oakland University's Handshake Career Fair listings into a live, organized Excel spreadsheet — so a student doesn't have to manually re-check Handshake every week during job/internship search season.

Built by [Fu Wei Hsu (Vivian)](https://www.linkedin.com/in/vivianfuweihsu), MSBA student at Oakland University, out of a personal workflow used to track the Fall 2026 Career Fair.

## What it does

1. Asks for your year, major, and target role keywords (once — saved locally so you're not asked again)
2. Logs into your OU Handshake account (via Playwright MCP) and reads the Career Fair's employer and job listings
3. Star-rates each employer for relevance to your search (`★★★☆☆ - reason`)
4. Writes everything into a formatted Excel tracker, matching by company name so re-running never creates duplicates
5. Optionally sets up a weekly reminder, since employer registrations and job postings change frequently in the weeks before a fair

Built around Handshake, but the same read → rate → write approach can be pointed at other job listing pages too — see the "Not just Handshake" section in `SKILL.md`.

## Prerequisites

- [Claude Code](https://claude.ai/code) with the **Playwright MCP** server enabled
- Your own OU NetID login for Handshake

If you don't have Playwright MCP set up yet, just run the skill anyway — it checks for this first and will walk you through adding it.

## Installation

1. Download or clone this folder
2. Copy `ou-handshake-tracker/` into your Claude Code skills directory (`~/.claude/skills/`)
3. In Claude Code, just mention Handshake, Career Fair, or job tracking — the skill triggers automatically

## File structure

```
ou-handshake-tracker/
├── SKILL.md               # Full workflow instructions Claude follows
├── scripts/
│   └── update_tracker.py  # Writes scraped rows into the Excel tracker, preserving formatting
└── assets/
    └── template.xlsx      # Starter spreadsheet with the fixed column format
```

Your own tracker file and search profile are kept outside this folder, so updating the skill never overwrites your personal data.

## Column format

| Column | Field | Notes |
|---|---|---|
| A | Platform | `Career Fair` or `General Search` |
| B | Employer | Company name |
| C | Industry | |
| D | Job Position | `(not yet posted)` if the employer hasn't listed a role yet |
| E | Job Description | One line |
| F | Job Type | Full-time / Part-time / Internship |
| G | Location | |
| H | OPT/CPT sponsorship | `yes` / `no` / `not stated` |
| I | Relevance Note | Star rating + reason |
| J+ | (open) | Add your own columns — the write script never touches past column I |

## License

MIT — free to use, adapt, or share with other students.
