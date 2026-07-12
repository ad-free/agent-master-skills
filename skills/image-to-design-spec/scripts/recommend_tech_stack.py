#!/usr/bin/env python3
"""
Tech Stack Recommendation Module
Recommends best-in-class frontend stack based on detected page type and components.
"""

RECOMMENDATIONS = {
    "dashboard": {
        "frontend": {
            "framework": "Next.js + React",
            "reason": "SSR for data-heavy pages, file-based routing",
        },
        "styling": {
            "solution": "Tailwind CSS + shadcn/ui",
            "reason": "Pre-built dashboard components, stat cards, tables",
        },
        "state": {
            "library": "TanStack Query",
            "reason": "Server state for real-time dashboard data",
        },
        "charts": {
            "library": "Recharts",
            "reason": "React-native chart library for bar/donut/line charts",
        },
        "backend": {
            "framework": "Next.js API routes or Express",
            "reason": "Same-repo API for dashboard data",
        },
        "deployment": {
            "platform": "Vercel",
            "reason": "Optimized for Next.js, edge functions for API",
        },
    },
    "landing": {
        "frontend": {
            "framework": "Next.js or Astro",
            "reason": "Static generation for fast landing pages",
        },
        "styling": {
            "solution": "Tailwind CSS + Framer Motion",
            "reason": "Animation for hero sections, scroll effects",
        },
        "state": {
            "library": "None needed",
            "reason": "Landing pages are mostly static",
        },
        "backend": {
            "framework": "None or lightweight CMS",
            "reason": "Content can be Markdown or Sanity CMS",
        },
        "deployment": {
            "platform": "Vercel or Netlify",
            "reason": "Static export, global CDN",
        },
    },
    "login": {
        "frontend": {
            "framework": "Next.js + React",
            "reason": "Built-in auth patterns, middleware for protected routes",
        },
        "styling": {
            "solution": "Tailwind CSS",
            "reason": "Clean form styling, focus states",
        },
        "auth": {
            "library": "NextAuth.js / Auth.js or Supabase Auth",
            "reason": "Battle-tested auth with multiple providers",
        },
        "backend": {
            "framework": "Next.js API routes or Supabase",
            "reason": "Auth endpoints + database",
        },
        "deployment": {
            "platform": "Vercel",
            "reason": "Edge middleware for auth checks",
        },
    },
    "register": {
        "frontend": {
            "framework": "Next.js + React",
            "reason": "Form validation, API integration",
        },
        "styling": {
            "solution": "Tailwind CSS + shadcn/ui",
            "reason": "Form components, input validation styles",
        },
        "auth": {
            "library": "NextAuth.js / Auth.js or Supabase Auth",
            "reason": "Registration flow, email verification",
        },
        "backend": {
            "framework": "Supabase or Next.js API",
            "reason": "User creation, email sending",
        },
        "deployment": {"platform": "Vercel", "reason": "Serverless functions for auth"},
    },
    "analytics": {
        "frontend": {
            "framework": "Next.js + React",
            "reason": "SSR/SSG for analytics dashboards",
        },
        "styling": {
            "solution": "Tailwind CSS + shadcn/ui",
            "reason": "Progress bars, stat cards, dark mode",
        },
        "state": {
            "library": "TanStack Query + Zustand",
            "reason": "Real-time data + client state for filters",
        },
        "charts": {
            "library": "Recharts or D3.js",
            "reason": "Customizable charts, progress indicators",
        },
        "backend": {
            "framework": "Express or FastAPI",
            "reason": "REST API for analytics data aggregation",
        },
        "deployment": {
            "platform": "Vercel + Railway",
            "reason": "Frontend on edge, backend on dedicated",
        },
    },
    "pricing": {
        "frontend": {
            "framework": "Next.js or Astro",
            "reason": "Static generation, fast rendering",
        },
        "styling": {
            "solution": "Tailwind CSS",
            "reason": "Card layouts, responsive grid, hover effects",
        },
        "state": {"library": "None needed", "reason": "Static content"},
        "backend": {"framework": "Stripe + webhooks", "reason": "Payment processing"},
        "deployment": {
            "platform": "Vercel",
            "reason": "Static pages + serverless for webhooks",
        },
    },
    "settings": {
        "frontend": {
            "framework": "Next.js + React",
            "reason": "Form-heavy pages, client-side navigation",
        },
        "styling": {
            "solution": "Tailwind CSS + shadcn/ui",
            "reason": "Toggle, switch, input, select components",
        },
        "state": {
            "library": "React Hook Form + Zod",
            "reason": "Form validation, error handling",
        },
        "backend": {
            "framework": "Next.js API routes",
            "reason": "Simple CRUD for user settings",
        },
        "deployment": {
            "platform": "Vercel",
            "reason": "Serverless API for settings persistence",
        },
    },
    "blog": {
        "frontend": {
            "framework": "Next.js or Astro",
            "reason": "MDX support, static generation",
        },
        "styling": {
            "solution": "Tailwind CSS + typography plugin",
            "reason": "Prose styling for article content",
        },
        "state": {"library": "None needed", "reason": "Static content"},
        "backend": {
            "framework": "MDX or CMS (Sanity/Contentlayer)",
            "reason": "Content management",
        },
        "deployment": {
            "platform": "Vercel",
            "reason": "ISR for instant content updates",
        },
    },
    "portfolio": {
        "frontend": {
            "framework": "Next.js or Astro",
            "reason": "Static generation, image optimization",
        },
        "styling": {
            "solution": "Tailwind CSS + Framer Motion",
            "reason": "Grid layouts, hover effects, transitions",
        },
        "state": {"library": "None needed", "reason": "Static content"},
        "backend": {"framework": "None needed", "reason": "Fully static site"},
        "deployment": {
            "platform": "Vercel or Netlify",
            "reason": "Free hosting for static sites",
        },
    },
    "ecommerce": {
        "frontend": {
            "framework": "Next.js + React",
            "reason": "SSR for product pages, ISR for catalog",
        },
        "styling": {
            "solution": "Tailwind CSS + Radix UI",
            "reason": "Accordion, dialog, dropdown primitives",
        },
        "state": {
            "library": "Zustand + TanStack Query",
            "reason": "Cart state + product data fetching",
        },
        "backend": {
            "framework": "Next.js API + Stripe",
            "reason": "Product API, checkout, payment",
        },
        "deployment": {
            "platform": "Vercel",
            "reason": "Edge functions for cart, SSR for SEO",
        },
    },
}


