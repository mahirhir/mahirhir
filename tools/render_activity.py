"""GitHub API から毎回引き直して、活動の帯を焼く。

静止画は要らない、というのが Owner の裁定。API に沿って**決定論的に変わる**物にする。
- 入力は毎回 live: `search/issues?q=author:<user> type:pr is:merged`
- 描くのは「他人の repo に入った merge」の 53 週分の帯。数字は画像に焼かず、
  同じ data を入れれば同じ絵が出る(乱数は固定 seed の LCG)。
- 出力は PNG 1 枚。release asset へ上げるので README の URL は変わらない。

依存は Pillow のみ(ubuntu-latest に pip で入る)。ブラウザは使わない。
"""
import datetime as dt
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

USER = os.environ.get("GX_USER", "mahirhir")
OUT = os.environ.get("GX_OUT", "activity.png")
W, H = 1280, 330
INK = (11, 10, 9)
PAPER = (236, 231, 218)

_s = [20260818]


def rnd():
    _s[0] = (_s[0] * 1664525 + 1013904223) % 4294967296
    return _s[0] / 4294967296


def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print(f"gh api failed: {path}\n{r.stderr[:300]}", file=sys.stderr)
        return {}
    return json.loads(r.stdout)


def fetch():
    items, page = [], 1
    while page <= 10:
        d = gh(f"search/issues?q=author:{USER}+type:pr+is:merged&per_page=100&page={page}")
        got = d.get("items") or []
        items += got
        if len(got) < 100:
            break
        page += 1
    mine = (f"{USER}/", "Glovrex/", "TraceFold/")
    out = []
    for i in items:
        repo = i["repository_url"].replace("https://api.github.com/repos/", "")
        if repo.startswith(mine):
            continue
        when = i.get("closed_at") or i["created_at"]
        out.append({"repo": repo, "at": when})
    return out


def font(sz, mono=False):
    names = (["DejaVuSansMono.ttf", "LiberationMono-Regular.ttf"] if mono
             else ["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf", "Georgia.ttf"])
    for n in names:
        for base in ("/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/truetype/liberation/",
                     "C:/Windows/Fonts/", ""):
            try:
                return ImageFont.truetype(base + n, sz)
            except Exception:
                continue
    return ImageFont.load_default()


def main():
    rows = fetch()
    if not rows:
        print("no data; not overwriting", file=sys.stderr)
        return 1

    today = dt.date.today()
    weeks = 53
    start = today - dt.timedelta(days=today.weekday() + 7 * (weeks - 1))
    buckets = [0] * weeks
    for r in rows:
        d = dt.datetime.strptime(r["at"][:10], "%Y-%m-%d").date()
        idx = (d - start).days // 7
        if 0 <= idx < weeks:
            buckets[idx] += 1

    img = Image.new("RGB", (W, H), INK)
    dr = ImageDraw.Draw(img)
    # 地。わずかに温度を持たせる(中性グレーは「選んでいない」に読める)
    for y in range(H):
        t = y / H
        dr.line([(0, y), (W, y)], fill=(int(11 + 7 * t), int(10 + 6 * t), int(9 + 6 * t)))

    X0, Y0, CW, CH, GAP = 74, 96, 18, 46, 5
    mx = max(buckets) or 1
    for i, n in enumerate(buckets):
        cx = X0 + i * (CW + GAP)
        if cx + CW > W - 60:
            break
        t = 0.0 if n == 0 else 0.24 + 0.76 * (n / mx) ** 0.6
        a = int(255 * (0.05 + t * 0.92))
        dr.rectangle([cx, Y0, cx + CW, Y0 + CH],
                     fill=(int(PAPER[0] * a / 255), int(PAPER[1] * a / 255), int(PAPER[2] * a / 255)))
        e = int(255 * (0.16 + t * 0.40))
        dr.rectangle([cx, Y0, cx + CW, Y0 + CH],
                     outline=(int(PAPER[0] * e / 255), int(PAPER[1] * e / 255), int(PAPER[2] * e / 255)))

    fs, fm, fsm = font(30), font(11, True), font(15)
    dr.text((74, 40), "m a h i r h i r", font=fs, fill=PAPER)
    dr.text((74, Y0 + CH + 22),
            "each column is one week; brighter means more of my pull requests were merged that week",
            font=fsm, fill=(163, 155, 142))
    lit = sum(1 for b in buckets if b)
    dr.text((74, Y0 + CH + 44),
            f"the shape is the caveat: {lit} of {weeks} weeks carry all of it, so read it as a burst",
            font=fsm, fill=(163, 155, 142))
    repos = len({r["repo"] for r in rows})
    owners = len({r["repo"].split("/")[0] for r in rows})
    dr.text((74, Y0 + CH + 74),
            f"{len(rows)} MERGED INTO REPOSITORIES I DO NOT OWN  |  {repos} REPOSITORIES  |  {owners} OWNERS",
            font=fm, fill=(125, 117, 104))
    dr.text((74, Y0 + CH + 94),
            f"REDRAWN FROM THE GITHUB API ON {today.isoformat()}  |  53 WEEKS TO {today.isoformat()}",
            font=fm, fill=(125, 117, 104))

    # 粒子(固定 seed=同じ data なら同じ絵)
    px = img.load()
    for _ in range(24000):
        x, y = int(rnd() * W), int(rnd() * H)
        n = int((rnd() - 0.5) * 20)
        r0, g0, b0 = px[x, y]
        px[x, y] = (max(0, min(255, r0 + n)), max(0, min(255, g0 + n)), max(0, min(255, b0 + n)))

    img.save(OUT)
    print(f"{OUT} {os.path.getsize(OUT):,}B  merges={len(rows)} weeks_nonzero={sum(1 for b in buckets if b)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
