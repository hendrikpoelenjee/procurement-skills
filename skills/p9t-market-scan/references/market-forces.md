<!-- SPDX-License-Identifier: Apache-2.0 -->

# Market Forces

Structured prompts for analysing supply market dynamics across five dimensions.

Use when building the market structure section of a scan. Map what is known, label what is inferred, and flag what is unverifiable.

---

## 1. Supplier power

Questions:
- How many credible suppliers operate in this market?
- Is the market concentrated (few large players) or fragmented (many small ones)?
- Do suppliers have pricing power — can they raise prices without losing business?
- Are there proprietary technologies, certifications, or data formats that entrench suppliers?
- Do suppliers sell to many buyers, reducing their dependence on any one customer?

**High supplier power signals**: few players, proprietary capability, high switching cost, long delivery lead times, regulatory certification barriers.

## 2. Buyer power

Questions:
- How large is our spend relative to the supplier's total revenue?
- Do we represent a reference customer or a commodity transaction to the supplier?
- Can we credibly threaten to switch — and within what timeframe?
- Do we buy individually or through a consortium or framework?

**High buyer power signals**: large relative spend, multiple real alternatives, short switching timeline, group purchasing leverage.

## 3. Substitutes

Questions:
- Can the need be met by a different product, technology, or service model?
- Is there a viable insource option?
- Are technology trends shifting the solution landscape?
- Would a different category definition or specification unlock more competition?

## 4. New entrants

Questions:
- How easy is it for a new supplier to enter this market?
- What are the barriers to entry: capital, certification, talent, regulation?
- Are there new entrants from adjacent categories or geographies gaining traction?
- Is the market growing in ways that attract new investment?

**High entry barrier signals**: heavy regulation, safety certification requirements, capital-intensive infrastructure, long customer reference cycles.

## 5. Competitive intensity

Questions:
- How actively do suppliers compete on price, service, and innovation?
- Are there price wars, margin compression, or consolidation activity?
- What is recent M&A or partnership activity in this market?
- Are suppliers differentiating on capability, geography, or commercial model?

---

## Output format per dimension

For each dimension return:
- **Rating**: `HIGH`, `MEDIUM`, or `LOW` power / intensity
- **Key finding**: one sentence
- **Evidence source**: what this is based on and from where
- **Confidence**: `HIGH` / `MEDIUM` / `LOW` — how reliable the finding is given available data

Aggregate into a market summary: overall attractiveness for competitive sourcing, and primary risk factors to flag.
