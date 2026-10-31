# After-action report: Gitee search for the X25 tool sweep, 31 October 2026

Written 31 Oct 2026 at the author's request. Purpose: record why Gitee, China's largest public
code site, could not be added to the X25 tool sweeps, what was tried, what went well, and what to
do differently. Sources: the session log for 31 Oct, `docs/INQUIRIES.md`, `docs/TERMS_OF_USE.md`
and the two private `gitee_probe` results (counts only).

## Goal

Add one Chinese code repository to the X25 sweeps beside GitHub, so tools published mainly in
China are counted (author's decision, 30 Oct 2026: one site from China, two from Russia; the two
Russian sites were later dropped for US sanctions and SourceCraft for needing a Russian account).

## What happened

1. **30-31 Oct, first look.** The `repo_scout` research task read Gitee's terms pages and tried
   one search through Gitee's official API (v5) without an account: the API answered (HTTP 200)
   but returned **0 results** for 渗透测试 ("penetration testing"). Gitee's API documentation says
   searching needs a personal access token, so an account looked like the way forward.
2. **31 Oct, 13:20 ET, sign-up.** The author started an account. Binding a phone number failed:
   the form has no country selector and accepts only 11-digit mainland China mobile numbers. A US
   number written with its leading 1 looked like a Chinese number, so a code would have gone to a
   phone in China; the author stopped before sending a second code. Gitee was recorded as not
   used.
3. **13:32, the account worked anyway.** The author found the account usable without a bound
   phone and was able to create a token. At the author's request, **Gitee's terms were re-read
   before anything ran** (viewing allowed; framing, hot-linking, bulk link requests and star
   manipulation forbidden; nothing on the API, automation or research; the phone described as a
   basis of the service; Chinese law, Beijing courts; no sign of US sanctions in a quick search).
   The author approved a small test.
4. **13:45, test 1.** New research task `gitee_probe`: five searches through the official API,
   three seconds apart, counts only, results saved privately, the token passed to that task
   alone. Token scope: `user_info` only. Result: all five answered (HTTP 200), **0 results each**,
   the same as without a token.
5. **13:53, website check.** The author searched 渗透测试 on the Gitee website while signed in:
   about **200 projects**, with languages, stars and dates. So the content exists and is public;
   only the API returned nothing.
6. **14:00, scope widened.** Agreed retry with the `projects` scope added. The first save ticked
   **All** scopes and set the token to never expire; Claude asked for it to be narrowed to
   `user_info` and `projects` with an expiry (set to 31 Jan 2028) before running.
7. **14:05, test 2.** Same five searches: **0 results each.** Gitee recorded as not used; China
   is covered through the Chinese-language searches already in the GitHub sweep.

## Why it did not work

- **Root cause (most likely): Gitee's public repository search is not served through its open
  API.** The API answered every request normally but returned nothing, with no token, with a
  narrow token and with a wider one, while the website's search (a separate service,
  so.gitee.com) found about 200 projects for the same term. This points to a server-side
  restriction on API search rather than anything in our requests. Gitee has tightened access to
  public content since 2022; whether the API search was switched off on purpose was not
  confirmed (no current documentation found), so this stays a finding, not a fact.
- **Contributing: account rules.** Phone binding accepts mainland China numbers only, so an
  account from outside China may be limited now or later, and the privacy policy treats the phone
  number as part of the service.
- **Not an option: the website search.** Reading so.gitee.com automatically would be scraping a
  website rather than using its API, against the study's standing rule (sites are read only
  through their official routes; nothing is worked around).

## What went well

- The terms were reviewed before any request with the account, at the author's request.
- The tests were small and safe: five searches, three seconds apart, counts only, saved
  privately, the token given to one task alone and never shown in chat or logs.
- The phone problem was caught before a code could reach a stranger's phone.
- The over-wide token (all scopes, no expiry) was caught and narrowed before use.
- The website check by the author separated "no content" from "no API access" in one step.
- Every step was logged the same day, and the fallback (Chinese-language GitHub searches) was
  already in place, so the sweep lost nothing.

## What to do differently

- **Check API access before an account.** For any new site, the first probe should compare an
  API search with the website's own search for the same term; a mismatch means the API is closed
  to us, whatever the account.
- **Ask for the narrowest key from the start,** with an expiry, and check the scope screen with
  the author before saving (token pages often default to everything).
- **Expect country limits** on sign-up for sites in China and Russia, and stop at the first one.

## Follow-ups

- [x] Author: delete the Gitee token on gitee.com (Settings, Personal access tokens) and the
      `GITEE_TOKEN` secret in GitHub (Settings, Secrets and variables, Actions). The author may
      keep or delete the Gitee account itself; the study does not need it.
- [x] `docs/TERMS_OF_USE.md` and `docs/INQUIRIES.md` record Gitee as not used (31 Oct 2026).
- [x] Claude: once the secret is gone, remove the `GITEE_TOKEN` line from the Research workflow;
      keep the `gitee_probe` task (it now runs without a token, anonymously) so the check can be
      repeated if Gitee's API changes. Re-check once, at the 18 Nov refinement, with no token.

**Closed 31 Oct 2026, 18:10 ET.** The author deleted the token on Gitee and the `GITEE_TOKEN`
repository secret in GitHub (a repository secret, so both tests did run with the token); the
workflow line that passed it was removed. The only follow-up left is the anonymous re-check at the
18 Nov refinement.
