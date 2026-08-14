# specs/aegis-brand.md — Aegis Brand Generation Spec

## Brand Identity

**Brand:** aegis
**Tagline:** "White hat agents securing your future"
**Tone:** precise, vigilant, trustworthy
**Audience:** engineering teams deploying agents in production

**Narrative:** Red is the threat. White is the solution. The entire visual identity tells the story of threat-to-resolution — crimson danger dissolving into clean, secured white.

### Palette — The Red-to-White Spectrum

| Token | Hex | Role |
|-------|-----|------|
| primary | `#f0f0f5` | White — the solution, purity, secured state |
| secondary | `#6e7fff` | Cool blue — technology bridge between threat and safety |
| accent | `#e63946` | Crimson — threat, alert, active danger |
| background | `#0a0a0f` | Near-black — the threat landscape |
| bg-secondary | `#12121a` | Depth layer |
| surface | `#1a1a2e` | Cards, containers |
| text | `#e8e8ed` | Near-white — clean readability |
| muted | `#5a5a72` | Subdued information |
| border | `#2a2a3e` | Subtle structure |
| overlay | `rgba(10, 10, 15, 0.8)` | Dark overlay |
| error | `#ff2d2d` | Hard red — active threat |
| warning | `#e63946` | Crimson — threats in progress |
| success | `#f0f0f5` | White — secured, resolved, clean |

**Key design decision:** Success is white, not green. The absence of danger IS the security state.

### Typography

- heading: "Inter"
- body: "Inter"
- mono: "JetBrains Mono"
- Scale: standard (h1: 3rem/700, h2: 2rem/600, h3: 1.5rem/600, body: 1rem/400, small: 0.875rem/400, caption: 0.75rem/500)

### Spacing, Breakpoints, Shadows, Motion

- spacing.unit: 0.5rem
- radius: sm 0.375rem, md 0.75rem, lg 1rem
- container-max: 1200px
- breakpoints: sm 640px, md 768px, lg 1024px, xl 1280px
- shadows: dark-adjusted (rgba(0,0,0,0.5) base)
- motion: fast 150ms, normal 300ms, slow 500ms, easing cubic-bezier(0.4, 0, 0.2, 1)

### Identity

```yaml
identity:
  mission: "Proactive agent security — white hat teams that never sleep"
  description: |
    Aegis deploys preemptive and defensive agent teams that continuously
    monitor, detect, and neutralize threats to your agent infrastructure.
    Red means danger. White means secured. We turn your systems white.
  keywords:
    - "agent security"
    - "white hat agents"
    - "threat detection"
    - "defensive AI"
    - "production agent monitoring"
  voice: "precise, confident, zero-fluff — like a security briefing"
  avoid:
    - "hype language"
    - "fear mongering"
    - "vague promises"
```

---

## Products (3)

Three products covering the full surface area. Each tree is a **complete, fully built-out page** — not a section. Each leaf contains all the sections that page needs. 3 variants per page explore different layout approaches.

### Product 1: `app`

The core SaaS platform — where security teams live day-to-day.

**Product-level brand.yaml override:**
```yaml
name: Aegis Platform
tagline: "Your agent security command center"
spacing:
  container-max: "1440px"
```

Wider container for data-dense dashboard layouts.

**Trees (3) — 3 branches each = 9 leaves:**

| Tree | Full Page Includes | Icon |
|------|-------------------|------|
| `dashboard` | Command center overview + real-time threat feed + agent team status panels + defense posture gauge + active incident summary + sparkline trends | shield |
| `operations` | Threat intelligence cards + incident response timeline + attack pattern categories + risk heatmap + containment status + agent action log | activity |
| `agents` | Full agent roster (Scanner, Monitor, Responder, Sentinel) + per-agent detail panels + activity sparklines + deployment controls + uptime metrics + action history | users |

### Product 2: `site`

The marketing/landing page — sells the Aegis platform to engineering teams.

**Product-level brand.yaml override:**
```yaml
name: Aegis
tagline: "White hat agents securing your future"
typography:
  scale:
    h1: { size: "3.5rem", weight: 700, tracking: "-0.03em" }
    h2: { size: "2.25rem", weight: 600, tracking: "-0.02em" }
spacing:
  container-max: "1100px"
```

