// SPDX-License-Identifier: Apache-2.0
// Copyright (c) 2026 Glovrex

// The figure this rewrites was a hand count carrying the date it was taken. A number a
// reader cannot re-derive is a claim, so the query that produced it lives here and runs
// on a schedule instead.

import fs from 'node:fs';

const TOKEN = process.env.GITHUB_TOKEN;
const README = 'README.md';
const START = '<!-- pr-count:start -->';
const END = '<!-- pr-count:end -->';
const QUERY = 'author:mahirhir type:pr is:merged -user:mahirhir -user:TraceFold -user:Glovrex';

async function search(page) {
  const url = `https://api.github.com/search/issues?q=${encodeURIComponent(QUERY)}&per_page=100&page=${page}`;
  const r = await fetch(url, {
    headers: { Authorization: `Bearer ${TOKEN}`, Accept: 'application/vnd.github+json' },
  });
  if (!r.ok) throw new Error(`search page ${page}: HTTP ${r.status}`);
  return r.json();
}

const repos = new Set();
let merged = 0;
for (let page = 1; page <= 10; page++) {
  const j = await search(page);
  if (!j.items || j.items.length === 0) break;
  merged += j.items.length;
  for (const it of j.items) repos.add(it.repository_url.split('/').slice(-2).join('/'));
  if (j.items.length < 100) break;
}

// A zero here would mean the search failed or the query stopped matching, and writing it
// would replace a true statement with a false one. Refuse rather than publish it.
if (merged === 0 || repos.size === 0) {
  console.error(`refusing to write: merged=${merged} repos=${repos.size}`);
  process.exit(2);
}

const today = new Date().toISOString().slice(0, 10);
const line =
  `> **${merged} pull requests merged into ${repos.size} repositories**, none of them mine, ` +
  `measured ${today} by [\`sync-pr-count\`](.github/workflows/sync-pr-count.yml) ` +
  `&middot; *152 of them merged inside a single month, counted 20 August 2026 when the total ` +
  `was 153. A burst, not a four-year cadence.*`;

const src = fs.readFileSync(README, 'utf8');
const a = src.indexOf(START);
const b = src.indexOf(END);
if (a < 0 || b < 0) {
  console.error('markers absent; nothing rewritten');
  process.exit(2);
}
const next = src.slice(0, a + START.length) + '\n' + line + '\n' + src.slice(b);
if (next === src) {
  console.log(`unchanged merged=${merged} repos=${repos.size}`);
  process.exit(0);
}
fs.writeFileSync(README, next);
console.log(`rewrote merged=${merged} repos=${repos.size}`);
