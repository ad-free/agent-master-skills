# Input gate

Read when the input is vague, a one-liner, or comes as spec files.

| Input | Action |
|---|---|
| Short or vague ("Build HRM", "Make me a CRM") | Do not build. Draft a Task Brief from what is known, list open questions, ask the user to confirm. Offer `product-thinking` if the idea itself is unformed. |
| "Just build it, I'll know it when I see it" | Same: draft the brief and get a yes. Building without written requirements produces rework. |
| Spec files attached (md, pdf, xlsx, csv) | Load `project-discovery` to extract the domain model, then continue. |
| `PRODUCT.md`, `DOMAIN.md`, or `PLAN.md` exists | Load it as the requirements source. |
| Thin description | Offer the task template in `challenge.md`. |
| Clear request or spec | Proceed. |