Bolder typography for marketing impact, tighter container for readability.

**Trees (1) — 3 branches = 3 leaves:**

| Tree | Full Page Includes | Icon |
|------|-------------------|------|
| `landing` | Hero section (red-to-white narrative, bold headline, dual CTAs) + feature showcase (Preemptive Scanning, Hack-Time Defense, Agent Roster, Continuous Monitoring) + pricing tiers (Starter/Pro/Enterprise with red-to-white progression) + social proof (compliance badges, testimonials, stats counters) + final CTA | layout |

### Product 3: `mobile`

Mobile-first layouts — how Aegis looks on phones and tablets.

**Product-level brand.yaml override:**
```yaml
name: Aegis Mobile
tagline: "Agent security in your pocket"
typography:
  scale:
    h1: { size: "2rem", weight: 700, tracking: "-0.02em" }
    h2: { size: "1.5rem", weight: 600, tracking: "-0.01em" }
    body: { size: "0.9375rem", weight: 400, line-height: 1.5 }
spacing:
  unit: "0.375rem"
  radius-sm: "0.5rem"
  radius-md: "0.875rem"
  radius-lg: "1.25rem"
  container-max: "428px"
```

Compact type scale, tighter spacing, mobile container width, larger radii for touch targets.

**Trees (2) — 3 branches each = 6 leaves:**

| Tree | Full Page Includes | Icon |
|------|-------------------|------|
| `dashboard` | Defense posture ring gauge + compact threat feed cards + agent status strip (4 circular indicators) + recent incidents summary + bottom tab navigation (Dashboard/Alerts/Agents/Settings) | smartphone |
| `alerts` | Active alert count badge + alert cards with severity pills and swipe hints + grouped alert sections (Critical/High/Medium) + alert history timeline + resolved vs unresolved states (crimson border vs white border) | bell |

---

## Total Surface Area

| Product | Trees | Branches/Tree | Total Leaves |
|---------|-------|---------------|-------------|
| app | 3 | 3 | 9 |
| site | 1 | 3 | 3 |
| mobile | 2 | 3 | 6 |
| **Total** | **6** | | **18** |

Each leaf is a **complete, multi-section page** — not a fragment.

---

## Generation Prompts — Execution Order

All prompts use `/ui` — the natural language catch-all that routes to the correct workflow(s) automatically.

### Prompt 1: Brand + Products Setup

```
/ui Create a new brand called "aegis" — an agent security platform. White hat agents securing your future. The brand narrative is red-to-white: red is the threat, white is the solution. Use the palette from specs/aegis-brand.md. Then create 3 products inside aegis: "app" (the core SaaS platform, wider 1440px container), "site" (marketing landing pages, bolder typography with 3.5rem h1, 1100px container), and "mobile" (phone-first layouts, compact type scale with 2rem h1, 428px container, larger radii for touch targets). Apply the product-level brand.yaml overrides specified in specs/aegis-brand.md for each.
```

### Prompt 2: App — Dashboard

```
/ui Generate 3 variants of a complete security operations dashboard page for aegis app under the "dashboard" tree. Each leaf is a FULL multi-section scrollable page, not a fragment. Every page must include ALL of: (1) Defense posture gauge — large prominent metric at top showing percentage of systems secured as a red-to-white gradient fill arc or ring. (2) Real-time threat feed — list of recent detections, each with threat name, severity badge (Critical/High/Medium in crimson shades), affected system, and timestamp. (3) Agent team status panel — 4 defensive teams (Scanner, Monitor, Responder, Sentinel) each with active/idle/offline indicator dots, uptime percentage, and threats neutralized today. (4) Active incidents summary — open incident count with sparkline trend, grouped by severity. (5) Quick stats bar — total threats today, mean response time, agents online. Use crimson for threat indicators, white for secured states. Dark surface cards, data-dense but scannable. Variant approaches: v1 grid-based cards with gauge hero, v2 single-column feed with persistent stats header, v3 split-panel threat feed left and agent status right.
```

### Prompt 3: App — Operations

