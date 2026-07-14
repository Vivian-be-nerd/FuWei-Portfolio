---
name: ou-handshake-tracker
description: Scrapes Oakland University's Handshake Career Fair employer and job listings into a formatted Excel tracker, filtered by the student's year, major, and target role type. Use this skill whenever a user wants to track Career Fair employers, organize Handshake job listings into a spreadsheet, or asks for help keeping an up-to-date list of companies attending an OU Career Fair. Make sure to use this skill any time the user mentions Handshake, Career Fair, OU job tracking, or wants a weekly-refreshed spreadsheet of career fair employers, even if they don't explicitly ask for a "tracker" or "skill" by name.
---

# OU Handshake Career Fair Tracker

Turns Oakland University's Handshake Career Fair listings into an organized, always-up-to-date Excel spreadsheet, so a student does not have to manually re-check Handshake every week.

## Who this is for

Any Oakland University student searching for a job or internship who wants a running spreadsheet of Career Fair employers instead of manually browsing Handshake. Works for any major or year — the filtering step below adapts to the student.

## Not just Handshake

This skill's example is built around OU's Handshake, but the underlying method (log in with Playwright MCP → read listings → write into the same Excel format) works on any job listing page, not just Handshake. If a student wants to track a different site — a specific company's careers page, LinkedIn Jobs, a different job board — tell Claude the URL and ask it to track that instead. Claude should adapt Step 2's scraping instructions to that site's actual structure (the exact steps in Step 2 are Handshake-specific; the columns in Step 4 and the write script stay the same for any source). Mention this to the student the first time you run this skill, so they know Handshake isn't a hard limit — just say something like: "This is built around Handshake by default, but if there's another site you check regularly, I can point the same tracker at that instead."

## Step 0: Check prerequisites before doing anything else

