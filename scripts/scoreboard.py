"""Draws assets/scoreboard.svg: a red LED stadium scoreboard of real GitHub and
LeetCode numbers. Runs daily in .github/workflows/scoreboard.yml.

Usage: python3 scripts/scoreboard.py            # fetch live numbers, then draw
       python3 scripts/scoreboard.py --offline  # draw from assets/stats.json only

Needs GITHUB_TOKEN in the environment for the GitHub numbers. If a source
can't be reached, the last saved numbers in assets/stats.json are kept, and a
number that was never fetched shows as "--" (nothing is ever made up).
"""
import datetime as dt
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from gen import AMBER as RED, CHALK, led_text, text_cols  # noqa: E402

GH_USER = os.environ.get("GH_USER", "iliass-elguaari")
LC_USER = os.environ.get("LC_USER", "Iliassel")
ROOT = os.path.join(os.path.dirname(__file__), "..")
CACHE = os.path.join(ROOT, "assets", "stats.json")
OUT = os.path.join(ROOT, "assets", "scoreboard.svg")
UA = "profile-scoreboard (GitHub Actions)"


def post_json(url, payload, headers):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={
        "Content-Type": "application/json", "User-Agent": UA, **headers})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


# ------------------------------------------------------------------ GitHub
GH_QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""


def streaks(days):
    """days: list of (date, count) oldest first. Returns (current, longest)."""
    longest = run = 0
    for _, c in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    current = 0
    rev = list(reversed(days))
    if rev and rev[0][1] == 0:  # today not counted yet: start from yesterday
        rev = rev[1:]
    for _, c in rev:
        if c == 0:
            break
        current += 1
    return current, longest


