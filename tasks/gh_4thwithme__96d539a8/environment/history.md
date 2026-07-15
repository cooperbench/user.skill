> DEVELOPER

hey bro for our feature ask ai we need to change predefined use-case based chips... our list right now is


New Hire Onboarding



Trade Shows & Expos



Gifting



Staff Uniforms



Workwear & Safety Uniforms



School Spirit



Faith & Community



Fitness & Wellness 



Non-profit & Advocacy



Team Events & Fun

> TOOL

tool_use Skill
id: toolu_01SqE3JPW8yn2Zg5RgqbDikE
```json
{
  "skill": "dev"
}
```

> TOOL

tool_result
id: toolu_01SqE3JPW8yn2Zg5RgqbDikE
```
Launching skill: dev
```

> AGENT

What's the new list?

> TOOL

tool_use Grep
id: toolu_01C8LCY8QYAGRpEGoF5z1iKb
```json
{
  "pattern": "New Hire Onboarding|Trade Shows|Gifting|Staff Uniforms",
  "output_mode": "files_with_matches"
}
```

> TOOL

tool_result
id: toolu_01C8LCY8QYAGRpEGoF5z1iKb
```
Found 3 files
src/components/ci-ask-ai/ci-ask-ai.tsx
src/constants/navigation-links.ts
src/components/ci-solutions/ci-solutions.spec.tsx
```

> TOOL

tool_use Grep
id: toolu_013KEPHHJQJdjNgmXVwW55KF
```json
{
  "pattern": "New Hire Onboarding|Trade Shows|Gifting|Staff Uniforms|School Spirit|Faith|Fitness|Non-profit|Team Events",
  "output_mode": "content",
  "path": "src/components/ci-ask-ai/ci-ask-ai.tsx"
}
```

> TOOL

tool_result
id: toolu_013KEPHHJQJdjNgmXVwW55KF
```
21:    name: 'Trade Shows',
31:    name: 'Gifting',
```

> TOOL

tool_use Read
id: toolu_01WVVvKQWkRMtEHuQtcBrpyM
```json
{
  "file_path": "/Users/4thwithme/Documents/repo/ci-header-footer/src/components/ci-ask-ai/ci-ask-ai.tsx",
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_01WVVvKQWkRMtEHuQtcBrpyM
```
1	import { Component, h, State, Listen, Element } from '@stencil/core';
2	import { isBrowser } from '../../constants/constants';
3	import { trackAnalyticsEvent } from '../../utils/analytics';
4	
5	const NEURAL_SEARCH_URL = 'http://localhost:9009/api/v1/neural-search';
6	const STORAGE_KEY = 'ci-ask-ai-history';
7	
8	interface CategoryTag {
9	  name: string;
10	  tip: string;
11	  blurb: string;
12	}
13	
14	const CATEGORY_TAGS: CategoryTag[] = [
15	  {
16	    name: 'Onboarding',
17	    tip: 'For new hires, we recommend a mix of high-utility tech and soft-touch apparel — T-shirts, pens, notebooks — to ensure they feel the quality on day one.',
18	    blurb: 'First impressions start with gear that makes new hires feel part of the team from day one.',
19	  },
20	  {
21	    name: 'Trade Shows',
22	    tip: 'Stand out on the floor with swag people actually keep — promo items, tote bags, sunglasses — curated so your booth is the one they remember.',
23	    blurb: 'Booths fade from memory, but quality swag travels home — these are the pieces people keep.',
24	  },
25	  {
26	    name: 'Events',
27	    tip: 'Fundraisers, meetups, community gatherings — T-shirts, tote bags, drinkware, and sunglasses that bring everyone together without stretching the budget.',
28	    blurb: […]

> AGENT

The code currently has a different set: Onboarding, Trade Shows, Events, Gifting, Uniforming, Spirit Wear, Team & Club Gear, Reselling.

Each chip needs `tip` and `blurb` text too. Do you want to replace the current list with yours and have me generate tips/blurbs, or do you have that content already?