This skill needs the **Playwright MCP** server (it's what logs into Handshake and reads the listings) and an **OU NetID login** for Handshake.

1. Check whether a Playwright MCP tool (e.g. `browser_navigate`) is available in your current toolset.
2. **If it's missing, don't just refuse.** Tell the student plainly what's missing and offer to walk them through adding it (for Claude Code: `claude mcp add playwright` or enabling it in settings, depending on their setup). Only stop and wait for them to confirm it's installed before moving on — don't attempt to scrape Handshake with WebFetch or Firecrawl, since Handshake requires a logged-in session those tools can't hold.
3. Confirm `assets/template.xlsx` is present in this skill's folder (do not delete it — the write script copies its formatting from here).

## Step 1: Greet the student and get their search profile

**First run:** Greet the student and explain what this skill does in one or two sentences — e.g. "This helps you track who's coming to OU's Fall Career Fair (Sep 29, 2026) by pulling live data from Handshake into a spreadsheet." Share the reference page so they know where the source data comes from: `https://oakland.joinhandshake.com/stu/career_fairs/[FAIR_ID]/employers_list`.

Then ask:
1. What year are you (freshman / sophomore / junior / senior / grad)?
2. What is your major?
3. What kind of role are you looking for? (e.g. "marketing analytics", "software engineering", "supply chain") — this can be more than one keyword.
4. Besides the Career Fair, is there another Handshake page you'd like scanned regularly (e.g. general job search results for a specific keyword)? Let them know this is available, but don't push it — Career Fair tracking is the default.

Save the answers to a small local file (e.g. `my-profile.md`, next to the student's own tracker copy, **not** inside this skill's shared folder) so future runs don't need to repeat this interview. On later runs, just confirm: "Same search profile as last time (year/major/keywords), or do you want to update it?"

Use these answers to prioritize and flag relevant listings in Step 3. Do not skip this — a generic unfiltered dump of every Career Fair employer is not useful to the student.

## Step 2: Scrape Handshake via Playwright MCP

**Finding the right Career Fair first**: Every fair has its own ID number in the URL (e.g. `.../career_fairs/64690/...`), and it's different every semester — do not assume it's the same one used before. Ask the student which fair they mean (e.g. "Fall Career Fair 2026"), then have them find it themselves: **Handshake → Events → find that fair in the list → click into it → copy the URL from the browser address bar and paste it here.** Confirm the fair name and date with the student before scraping, so you don't accidentally pull the wrong semester's data.

1. Navigate to the student's OU Handshake Career Fair Employers tab (URL pattern: `https://oakland.joinhandshake.com/stu/career_fairs/[FAIR_ID]/employers_list?page=1&per_page=25`, using the fair ID found above).
2. For each employer, visit `https://oakland.joinhandshake.com/e/[EMPLOYER_ID]/jobs` to see their posted roles (if any — many employers register without posting a specific job).
3. Also check the Career Fair's Jobs tab directly (`.../career_fairs/[FAIR_ID]/jobs`) for postings not tied to a specific employer page.
4. Record for each employer/job: company name, industry, job position (or "not yet posted" if the employer registered without a listing), a one-line job description, job type (Full-time/Part-time/Internship), location, and whether the listing mentions OPT/CPT/visa sponsorship (`yes` / `no` / `not stated` — only mark `no` if the posting explicitly excludes sponsorship, do not guess).

## Step 3: Flag relevance based on Step 1's answers

For each row, rate how well it matches the student's stated major/role interest using a 1-5 star score, written as filled/empty stars followed by a short reason — e.g. `★★★☆☆ - Large retailer, likely has marketing analytics roles`. Put the stars first so the student can scan the column visually before reading the reason. Do not filter rows out entirely — keep the full list, just star-rate them, since students should still see the full picture of who is attending.

Rough guide for the rating:
- ★★★★★ / ★★★★☆ — directly matches their stated role keywords or major
- ★★★☆☆ — plausible fit, industry commonly has this kind of role, but not confirmed
- ★★☆☆☆ / ★☆☆☆☆ — unlikely fit, but still worth listing since it's an active employer at the fair

## Step 4: Write to Excel

Use `scripts/update_tracker.py` to write the results into a copy of `assets/template.xlsx`. Read the script's docstring before running it — it expects a list of row dictionaries and writes them by matching company name (never by row number, since the student may re-sort the sheet later). Always read the existing header row first to confirm column order before writing; do not assume it matches this document if the student has customized their copy.

**Do not modify `assets/template.xlsx` itself.** Always have the student work from their own copy (e.g. `MyCareerFairTracker.xlsx`) so re-running this skill never overwrites their personal notes.

## Column format (fixed columns, customization allowed after column I)

| Col | Name | Notes |
|---|---|---|
| A | Platform | `Career Fair` or `General Search` |
| B | Employer | Company name as shown on Handshake |
| C | Industry | |
| D | Job Position | `(not yet posted)` if employer hasn't listed a role |
| E | Job Description | One line |
| F | Job Type | `Full-time` / `Part-time` / `Internship` |
| G | Location | |
| H | OPT/CPT sponsorship | `yes` / `no` / `not stated` |
| I | Relevance Note | Star rating + reason from Step 3 (e.g. `★★★★☆ - Matches major`), based on the student's own year/major/role |
| J+ | (open) | Student can add their own columns (e.g. personal networking contacts, follow-up notes) — this skill never writes past column I |

## Re-running weekly

Handshake employer registrations and job postings change frequently in the weeks before a Career Fair, so this works best re-run weekly. After the first successful run, ask the student: **"Want me to set up a weekly reminder so you don't have to remember this yourself?"**

- If they say yes and you have calendar or email tools connected, offer to set up a recurring weekly reminder (calendar event and/or email) pointing back to this skill.
- If no scheduling tools are connected, or the student prefers something lighter, suggest they add a recurring reminder in whatever calendar app they already use.
- Don't set this up silently without asking — some students may not want a recurring email, and Claude should never assume the answer is yes.

## Formatting note

`assets/template.xlsx` ships with a clean, readable default format (header row bold, column A centered). If the student wants different formatting, they should edit their own copy — `scripts/update_tracker.py` always preserves whatever formatting is already in the row above where it writes, so a student's manual formatting choices are never overwritten.