```
/ui Generate 3 variants of a complete security operations and intelligence page for aegis app under the "operations" tree. Each leaf is a FULL multi-section page. Every page must include ALL of: (1) Threat intelligence section — vulnerability cards with CVE-style entries, severity score (0-10), affected systems count, time-since-detection, remediation status. (2) Incident response timeline — showing an incident progressing through Detection (red) > Investigation (amber) > Containment (secondary blue) > Resolution (white), each node showing which agent acted, what it did, and timestamp. (3) Attack pattern categories — common vectors (prompt injection, data exfiltration, privilege escalation, model poisoning) with frequency counts. (4) Risk overview — red-to-white spectrum showing system-by-system risk. (5) Containment status — isolated systems, actively responding agents. Status badges transition red > amber > blue > white. Variant approaches: v1 timeline-centric with intel sidebar, v2 table-heavy with sortable vulnerabilities and timeline below, v3 visual-first large risk overview hero with expandable sections.
```

### Prompt 4: App — Agents

```
/ui Generate 3 variants of a complete agent management page for aegis app under the "agents" tree. Each leaf is a FULL multi-section page. Every page must include ALL of: (1) Agent roster — 4 large cards for Scanner (vulnerability scanning), Monitor (traffic analysis), Responder (threat containment), Sentinel (perimeter watch). Each card: name with icon, status indicator (active=white glow, standby=amber, offline=red), uptime percentage, threats neutralized, last action with timestamp, mini sparkline for last 24h. (2) Deployment controls — toggles to activate/deactivate, config summary. (3) Activity log — chronological feed of recent actions across all agents, filterable by type. (4) Performance metrics — response times, false positive rates, coverage per agent. Active agents glow white, offline agents dimmed. Variant approaches: v1 2x2 card grid with activity log below, v2 full-width list with expandable rows and metrics sidebar, v3 hero spotlight on one agent with tabbed nav to switch.
```

### Prompt 5: Site — Landing Page

```
/ui Generate 3 variants of a complete marketing landing page for aegis site under the "landing" tree. Each leaf is a FULL scrollable page with ALL major sections — not a single section. Every page must include ALL of: (1) HERO — red-to-white narrative front and center. Bold headline about white hat agents protecting production systems. Subheadline on preemptive + defensive teams that never sleep. Primary CTA 'Secure Your Agents' in white on dark. Ghost CTA 'See How It Works'. Background uses crimson subtly — gradient wash or abstract threat pattern fading to dark. (2) FEATURES — four blocks: Preemptive Scanning (find vulnerabilities before attackers), Hack-Time Defense (real-time response during attacks), Agent Roster (Scanner/Monitor/Responder/Sentinel), Continuous Monitoring (24/7 surveillance). Icon + heading + 2-sentence description each. (3) PRICING — 3 tiers: Starter $299/mo (monitoring, alerts, 5 agents), Pro $899/mo (+ defense, incident response, 25 agents — highlighted tier), Enterprise custom (full team, unlimited, Sentinel, SLA). Red-to-white tier progression: Starter=crimson accents, Pro=blue, Enterprise=white. (4) TRUST — compliance badges (SOC2 II, ISO 27001, GDPR) as white icons on dark cards. 2-3 testimonials from engineering leads. Stats: 1.2M+ threats neutralized, 99.99% uptime, 10K+ agents, <200ms response. White for positive, crimson for threats. (5) FINAL CTA — closing section with large 'Get Started' button. Variant approaches: v1 classic centered vertical scroll with generous whitespace, v2 alternating left-right asymmetric sections with bold type, v3 immersive full-viewport sections with dramatic transitions.
```

### Prompt 6: Mobile — Dashboard

