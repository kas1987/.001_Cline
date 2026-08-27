# Learnings Log — ClinePass Lifecycle

> This document evolves monthly. Each section captures what we learned,
> confirmed, or changed our mind about. Updated as we progress from
> exploration -> understanding -> aptitude.

---

## August 2026 — Month 1: Exploration

### What We Explored
- Full ClinePass setup and configuration (providers, models, auth)
- Token lifecycle (JWT 1hr TTL, auto-refresh via refresh token)
- Billing model (subscription + quota windows + overflow)
- Free tier availability (stealth/ox-alpha, poolside/laguna-s-2.1:free)
- Session data structure and how to parse it
- Context caching mechanics and cost savings

### Key Findings

#### Finding 1: ClinePass is NOT a $10 Cap
- **What we thought:** $9.99/mo = hard spending limit
- **Reality:** $9.99 covers ACCESS + rolling quota windows. Overflow charges are extra but heavily discounted via cache
- **Impact:** Budget can be much lower than feared. Cache saves 88% on token costs
- **Action:** Set budget to $25/mo (2x headroom for growth)

#### Finding 2: Cache Savings Are Massive (88%)
- **Raw token math:** $11.37 for our sessions
- **Actually charged:** $1.36
- **Why:** Context that repeats across messages is cached and charged at a fraction
- **Action:** Longer sessions = more cache = less cost. Don't fear long conversations.

#### Finding 3: Free Models Exist and Work
- **Available:** stealth/ox-alpha (reasoning), poolside/laguna-s-2.1:free (fast)
- **Quality:** Good enough for 80% of tasks (exploration, simple edits, debugging)
- **Cost:** $0, no quota consumed
- **Action:** Default to free, reserve ClinePass for complex work

#### Finding 4: Direct API vs ClinePass
- **Direct DeepSeek API:** Charged at your API key rates, no cache benefits
- **ClinePass DeepSeek:** Same model but with ClinePass negotiated rates + cache
- **Result:** ClinePass deepseek-v4-flash was 69% cheaper than direct API
- **Action:** Always use ClinePass models, never direct API

#### Finding 5: Quota Windows Reset on Schedules
- **5-hour window:** Resets every 5 hours
- **Weekly window:** Resets weekly
- **Monthly window:** Resets monthly
- **Impact:** Batch ClinePass work in bursts, space sessions apart
- **Action:** Schedule complex work within 5-hour windows

### Best Practices Established

1. **Model Selection Hierarchy:**
   - Default: `stealth/ox-alpha` (free, reasoning capable)
   - Fallback: `poolside/laguna-s-2.1:free` (free, fast)
   - Premium: `cline-pass/mimo-v2.5` (complex refactors, multi-file)
   - Never: Direct API calls (bypass ClinePass discounts)

2. **Session Management:**
   - Start with free model, upgrade to ClinePass if needed
   - Batch ClinePass work within 5-hour windows
   - Don't fear long sessions (cache saves money)
   - Space overflow sessions to let quota windows reset

3. **Cost Monitoring:**
   - Run BudgetTracker daily to track burn rate
   - Run BillingAnalysis weekly to understand patterns
   - Log snapshots with Track-ClineUsage.py for trend data
   - Set alerts at 80% of monthly budget

4. **Auth Management:**
   - Refresh token auto-rotates (weeks/months)
   - JWT expires hourly but Cline handles it
   - Only re-auth if refresh token expires (rare)
   - Check auth status with Check-ClineAuth.ps1

### Questions for Next Month
- [ ] How do quota windows actually reset?
- [ ] What happens when ALL quota windows are exhausted?
- [ ] Does session length affect cache hit rate?
- [ ] Are there diminishing returns on context size?
- [ ] How does ClinePass handle model switching mid-session?

---

## Template for Future Months

### September 2026 — Month 2: Understanding
*(Fill in as month progresses)*

#### What We Learned
- 

#### Confirmed (from Month 1)
- 

#### Changed Our Mind About
- 

#### New Best Practices
- 

#### Questions for Next Month
- 

---

### October 2026 — Month 3: Aptitude
*(Fill in as month progresses)*

#### Mastery Milestones
- [ ] Can optimize model selection for any task type
- [ ] Understand quota window timing and batch work
- [ ] Can predict monthly cost within 20% accuracy
- [ ] Have established personal workflow patterns
- [ ] Can teach others ClinePass optimization

---

## Monthly Metrics Tracking

| Month | Sessions | Total Cost | CP Cost | Free % | Daily Avg | Budget Used |
|-------|----------|------------|---------|--------|-----------|-------------|
| Aug 2026 | 21 | $1.36 | $1.04 | 57% | $0.27 | 5.4% of $25 |
| Sep 2026 | | | | | | |
| Oct 2026 | | | | | | |

---

## SWOT Analysis

> Updated monthly. Tracks competitive position with AI tooling.

### August 2026

#### Strengths
- **Cost efficiency:** 88% savings via cache, budget under control
- **Free tier access:** 57% of sessions at $0 cost
- **Model flexibility:** 15+ models available, switch per task
- **Local data ownership:** All session data stored locally
- **Custom tooling:** Budget tracker, auth checker, usage logger
- **Automation potential:** Scripts ready for daily monitoring

#### Weaknesses
- **Learning curve:** Month 1, still discovering features
- **No team usage:** Solo user, no shared workflows yet
- **Manual monitoring:** Scripts exist but not automated
- **Model knowledge gaps:** Don't fully understand quota mechanics
- **Documentation incomplete:** Best practices are draft

#### Opportunities
- **Workflow optimization:** 80/20 free/premium split
- **Multi-device:** Could use Cline on multiple machines
- **Skill building:** AI aptitude improving with each session
- **Cost prediction:** Build forecasting from trend data
- **Community:** Share learnings, contribute to ecosystem
- **Integration:** Connect to GitHub, CI/CD, other tools

#### Threats
- **Price changes:** ClinePass pricing could increase
- **Model deprecation:** Current models may be replaced
- **Usage spikes:** Complex projects could blow budget
- **Platform risk:** Cline service availability dependent
- **Competition:** Other AI coding tools may offer better value
- **Data loss:** Local storage without backups

---

## Decision Log

> Track important decisions and their rationale.

| Date | Decision | Rationale | Outcome |
|------|----------|-----------|---------|
| 2026-08-27 | Set budget to $25/mo | $9.99 sub + overflow + 2x buffer | On track at 5.4% |
| 2026-08-27 | Default to free models | 57% free usage proves viability | TBD |
| 2026-08-27 | Built custom tracking tools | Cline logs could rotate | Working |
| 2026-08-27 | Removed dead cline-pass provider | Was expired, cluttering config | Clean |

---

## User Growth Tracking

### AI Aptitude Self-Assessment

| Skill Area | Month 1 | Month 2 | Month 3 |
|------------|---------|---------|---------|
| Model selection | Learning | | |
| Prompt engineering | Learning | | |
| Workflow optimization | Learning | | |
| Cost management | Learning | | |
| Tool integration | Learning | | |
| Teaching others | Not started | | |

---

*Last updated: 2026-08-27*
*Next review: 2026-09-01*
