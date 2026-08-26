# Work other people merged

Everything the profile used to say about merged pull requests, with the method to re-derive
each figure. It lives here so the profile can be six chips instead of a table.

## The numbers

Re-measured 26 August 2026 from the GitHub search API without credentials, which is also
where you can count them. The figures the profile carried before this page existed were
measured on 20 August 2026 and are kept in the last column so the drift is visible.

| | measured 26 Aug 2026 | how to re-derive it | was, 20 Aug |
|:--|--:|:--|--:|
| Pull requests merged | **154** | [search: author, merged](https://github.com/search?q=author%3Amahirhir+type%3Apr+is%3Amerged&type=pullrequests) | 153 |
| Into repositories I do not own | **154 of 154** | add `user:mahirhir` to that same search and the count is 0 | 153 of 153 |
| Distinct repositories | **144** | tally `repository_url` over the 154 merged results | 143 |
| Opened in total | **353** | drop `is:merged` from the search. The other 199 are visible too | 351 |

152 of them merged inside a single month, counted 20 August 2026 when the total was 153.
It is a burst, not a four-year cadence. That month-level breakdown has not been re-run
since; the figure is carried forward with its date rather than restated as current.

## The projects the profile names

Star counts read from the repository API on 26 August 2026.

| project | merged | stars |
|:--|--:|--:|
| [ant-design](https://github.com/ant-design/ant-design) | 1 | 99,200 |
| [material-ui](https://github.com/mui/material-ui) | 1 | 98,928 |
| [gin](https://github.com/gin-gonic/gin) | 1 | 89,119 |
| [vite](https://github.com/vitejs/vite) | 1 | 82,542 |
| [nest](https://github.com/nestjs/nest) | 1 | 76,458 |
| [strapi](https://github.com/strapi/strapi) | 1 | 73,015 |
| [scrapy](https://github.com/scrapy/scrapy) | 1 | 64,041 |
| [pdf.js](https://github.com/mozilla/pdf.js) | 1 | 53,780 |

The full distribution, tallied over all 154 merged results on 26 August 2026:
one repository at three merged pull requests (`janhq/jan`), eight at two, and 135 at one.
**There is no repository I am a deep contributor to.** The shape of this record is breadth,
not depth, and the eight projects named above are chosen by how well known they are, not by
how much of my work is in them &mdash; each of the eight is a single merged pull request.

## The picture

![Each square is one merged pull request, lighting in the order they landed](https://github.com/mahirhir/mahirhir/releases/download/brand-assets/activity.gif)

Not an illustration. A workflow refetches every merge from the GitHub API each Monday and
draws it again, so it is whatever this account has actually done by the time you look.
Generator: [`tools/render_activity.py`](https://github.com/mahirhir/mahirhir/blob/main/tools/render_activity.py).

## The Tracefold demo that used to sit on the profile

![Verify a receipt, flip one byte, verify again](https://github.com/TraceFold/tracefold/releases/download/demo-assets/tracefold-demo-10s.gif)

A receipt, a signed checkpoint and a public key. The receipt verifies offline and exits
`0`. One byte of it is flipped, `cmp -l` prints the single line proving one byte moved, and
the same command exits `7`. Real terminal, fresh anonymous clone, 26 August 2026; the build
that precedes it is deliberately outside the recording. The same recording is on the
[repository README](https://github.com/TraceFold/tracefold#readme).