```
/ui Generate 3 variants of a complete mobile command center page for aegis mobile under the "dashboard" tree. Phone viewport, 428px max. Each leaf is a FULL mobile page with all sections stacked for thumb-scrolling. Every page must include ALL of: (1) Defense posture ring — prominent circular gauge at top, red-to-white gradient arc fill, large centered percentage number. (2) Threat feed — detection cards each with threat name, severity pill (Critical=crimson, High=accent, Medium=muted), system name, relative timestamp. Swipeable feel with shadows and rounded corners. (3) Agent status strip — 4 circular indicators in a horizontal row for Scanner/Monitor/Responder/Sentinel with colored dots (white=active, amber=standby, red=offline) and labels. Active agents pulse. (4) Recent incidents — compact list of 3-5 incidents with status dots and one-liners. (5) Bottom nav bar — 4 tabs: Dashboard (active), Alerts, Agents, Settings — fixed bottom with icons and labels. Touch-friendly tap targets. Variant approaches: v1 gauge hero top with card stack below, v2 horizontal-scroll feed with status bar and gauge below, v3 minimal with large gauge and compact inline feed.
```

### Prompt 7: Mobile — Alerts

```
/ui Generate 3 variants of a complete mobile alerts page for aegis mobile under the "alerts" tree. Phone viewport, 428px max. Each leaf is a FULL mobile page. Every page must include ALL of: (1) Active alert count header — '7 Active Alerts' with number in crimson if any critical, white if all low. (2) Alert cards — threat name heading, severity pill (Critical/High/Medium), affected system, timestamp, 1-line description. Left border crimson for unresolved, white for resolved. Swipe gesture hints (left=acknowledge, right=escalate). (3) Severity filter — horizontal pill toggles: All/Critical/High/Medium with count badges. (4) Alert history — compact timeline of resolved alerts with resolution agent and time-to-resolve. Resolved entries in white/muted styling contrasting active crimson above. (5) Bottom nav bar consistent with dashboard. Variant approaches: v1 stacked cards with swipe hints and inline filters, v2 grouped by severity in collapsible accordions with count headers, v3 timeline-first with inline alert details and floating filter bar.
```

---

## Generation Summary

| Prompt | Routes To | Product | Trees | Leaves |
|--------|-----------|---------|-------|--------|
| 1 | `/new-brand` + 3x `/new-product` | all | 0 | 0 |
| 2 | `/generate aegis app dashboard 3` | app | 1 | 3 |
| 3 | `/generate aegis app operations 3` | app | 1 | 3 |
| 4 | `/generate aegis app agents 3` | app | 1 | 3 |
| 5 | `/generate aegis site landing 3` | site | 1 | 3 |
| 6 | `/generate aegis mobile dashboard 3` | mobile | 1 | 3 |
| 7 | `/generate aegis mobile alerts 3` | mobile | 1 | 3 |
| **Total** | **7 prompts** | **3** | **6** | **18** |

---

## Video Demo Sequence

1. **Create brand "aegis"** — show the brand.yaml with the red-to-white palette
   - "One config file. 13 colors. Red is the threat. White is the solution."

2. **Generate app/dashboard** — the money shot, live on camera
   - Watch the orchestrator delegate across all 4 teams
   - Browse 3 complete dashboard variants — data-dense, multi-section, crimson threats, white secured states

3. **Show app/agents** — the meta moment
   - "These agent cards — Scanner, Monitor, Responder, Sentinel — were generated by agents."

4. **Switch to site/landing** — full marketing pages, same brand
   - 3 complete landing pages with hero + features + pricing + trust
   - "Same brand.yaml. Dashboards and marketing pages — all on-brand."

5. **Switch to mobile/dashboard** — mobile proof
   - "Same brand, phone viewport. Complete pages, not fragments."

6. **Change a color in the sidebar** — all 18 leaves update instantly
   - "Every page across 3 products, 6 trees, 18 leaves — one brand config."

7. **Close:** "Agents built this. Code validated it. You're browsing the proof."

---

## Post-Generation: Validation Checklist

- [ ] All 18 leaves render without errors
- [ ] Each leaf is a complete multi-section page (not a fragment)
- [ ] Brand tokens used exclusively — grep for hardcoded hex values
- [ ] Red-to-white narrative visible across all products
- [ ] Mobile leaves are viewport-appropriate (428px container)
- [ ] App leaves are data-dense with multiple functional sections
- [ ] Site landing pages include hero + features + pricing + trust
- [ ] VueFlow canvas shows the full 6-tree hierarchy correctly
- [ ] Changing brand primary color cascades to all 18 leaves