def fetch_github():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN not set")
    data = post_json("https://api.github.com/graphql",
                     {"query": GH_QUERY, "variables": {"login": GH_USER}},
                     {"Authorization": f"bearer {token}"})
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    u = data["data"]["user"]
    cc = u["contributionsCollection"]
    days = [(d["date"], d["contributionCount"])
            for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    cur, best = streaks(days)
    langs = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return {
        # private contributions are hidden from the Action's token; add their count back
        "contributions": cc["contributionCalendar"]["totalContributions"] + cc["restrictedContributionsCount"],
        "streak": cur,
        "best_streak": best,
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        "repos": u["repositories"]["totalCount"],
        "languages": langs,
    }


# ------------------------------------------------------------------ LeetCode
LC_QUERY = """
query($username: String!) {
  matchedUser(username: $username) {
    profile { ranking }
    submitStatsGlobal { acSubmissionNum { difficulty count } }
  }
}"""


def fetch_leetcode():
    data = post_json("https://leetcode.com/graphql",
                     {"query": LC_QUERY, "variables": {"username": LC_USER}},
                     {"Referer": f"https://leetcode.com/u/{LC_USER}/"})
    mu = data["data"]["matchedUser"]
    if not mu:
        raise RuntimeError("LeetCode user not found")
    ac = {x["difficulty"]: x["count"] for x in mu["submitStatsGlobal"]["acSubmissionNum"]}
    return {"solved": ac.get("All"), "easy": ac.get("Easy"), "medium": ac.get("Medium"),
            "hard": ac.get("Hard"),
            # LeetCode reports 5,000,001 for accounts it hasn't ranked yet
            "ranking": mu["profile"]["ranking"] if (mu["profile"]["ranking"] or 0) < 5_000_000 else None}


# ------------------------------------------------------------------ drawing
def fmt(n):
    if n is None:
        return "--"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 10_000:
        return f"{n / 1000:.1f}K"
    return str(n)


SEG_COLORS = [RED, CHALK, "#9AA5A0", "#B3121F", "#5A6470", "#FF8A93"]


def label(text, x, y, size=12, fill="#AEB8B2", anchor="start", weight=600):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="1.8" fill="{fill}">{text}</text>')


def draw(stats, updated):
    W, H = 1200, 500
    gh, lc = stats.get("github", {}), stats.get("leetcode", {})
    defs, body, nums = [], [], []

    def tile(x, y, w, value, lab, i):
        body.append(f'<rect x="{x}" y="{y}" width="{w}" height="96" rx="6" fill="#0A0E15" stroke="#1E2633"/>')
        v = fmt(value)
        nums.append(f'<g class="n" style="animation-delay:{i * 0.12:.2f}s">{led_text(v, x + w / 2, y + 18, 5, RED, dot=4)}</g>')
        body.append(label(lab, x + w / 2, y + 80, anchor="middle"))

    body.append(f'<rect width="{W}" height="{H}" rx="14" fill="#06090F"/>')
    body.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="#2A3445" stroke-width="2"/>')
    body.append(f'<g filter="url(#sg)">{led_text("LIVE STATS", 60, 30, 4, RED, anchor="start", dot=3.3)}</g>')
    body.append(label(f"UPDATED {updated}", W - 60, 50, anchor="end"))
    body.append('<rect x="60" y="72" width="1080" height="1.5" fill="#1E2633"/>')

    body.append(label(f"GITHUB · {GH_USER.upper()} · LAST 12 MONTHS", 60, 103, 13, CHALK, weight=700))
    gtiles = [("contributions", "CONTRIBUTIONS"), ("streak", "CURRENT STREAK"), ("best_streak", "BEST STREAK"),
              ("commits", "COMMITS"), ("prs", "PULL REQUESTS"), ("stars", "STARS")]
    w = (1080 - 5 * 12) / 6
    for i, (k, lab) in enumerate(gtiles):
        tile(60 + i * (w + 12), 116, w, gh.get(k), lab, i)

    body.append(label(f"LEETCODE · {LC_USER.upper()}", 60, 251, 13, CHALK, weight=700))
    ltiles = [("solved", "SOLVED"), ("easy", "EASY"), ("medium", "MEDIUM"), ("hard", "HARD"), ("ranking", "GLOBAL RANK")]
    w = (1080 - 4 * 12) / 5
    for i, (k, lab) in enumerate(ltiles):
        tile(60 + i * (w + 12), 264, w, lc.get(k), lab, i + 6)

    body.append(label("LANGUAGES · SHARE OF CODE IN MY REPOS", 60, 399, 13, CHALK, weight=700))
    langs = sorted((gh.get("languages") or {}).items(), key=lambda kv: -kv[1])
    total = sum(v for _, v in langs) or 1
    top = langs[:5]
    other = total - sum(v for _, v in top)
    if langs and round(100 * other / total) > 0:
        top.append(("OTHER", other))
    x = 60
    defs.append('<clipPath id="bar"><rect x="60" y="410" width="1080" height="22" rx="11"/></clipPath>')
    segs = []
    if not langs:
        segs.append('<rect x="60" y="410" width="1080" height="22" fill="#1E2633"/>')
    for i, (name, v) in enumerate(top):
        sw = 1080 * v / total
        segs.append(f'<rect class="seg" x="{x:.1f}" y="410" width="{sw + 0.5:.1f}" height="22" fill="{SEG_COLORS[i % len(SEG_COLORS)]}"/>')
        x += sw
    body.append(f'<g clip-path="url(#bar)">{"".join(segs)}</g>')
    lx = 60
    for i, (name, v) in enumerate(top):
        lab = f"{name.upper()} {round(100 * v / total)}%"
        body.append(f'<circle cx="{lx + 5}" cy="{460 + 8}" r="5" fill="{SEG_COLORS[i % len(SEG_COLORS)]}"/>')
        body.append(label(lab, lx + 16, 473))
        lx += 16 + len(lab) * 9.6 + 30

    style = ('<style>.n{animation:on 1.4s ease-out}'
             '@keyframes on{0%,100%{opacity:1}15%{opacity:.15}25%{opacity:1}32%{opacity:.3}45%{opacity:1}}'
             '.sw{animation:sw 6s ease-in-out infinite}'
             '@keyframes sw{0%{transform:translateX(-300px)}55%,100%{transform:translateX(1400px)}}</style>')
    defs.append('<filter id="sg" x="-5%" y="-40%" width="110%" height="180%"><feGaussianBlur stdDeviation="1.8" result="b"/>'
                '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    defs.append('<linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                '<stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    defs.append('<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".18"/></pattern>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Season stats scoreboard: GitHub contributions, streak, commits, pull requests, stars, LeetCode problems solved and top languages" '
           f'font-family="\'Segoe UI\',Helvetica,Arial,sans-serif">'
           f'<defs>{"".join(defs)}</defs>{style}{"".join(body)}'
           f'<g filter="url(#sg)">{"".join(nums)}</g>'
           f'<rect class="sw" x="0" y="0" width="260" height="{H}" fill="url(#sweep)"/>'
           f'<rect width="{W}" height="{H}" rx="14" fill="url(#scan)"/></svg>')
    with open(OUT, "w") as f:
        f.write(svg)


def main():
    try:
        with open(CACHE) as f:
            stats = json.load(f)
    except (OSError, ValueError):
        stats = {}
    if "--offline" not in sys.argv:
        for key, fn in (("github", fetch_github), ("leetcode", fetch_leetcode)):
            try:
                stats[key] = fn()
                print(f"{key}: ok")
            except Exception as e:  # keep the last good numbers
                print(f"{key}: kept cached numbers ({e})", file=sys.stderr)
        stats["updated"] = dt.date.today().isoformat()
        with open(CACHE, "w") as f:
            json.dump(stats, f, indent=2, sort_keys=True)
    draw(stats, stats.get("updated", "--"))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