GENERIC = {
    "frontend": {
        "framework": "Next.js + React",
        "reason": "Industry standard for modern web apps",
    },
    "styling": {
        "solution": "Tailwind CSS",
        "reason": "Utility-first, responsive, widely adopted",
    },
    "state": {
        "library": "Zustand or TanStack Query",
        "reason": "Lightweight state management",
    },
    "backend": {
        "framework": "Next.js API routes or Supabase",
        "reason": "Full-stack in one codebase",
    },
    "deployment": {
        "platform": "Vercel",
        "reason": "Optimized for Next.js, free tier available",
    },
}


PAGE_TYPE_NAMES = {
    "dashboard": "Admin Dashboard",
    "landing": "Landing Page",
    "login": "Login Page",
    "register": "Registration Page",
    "analytics": "Analytics Dashboard",
    "pricing": "Pricing Page",
    "settings": "Settings Page",
    "blog": "Blog",
    "portfolio": "Portfolio",
    "ecommerce": "E-commerce",
    "generic": "Web Application",
}


def recommend_tech_stack(page_type: str, components: list) -> dict:
    page_name = PAGE_TYPE_NAMES.get(page_type, "Web Application")
    recs = RECOMMENDATIONS.get(page_type, GENERIC).copy()

    comp_types = [c["type"] for c in components]

    if "navigation" in comp_types and "frontend" in recs:
        recs["frontend"] = {
            "framework": "Next.js + React",
            "reason": "File-based routing matches sidebar navigation structure",
        }

    if "input" in comp_types and "form" not in str(recs.get("state", {})):
        recs["form"] = {
            "library": "React Hook Form + Zod",
            "reason": "Form inputs detected — validation required",
        }

    if "toggle" in comp_types:
        recs["styling"] = {
            "solution": "Tailwind CSS + Radix UI",
            "reason": "Toggle/switch primitives built-in",
        }

    if "table" in comp_types:
        recs["table"] = {
            "library": "TanStack Table",
            "reason": "Tables detected — sortable, filterable, paginated data grids",
        }

    result = {
        "page_name": page_name,
        "page_type": page_type,
        "recommendations": recs,
    }

    return result


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Recommend tech stack from analysis")
    parser.add_argument(
        "--page-type", required=True, help="Page type from detect_page_type.py"
    )
    parser.add_argument("--components", help="JSON file of detected components")
    args = parser.parse_args()

    components = []
    if args.components:
        with open(args.components) as f:
            components = json.load(f)

    result = recommend_tech_stack(args.page_type, components)
    print(json.dumps(result, indent=2))
