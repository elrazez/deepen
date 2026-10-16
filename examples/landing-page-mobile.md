# Example: `make our landing page load faster on mobile`

Unedited output. Claude Code 2.1, model `claude-opus-5-5`, run headless in an empty directory with
only this skill installed and no MCP servers:

```bash
claude -p "/deepen make our landing page load faster on mobile" --setting-sources project --strict-mcp-config
```

---

I couldn't look at the actual landing page: this directory only has the deepen skill file, with no site code, build config or URL. So the answers below name the sources the rewritten prompt should pull rather than specific files.

**1. What a top professional would do that you didn't ask for**
- Measure real mobile visitors first (field data, 75th percentile), not a lab score from a fast laptop, and pick the one metric that's actually failing: LCP, INP or CLS.
- Find the single element that shows up last in the first screen (the LCP element, usually the hero image or headline font) and fix how it gets requested before touching anything else.
- Cap total page weight and set a time limit for mobile, then add a check that fails the build when a change goes over them.

**2. The rawest material to start from**
- Chrome UX Report (CrUX) field data for the landing URL: phone visitors, LCP/INP/CLS at the 75th percentile, from the PageSpeed Insights API or the CrUX History API.
- A Chrome DevTools performance trace and the network waterfall (HAR file) recorded with "Slow 4G" and 4× CPU throttling: request order, blocking CSS/JS, the hero image's size and priority.
- The production build output: bundle sizes from the build stats and a list of third-party scripts, plus the raw HTML the server returns (`curl -s <url>`).

**3. Methods and tools**
- `npx lighthouse <url> --form-factor=mobile --throttling-method=devtools` run 5 times, taking the median, and `npx unlighthouse` if there are several landing variants.
- WebPageTest on a Moto G-class phone over 4G: filmstrip view, LCP breakdown (time to first byte, load delay, load time, render delay).
- Targeted fixes: `fetchpriority="high"` and a preload for the LCP image, AVIF/WebP with `srcset`/`sizes`, critical CSS inlined, fonts set to `font-display: swap` and preloaded, non-essential JS deferred, third-party scripts loaded after the page settles.

**4. Checks that pass or fail on their own**
- CrUX phone data at p75, 28 days after deploy: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 (Google's "good" thresholds).
- Lighthouse CI (`@lhci/cli`) budget assertions in CI: mobile performance score, LCP, and the JS/image byte budgets.
- Real user behaviour: mobile bounce rate and conversion on the landing page in your analytics, before vs. after.

```
Make our landing page load faster on mobile. Don't add features or redesign anything.
1. Baseline: pull CrUX phone data for the landing URL (PageSpeed Insights API) at p75 for LCP, INP and CLS.
   Then run Lighthouse mobile 5 times and take the median, and record one throttled DevTools trace (Slow 4G, 4x CPU).
2. Identify the LCP element and break its time into TTFB, load delay, load time and render delay. Also list the
   render-blocking CSS/JS, the size of each JS bundle and every third-party script, with their bytes.
3. Fix the biggest contributors in order of measured impact: LCP image priority/format/srcset, critical CSS,
   font loading, deferring non-critical JS and third parties. Make one change at a time and re-measure after each.
4. Add Lighthouse CI with budgets: mobile LCP ≤ 2.5 s, CLS ≤ 0.1, and JS/image byte caps set from the new numbers.
5. Report a before/after table (median Lighthouse plus trace numbers) and note what to re-check in CrUX
   28 days after deploy (target: p75 LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1).
```

Want me to run it? Point me at the repo or the page URL first.
