# Cooklang Extraction Guide for LLMs

Save recipes in cooklang format. Use the files in the recipes directory to answer questions.
You also have access to a Postgres tool where you can execute arbitrary queries. Use it to store information!


## Core Syntax

**Ingredients**: `@ingredient{quantity%unit}`
- Single word: `@salt`
- Multiple words: `@black pepper{}`
- With quantity: `@potato{2}`
- With unit: `@bacon{1%kg}`

**Cookware**: `#pot` or `#potato masher{}`

**Timer**: `~{25%minutes}` or `~eggs{3%minutes}`

**Comments**: `-- inline comment` or `[- block comment -]`

## Structure Rules

- Each paragraph = one step
- Separate steps with blank lines
- Metadata goes in YAML front matter between `---` markers

## Key Extraction Patterns

1. **Ingredients**: Convert "2 kg potatoes" → `@potato{2%kg}`
2. **Cookware**: Convert "in a large pot" → `in a #pot{}`
3. **Times**: Convert "bake for 25 minutes" → `bake for ~{25%minutes}`
4. **Steps**: Split by action boundaries (prep, cook, serve)

## Metadata (optional)

```yaml
---
servings: 4
time: 45 minutes
tags: [quick, easy]
---
```

## Common Keys
- `servings`: number of people
- `time`: total duration
- `tags`: array of descriptors

## Scaling
- Use `=` for fixed quantities: `@salt{=1%tsp}` (won't scale with servings)
- Default: all quantities scale linearly with servings

```yaml
---
title: Spaghetti Carbonara
servings: 4
time: 25 minutes
tags: [pasta, italian, quick]
---

Bring a large #pot of salted water to boil. Add @spaghetti{400%g} and cook for ~{10%minutes} until al dente.

While pasta cooks, dice @pancetta{200%g} into small cubes. Heat a #large skillet over medium heat and cook @pancetta until crispy, about ~{5%minutes}.

In a #mixing bowl, whisk together @eggs{4}, @parmesan cheese{100%g}(grated), and @black pepper{1%tsp}.

Drain the pasta, reserving @pasta water{1%cup}. Add hot pasta to the skillet with pancetta and remove from heat.

Pour the egg mixture over the pasta and toss quickly, adding @pasta water{2%tbsp} at a time until creamy. -- The residual heat cooks the eggs; don't overheat or they'll scramble!

Serve immediately with extra @parmesan cheese{}(for serving) and @black pepper{}.
```