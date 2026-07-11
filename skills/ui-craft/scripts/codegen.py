#!/usr/bin/env python3
"""
Code generation for ui-craft.
Generates design token files, component code, and configuration files.
"""

import json
import os
from pathlib import Path


def generate_tailwind_config(design_system: dict, version: str = "4") -> str:
    """Generate tailwind.config.ts from design system."""
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    spacing = design_system.get("spacing_scale", {})

    if version == "4":
        return _generate_tailwind_v4(colors, typography, spacing)
    return _generate_tailwind_v3(colors, typography, spacing)


def _generate_tailwind_v4(colors: dict, typography: dict, spacing: dict) -> str:
    """Generate Tailwind v4 CSS-first config."""
    lines = []
    lines.append('@import "tailwindcss";')
    lines.append("")
    lines.append("@theme {")

    # Colors
    color_map = {
        "primary": colors.get("primary", "#2563EB"),
        "primary-foreground": colors.get("on_primary", "#FFFFFF"),
        "secondary": colors.get("secondary", "#3B82F6"),
        "accent": colors.get("accent", "#F97316"),
        "background": colors.get("background", "#F8FAFC"),
        "foreground": colors.get("foreground", "#1E293B"),
        "muted": colors.get("muted", "#F1F5F9"),
        "muted-foreground": colors.get("muted_foreground", "#64748B"),
        "border": colors.get("border", "#E2E8F0"),
        "destructive": colors.get("destructive", "#EF4444"),
        "ring": colors.get("ring", "#2563EB"),
    }
    for name, hex_val in color_map.items():
        lines.append(f"  --color-{name}: {hex_val};")

    # Typography
    lines.append("")
    lines.append(
        f"  --font-heading: '{typography.get('heading', 'Inter')}', sans-serif;"
    )
    lines.append(f"  --font-body: '{typography.get('body', 'Inter')}', sans-serif;")

    # Spacing
    if spacing:
        lines.append("")
        for token, value in spacing.items():
            lines.append(f"  --space-{token}: {value};")

    lines.append("}")
    return "\n".join(lines)


def _generate_tailwind_v3(colors: dict, typography: dict, spacing: dict) -> str:
    """Generate Tailwind v3 JS config."""
    lines = []
    lines.append("/** @type {import('tailwindcss').Config} */")
    lines.append("module.exports = {")
    lines.append("  theme: {")
    lines.append("    extend: {")

    # Colors
    lines.append("      colors: {")
    color_map = {
        "primary": colors.get("primary", "#2563EB"),
        "primary-foreground": colors.get("on_primary", "#FFFFFF"),
        "secondary": colors.get("secondary", "#3B82F6"),
        "accent": colors.get("accent", "#F97316"),
        "background": colors.get("background", "#F8FAFC"),
        "foreground": colors.get("foreground", "#1E293B"),
        "muted": colors.get("muted", "#F1F5F9"),
        "muted-foreground": colors.get("muted_foreground", "#64748B"),
        "border": colors.get("border", "#E2E8F0"),
        "destructive": colors.get("destructive", "#EF4444"),
        "ring": colors.get("ring", "#2563EB"),
    }
    for name, hex_val in color_map.items():
        lines.append(f"    {name}: '{hex_val}',")
    lines.append("    },")
    lines.append("")

    # Fonts
    lines.append("    fontFamily: {")
    lines.append(
        f"      heading: ['{typography.get('heading', 'Inter')}', 'sans-serif'],"
    )
    lines.append(f"      body: ['{typography.get('body', 'Inter')}', 'sans-serif'],")
    lines.append("    },")
    lines.append("")

    # Spacing
    if spacing:
        lines.append("    spacing: {")
        for token, value in spacing.items():
            lines.append(f"      '{token}': '{value}',")
        lines.append("    },")

    lines.append("    },")
    lines.append("  },")
    lines.append("}")
    return "\n".join(lines)


def generate_tokens_css(design_system: dict) -> str:
    """Generate tokens.css with CSS custom properties."""
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    spacing = design_system.get("spacing_scale", {})

    lines = []
    lines.append(":root {")

    # Colors
    color_map = {
        "--color-primary": colors.get("primary", "#2563EB"),
        "--color-primary-foreground": colors.get("on_primary", "#FFFFFF"),
        "--color-secondary": colors.get("secondary", "#3B82F6"),
        "--color-accent": colors.get("accent", "#F97316"),
        "--color-background": colors.get("background", "#F8FAFC"),
        "--color-foreground": colors.get("foreground", "#1E293B"),
        "--color-muted": colors.get("muted", "#F1F5F9"),
        "--color-muted-foreground": colors.get("muted_foreground", "#64748B"),
        "--color-border": colors.get("border", "#E2E8F0"),
        "--color-destructive": colors.get("destructive", "#EF4444"),
        "--color-ring": colors.get("ring", "#2563EB"),
    }
    for name, hex_val in color_map.items():
        lines.append(f"  {name}: {hex_val};")

    # Typography
    typography = design_system.get("typography", {})
    lines.append("")
    lines.append(
        f"  --font-heading: '{typography.get('heading', 'Inter')}', sans-serif;"
    )
    lines.append(f"  --font-body: '{typography.get('body', 'Inter')}', sans-serif;")

    # Spacing
    spacing = design_system.get("spacing_scale", {})
    if spacing:
        lines.append("")
        for token, value in spacing.items():
            lines.append(f"  --space-{token}: {value};")

    lines.append("}")
    return "\n".join(lines)


def generate_theme_ts(design_system: dict) -> str:
    """Generate TypeScript theme object."""
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})

    lines = []
    lines.append("export const theme = {")
    lines.append("  colors: {")
    color_map = {
        "primary": colors.get("primary", "#2563EB"),
        "primaryForeground": colors.get("on_primary", "#FFFFFF"),
        "secondary": colors.get("secondary", "#3B82F6"),
        "accent": colors.get("accent", "#F97316"),
        "background": colors.get("background", "#F8FAFC"),
        "foreground": colors.get("foreground", "#1E293B"),
        "muted": colors.get("muted", "#F1F5F9"),
        "mutedForeground": colors.get("muted_foreground", "#64748B"),
        "border": colors.get("border", "#E2E8F0"),
        "destructive": colors.get("destructive", "#EF4444"),
        "ring": colors.get("ring", "#2563EB"),
    }
    for name, hex_val in color_map.items():
        lines.append(f"  {name}: '{hex_val}',")
    lines.append("},")
    lines.append("")
    lines.append("  fonts: {")
    lines.append(f"    heading: '{typography.get('heading', 'Inter')}',")
    lines.append(f"    body: '{typography.get('body', 'Inter')}',")
    lines.append("  },")
    lines.append("};")
    return "\n".join(lines)


def generate_tokens_json(design_system: dict) -> str:
    """Generate design token JSON file."""
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    spacing = design_system.get("spacing_scale", {})

    tokens = {
        "colors": {
            "primary": colors.get("primary", "#2563EB"),
            "primary-foreground": colors.get("on_primary", "#FFFFFF"),
            "secondary": colors.get("secondary", "#3B82F6"),
            "accent": colors.get("accent", "#F97316"),
            "background": colors.get("background", "#F8FAFC"),
            "foreground": colors.get("foreground", "#1E293B"),
            "muted": colors.get("muted", "#F1F5F9"),
            "muted-foreground": colors.get("muted_foreground", "#64748B"),
            "border": colors.get("border", "#E2E8F0"),
            "destructive": colors.get("destructive", "#EF4444"),
            "ring": colors.get("ring", "#2563EB"),
        },
        "fonts": {
            "heading": typography.get("heading", "Inter"),
            "body": typography.get("body", "Inter"),
        },
        "spacing": spacing
        or {
            "xs": "4px",
            "sm": "8px",
            "md": "16px",
            "lg": "24px",
            "xl": "32px",
            "2xl": "48px",
            "3xl": "64px",
        },
    }
    return json.dumps(tokens, indent=2)


def generate_component(
    component_type: str, design_system: dict, version_info: dict
) -> str:
    """Generate a UI component file based on type and version info."""
    generators = {
        "button": _generate_button,
        "card": _generate_card,
        "modal": _generate_modal,
        "input": _generate_input,
        "navbar": _generate_navbar,
    }
    generator = generators.get(component_type, _generate_button)
    return generator(design_system, version_info)


def _generate_button(design_system: dict, version_info: dict) -> str:
    """Generate a Button component."""
    colors = design_system.get("colors", {})
    primary = colors.get("primary", "#2563EB")
    foreground = colors.get("foreground", "#1E293B")
    background = colors.get("background", "#F8FAFC")

    return """import { type VariantProps, cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-lg text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:opacity-90",
        secondary: "bg-secondary text-secondary-foreground hover:opacity-80",
        outline: "border border-border bg-transparent hover:bg-muted",
        ghost: "hover:bg-muted",
        destructive: "bg-destructive text-destructive-foreground hover:opacity-90",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  )
}
"""


def _generate_card(design_system: dict, version_info: dict) -> str:
    """Generate a Card component."""
    return """import { cn } from "@/lib/utils"

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "interactive"
}

export function Card({ className, variant = "default", ...props }: CardProps) {
  return (
    <div
      className={cn(
        "rounded-xl border bg-card text-card-foreground shadow-sm",
        variant === "interactive" && "transition-all duration-200 hover:shadow-md hover:-translate-y-0.5",
        className
      )}
      {...props}
    />
  )
}

export function CardHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
}

export function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h3 className={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...props} />
}

export function CardDescription({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  return <p className={cn("text-sm text-muted-foreground", className)} {...props} />
}

export function CardContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("p-6 pt-0", className)} {...props} />
}

export function CardFooter({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex items-center p-6 pt-0", className)} {...props} />
}
"""


def _generate_modal(design_system: dict, version_info: dict) -> str:
    """Generate a Modal component."""
    return """import { useEffect, useRef } from "react"
import { cn } from "@/lib/utils"

interface ModalProps {
  open: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
  className?: string
}

export function Modal({ open, onClose, title, children, className }: ModalProps) {
  const overlayRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose()
    }
    if (open) {
      document.addEventListener("keydown", handleEscape)
      document.body.style.overflow = "hidden"
    }
    return () => {
      document.removeEventListener("keydown", handleEscape)
      document.body.style.overflow = ""
    }
  }, [open, onClose])

  if (!open) return null

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
      onClick={(e) => e.target === overlayRef.current && onClose()}
      role="dialog"
      aria-modal="true"
    >
      <div
        className={cn(
          "bg-background rounded-xl shadow-xl max-w-lg w-full mx-4 p-6",
          "animate-in fade-in zoom-in-95 duration-200",
          className
        )}
      >
        {children}
      </div>
    </div>
  )
}
"""


def _generate_input(design_system: dict, version_info: dict) -> str:
    """Generate an Input component."""
    return """import { cn } from "@/lib/utils"

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  hint?: string
}

export function Input({ className, label, error, hint, id, ...props }: InputProps) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, "-")

  return (
    <div className="space-y-2">
      {label && (
        <label
          htmlFor={inputId}
          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
        >
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2",
          "text-sm ring-offset-background",
          "file:border-0 file:bg-transparent file:text-sm file:font-medium",
          "placeholder:text-muted-foreground",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
          "disabled:cursor-not-allowed disabled:opacity-50",
          error && "border-destructive focus-visible:ring-destructive",
          className
        )}
        aria-invalid={error ? "true" : undefined}
        aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
        {...props}
      />
      {error && (
        <p id={`${inputId}-error`} className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}
      {hint && !error && (
        <p id={`${inputId}-hint`} className="text-sm text-muted-foreground">
          {hint}
        </p>
      )}
    </div>
  )
}
"""


def _generate_navbar(design_system: dict, version_info: dict) -> str:
    """Generate a Navbar component."""
    return """import { cn } from "@/lib/utils"

interface NavItem {
  label: string
  href: string
  active?: boolean
}

interface NavbarProps {
  items: NavItem[]
  logo?: string
  className?: string
}

export function Navbar({ items, logo = "Logo", className }: NavbarProps) {
  return (
    <nav
      className={cn(
        "sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60",
        className
      )}
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="container flex h-16 items-center justify-between">
        <a href="/" className="text-xl font-bold" aria-label="Home">
          {logo}
        </a>
        <div className="hidden md:flex md:gap-6">
          {items.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className={cn(
                "text-sm font-medium transition-colors hover:text-primary",
                item.active ? "text-primary" : "text-muted-foreground"
              )}
              aria-current={item.active ? "page" : undefined}
            >
              {item.label}
            </a>
          ))}
        </div>
      </div>
    </nav>
  )
}
"""


def generate_all_tokens(
    design_system: dict, version_info: dict, output_dir: str
) -> dict:
    """Generate all design token files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    files = {}

    # Generate tailwind config
    tailwind_version = version_info.get("tailwindcss", "4")
    tailwind_content = generate_tailwind_config(design_system, tailwind_version)
    tailwind_file = output_path / "tailwind.config.ts"
    tailwind_file.write_text(tailwind_content, encoding="utf-8")
    files["tailwind.config.ts"] = str(tailwind_file)

    # Generate tokens.css
    tokens_css = generate_tokens_css(design_system)
    css_file = output_path / "tokens.css"
    css_file.write_text(tokens_css, encoding="utf-8")
    files["tokens.css"] = str(css_file)

    # Generate theme.ts
    theme_ts = generate_theme_ts(design_system)
    theme_file = output_path / "theme.ts"
    theme_file.write_text(theme_ts, encoding="utf-8")
    files["theme.ts"] = str(theme_file)

    # Generate tokens.json
    tokens_json = generate_tokens_json(design_system)
    json_file = output_path / "tokens.json"
    json_file.write_text(tokens_json, encoding="utf-8")
    files["tokens.json"] = str(json_file)

    return files


# ============ FORM GENERATION ============

def generate_form(form_type: str, design_system: dict, version_info: dict) -> str:
    """Generate a complete form with React Hook Form + Zod."""
    generators = {
        "login": _generate_login_form,
        "signup": _generate_signup_form,
        "contact": _generate_contact_form,
        "settings": _generate_settings_form,
        "password-reset": _generate_password_reset_form,
    }
    generator = generators.get(form_type, _generate_contact_form)
    return generator(design_system, version_info)


def _generate_login_form(design_system: dict, version_info: dict) -> str:
    """Generate a login form with React Hook Form + Zod."""
    react_version = version_info.get("react", "19")
    if react_version.startswith("19"):
        return _generate_login_form_r19(design_system, version_info)
    return _generate_login_form_r18(design_system, version_info)


def _generate_login_form_r19(design_system: dict, version_info: dict) -> str:
    """Generate a login form for React 19 (Server Components + useActionState)."""
    return """'use client'

import { useActionState } from 'react'
import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email({ message: 'Please enter a valid email address' }),
  password: z.string().min(6, { message: 'Password must be at least 6 characters' }),
})

type LoginFormData = z.infer<typeof loginSchema>

async function loginAction(prevState: any, formData: FormData) {
  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  const result = loginSchema.safeParse(data)
  if (!result.success) {
    return {
      errors: result.error.flatten().fieldErrors,
      message: 'Invalid credentials',
    }
  }

  // TODO: Implement actual login logic
  return { errors: null, message: 'Login successful' }
}

export function LoginForm() {
  const [state, formAction, isPending] = useActionState(loginAction, null)

  return (
    <form action={formAction} className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={state?.errors?.email ? 'email-error' : undefined}
          aria-invalid={state?.errors?.email ? 'true' : undefined}
        />
        {state?.errors?.email && (
          <p id="email-error" className="text-sm text-destructive" role="alert">
            {state.errors.email[0]}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="password" className="text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={state?.errors?.password ? 'password-error' : undefined}
          aria-invalid={state?.errors?.password ? 'true' : undefined}
        />
        {state?.errors?.password && (
          <p id="password-error" className="text-sm text-destructive" role="alert">
            {state.errors.password[0]}
          </p>
        )}
      </div>

      {state?.message && (
        <p className="text-sm text-destructive" role="alert">
          {state.message}
        </p>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="inline-flex h-10 w-full items-center justify-center rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50"
      >
        {isPending ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  )
}
"""


def _generate_login_form_r18(design_system: dict, version_info: dict) -> str:
    """Generate a login form for React 18 (useTransition)."""
    return """'use client'

import { useState, useTransition } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email({ message: 'Please enter a valid email address' }),
  password: z.string().min(6, { message: 'Password must be at least 6 characters' }),
})

type LoginFormData = z.infer<typeof loginSchema>

export function LoginForm() {
  const [error, setError] = useState<string | null>(null)
  const [isPending, startTransition] = useTransition()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    setError(null)
    startTransition(async () => {
      try {
        // TODO: Implement actual login logic
        console.log('Login attempt:', data)
      } catch (err) {
        setError('Invalid credentials')
      }
    })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.email ? 'email-error' : undefined}
          aria-invalid={errors.email ? 'true' : undefined}
        />
        {errors.email && (
          <p id="email-error" className="text-sm text-destructive" role="alert">
            {errors.email.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="password" className="text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          {...register('password')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.password ? 'password-error' : undefined}
          aria-invalid={errors.password ? 'true' : undefined}
        />
        {errors.password && (
          <p id="password-error" className="text-sm text-destructive" role="alert">
            {errors.password.message}
          </p>
        )}
      </div>

      {error && (
        <p className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="inline-flex h-10 w-full items-center justify-center rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50"
      >
        {isPending ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  )
}
"""


def _generate_signup_form(design_system: dict, version_info: dict) -> str:
    """Generate a signup form with React Hook Form + Zod."""
    react_version = version_info.get("react", "19")
    if react_version.startswith("19"):
        return _generate_signup_form_r19(design_system, version_info)
    return _generate_signup_form_r18(design_system, version_info)


def _generate_signup_form_r19(design_system: dict, version_info: dict) -> str:
    """Generate a signup form for React 19."""
    return """'use client'

import { useActionState } from 'react'
import { z } from 'zod'

const signupSchema = z.object({
  name: z.string().min(2, { message: 'Name must be at least 2 characters' }),
  email: z.string().email({ message: 'Please enter a valid email address' }),
  password: z.string().min(8, { message: 'Password must be at least 8 characters' })
    .regex(/[A-Z]/, { message: 'Password must contain at least one uppercase letter' })
    .regex(/[0-9]/, { message: 'Password must contain at least one number' }),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
})

type SignupFormData = z.infer<typeof signupSchema>

async function signupAction(prevState: any, formData: FormData) {
  const data = {
    name: formData.get('name') as string,
    email: formData.get('email') as string,
    password: formData.get('password') as string,
    confirmPassword: formData.get('confirmPassword') as string,
  }

  const result = signupSchema.safeParse(data)
  if (!result.success) {
    return {
      errors: result.error.flatten().fieldErrors,
      message: 'Validation failed',
    }
  }

  // TODO: Implement actual signup logic
  return { errors: null, message: 'Signup successful' }
}

export function SignupForm() {
  const [state, formAction, isPending] = useActionState(signupAction, null)

  return (
    <form action={formAction} className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="name" className="text-sm font-medium">
          Name
        </label>
        <input
          id="name"
          name="name"
          type="text"
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={state?.errors?.name ? 'name-error' : undefined}
          aria-invalid={state?.errors?.name ? 'true' : undefined}
        />
        {state?.errors?.name && (
          <p id="name-error" className="text-sm text-destructive" role="alert">
            {state.errors.name[0]}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={state?.errors?.email ? 'email-error' : undefined}
          aria-invalid={state?.errors?.email ? 'true' : undefined}
        />
        {state?.errors?.email && (
          <p id="email-error" className="text-sm text-destructive" role="alert">
            {state.errors.email[0]}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="password" className="text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={state?.errors?.password ? 'password-error' : undefined}
          aria-invalid={state?.errors?.password ? 'true' : undefined}
        />
        {state?.errors?.password && (
          <p id="password-error" className="text-sm text-destructive" role="alert">
            {state.errors.password[0]}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="confirmPassword" className="text-sm font-medium">
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          name="confirmPassword"
          type="password"
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={state?.errors?.confirmPassword ? 'confirmPassword-error' : undefined}
          aria-invalid={state?.errors?.confirmPassword ? 'true' : undefined}
        />
        {state?.errors?.confirmPassword && (
          <p id="confirmPassword-error" className="text-sm text-destructive" role="alert">
            {state.errors.confirmPassword[0]}
          </p>
        )}
      </div>

      {state?.message && (
        <p className="text-sm text-destructive" role="alert">
          {state.message}
        </p>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="inline-flex h-10 w-full items-center justify-center rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50"
      >
        {isPending ? 'Creating account...' : 'Create Account'}
      </button>
    </form>
  )
}
"""


def _generate_signup_form_r18(design_system: dict, version_info: dict) -> str:
    """Generate a signup form for React 18."""
    return """'use client'

import { useState, useTransition } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const signupSchema = z.object({
  name: z.string().min(2, { message: 'Name must be at least 2 characters' }),
  email: z.string().email({ message: 'Please enter a valid email address' }),
  password: z.string().min(8, { message: 'Password must be at least 8 characters' })
    .regex(/[A-Z]/, { message: 'Password must contain at least one uppercase letter' })
    .regex(/[0-9]/, { message: 'Password must contain at least one number' }),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
})

type SignupFormData = z.infer<typeof signupSchema>

export function SignupForm() {
  const [error, setError] = useState<string | null>(null)
  const [isPending, startTransition] = useTransition()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
  })

  const onSubmit = async (data: SignupFormData) => {
    setError(null)
    startTransition(async () => {
      try {
        // TODO: Implement actual signup logic
        console.log('Signup attempt:', data)
      } catch (err) {
        setError('Failed to create account')
      }
    })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="name" className="text-sm font-medium">
          Name
        </label>
        <input
          id="name"
          type="text"
          {...register('name')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.name ? 'name-error' : undefined}
          aria-invalid={errors.name ? 'true' : undefined}
        />
        {errors.name && (
          <p id="name-error" className="text-sm text-destructive" role="alert">
            {errors.name.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.email ? 'email-error' : undefined}
          aria-invalid={errors.email ? 'true' : undefined}
        />
        {errors.email && (
          <p id="email-error" className="text-sm text-destructive" role="alert">
            {errors.email.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="password" className="text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          {...register('password')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.password ? 'password-error' : undefined}
          aria-invalid={errors.password ? 'true' : undefined}
        />
        {errors.password && (
          <p id="password-error" className="text-sm text-destructive" role="alert">
            {errors.password.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="confirmPassword" className="text-sm font-medium">
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          type="password"
          {...register('confirmPassword')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.confirmPassword ? 'confirmPassword-error' : undefined}
          aria-invalid={errors.confirmPassword ? 'true' : undefined}
        />
        {errors.confirmPassword && (
          <p id="confirmPassword-error" className="text-sm text-destructive" role="alert">
            {errors.confirmPassword.message}
          </p>
        )}
      </div>

      {error && (
        <p className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="inline-flex h-10 w-full items-center justify-center rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50"
      >
        {isPending ? 'Creating account...' : 'Create Account'}
      </button>
    </form>
  )
}
"""


def _generate_contact_form(design_system: dict, version_info: dict) -> str:
    """Generate a contact form with React Hook Form + Zod."""
    react_version = version_info.get("react", "19")
    if react_version.startswith("19"):
        return _generate_contact_form_r19(design_system, version_info)
    return _generate_contact_form_r18(design_system, version_info)


def _generate_contact_form_r19(design_system: dict, version_info: dict) -> str:
    """Generate a contact form for React 19."""
    return """'use client'

import { useActionState } from 'react'
import { z } from 'zod'

const contactSchema = z.object({
  name: z.string().min(2, { message: 'Name must be at least 2 characters' }),
  email: z.string().email({ message: 'Please enter a valid email address' }),
  subject: z.string().min(5, { message: 'Subject must be at least 5 characters' }),
  message: z.string().min(10, { message: 'Message must be at least 10 characters' }),
})

type ContactFormData = z.infer<typeof contactSchema>

async function contactAction(prevState: any, formData: FormData) {
  const data = {
    name: formData.get('name') as string,
    email: formData.get('email') as string,
    subject: formData.get('subject') as string,
    message: formData.get('message') as string,
  }

  const result = contactSchema.safeParse(data)
  if (!result.success) {
    return {
      errors: result.error.flatten().fieldErrors,
      message: 'Validation failed',
    }
  }

  // TODO: Implement actual contact logic
  return { errors: null, message: 'Message sent successfully' }
}

export function ContactForm() {
  const [state, formAction, isPending] = useActionState(contactAction, null)

  return (
    <form action={formAction} className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="name" className="text-sm font-medium">
          Name
        </label>
        <input
          id="name"
          name="name"
          type="text"
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={state?.errors?.name ? 'name-error' : undefined}
          aria-invalid={state?.errors?.name ? 'true' : undefined}
        />
        {state?.errors?.name && (
          <p id="name-error" className="text-sm text-destructive" role="alert">
            {state.errors.name[0]}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={state?.errors?.email ? 'email-error' : undefined}
          aria-invalid={state?.errors?.email ? 'true' : undefined}
        />
        {state?.errors?.email && (
          <p id="email-error" className="text-sm text-destructive" role="alert">
            {state.errors.email[0]}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="subject" className="text-sm font-medium">
          Subject
        </label>
        <input
          id="subject"
          name="subject"
          type="text"
          required
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={state?.errors?.subject ? 'subject-error' : undefined}
          aria-invalid={state?.errors?.subject ? 'true' : undefined}
        />
        {state?.errors?.subject && (
          <p id="subject-error" className="text-sm text-destructive" role="alert">
            {state.errors.subject[0]}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="message" className="text-sm font-medium">
          Message
        </label>
        <textarea
          id="message"
          name="message"
          rows={4}
          required
          className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring min-h-[100px]"
          aria-describedby={state?.errors?.message ? 'message-error' : undefined}
          aria-invalid={state?.errors?.message ? 'true' : undefined}
        />
        {state?.errors?.message && (
          <p id="message-error" className="text-sm text-destructive" role="alert">
            {state.errors.message[0]}
          </p>
        )}
      </div>

      {state?.message && (
        <p className="text-sm text-destructive" role="alert">
          {state.message}
        </p>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="inline-flex h-10 w-full items-center justify-center rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50"
      >
        {isPending ? 'Sending...' : 'Send Message'}
      </button>
    </form>
  )
}
"""


def _generate_contact_form_r18(design_system: dict, version_info: dict) -> str:
    """Generate a contact form for React 18."""
    return """'use client'

import { useState, useTransition } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const contactSchema = z.object({
  name: z.string().min(2, { message: 'Name must be at least 2 characters' }),
  email: z.string().email({ message: 'Please enter a valid email address' }),
  subject: z.string().min(5, { message: 'Subject must be at least 5 characters' }),
  message: z.string().min(10, { message: 'Message must be at least 10 characters' }),
})

type ContactFormData = z.infer<typeof contactSchema>

export function ContactForm() {
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [isPending, startTransition] = useTransition()

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
  })

  const onSubmit = async (data: ContactFormData) => {
    setError(null)
    setSuccess(false)
    startTransition(async () => {
      try {
        // TODO: Implement actual contact logic
        console.log('Contact form submitted:', data)
        setSuccess(true)
        reset()
      } catch (err) {
        setError('Failed to send message')
      }
    })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="name" className="text-sm font-medium">
          Name
        </label>
        <input
          id="name"
          type="text"
          {...register('name')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.name ? 'name-error' : undefined}
          aria-invalid={errors.name ? 'true' : undefined}
        />
        {errors.name && (
          <p id="name-error" className="text-sm text-destructive" role="alert">
            {errors.name.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.email ? 'email-error' : undefined}
          aria-invalid={errors.email ? 'true' : undefined}
        />
        {errors.email && (
          <p id="email-error" className="text-sm text-destructive" role="alert">
            {errors.email.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="subject" className="text-sm font-medium">
          Subject
        </label>
        <input
          id="subject"
          type="text"
          {...register('subject')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.subject ? 'subject-error' : undefined}
          aria-invalid={errors.subject ? 'true' : undefined}
        />
        {errors.subject && (
          <p id="subject-error" className="text-sm text-destructive" role="alert">
            {errors.subject.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="message" className="text-sm font-medium">
          Message
        </label>
        <textarea
          id="message"
          rows={4}
          {...register('message')}
          className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring min-h-[100px]"
          aria-describedby={errors.message ? 'message-error' : undefined}
          aria-invalid={errors.message ? 'true' : undefined}
        />
        {errors.message && (
          <p id="message-error" className="text-sm text-destructive" role="alert">
            {errors.message.message}
          </p>
        )}
      </div>

      {error && (
        <p className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}

      {success && (
        <p className="text-sm text-green-600" role="status">
          Message sent successfully!
        </p>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="inline-flex h-10 w-full items-center justify-center rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50"
      >
        {isPending ? 'Sending...' : 'Send Message'}
      </button>
    </form>
  )
}
"""


def _generate_settings_form(design_system: dict, version_info: dict) -> str:
    """Generate a settings form with React Hook Form + Zod."""
    return """'use client'

import { useState, useTransition } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const settingsSchema = z.object({
  name: z.string().min(2, { message: 'Name must be at least 2 characters' }),
  email: z.string().email({ message: 'Please enter a valid email address' }),
  bio: z.string().max(500, { message: 'Bio must be less than 500 characters' }).optional(),
  notifications: z.boolean().default(true),
  theme: z.enum(['light', 'dark', 'system']).default('system'),
})

type SettingsFormData = z.infer<typeof settingsSchema>

export function SettingsForm() {
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [isPending, startTransition] = useTransition()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SettingsFormData>({
    resolver: zodResolver(settingsSchema),
    defaultValues: {
      name: '',
      email: '',
      bio: '',
      notifications: true,
      theme: 'system',
    },
  })

  const onSubmit = async (data: SettingsFormData) => {
    setError(null)
    setSuccess(false)
    startTransition(async () => {
      try {
        // TODO: Implement actual settings update logic
        console.log('Settings updated:', data)
        setSuccess(true)
      } catch (err) {
        setError('Failed to update settings')
      }
    })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="space-y-2">
        <label htmlFor="name" className="text-sm font-medium">
          Name
        </label>
        <input
          id="name"
          type="text"
          {...register('name')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.name ? 'name-error' : undefined}
          aria-invalid={errors.name ? 'true' : undefined}
        />
        {errors.name && (
          <p id="name-error" className="text-sm text-destructive" role="alert">
            {errors.name.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.email ? 'email-error' : undefined}
          aria-invalid={errors.email ? 'true' : undefined}
        />
        {errors.email && (
          <p id="email-error" className="text-sm text-destructive" role="alert">
            {errors.email.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="bio" className="text-sm font-medium">
          Bio
        </label>
        <textarea
          id="bio"
          rows={3}
          {...register('bio')}
          className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring min-h-[80px]"
          aria-describedby={errors.bio ? 'bio-error' : undefined}
          aria-invalid={errors.bio ? 'true' : undefined}
        />
        {errors.bio && (
          <p id="bio-error" className="text-sm text-destructive" role="alert">
            {errors.bio.message}
          </p>
        )}
      </div>

      <div className="flex items-center space-x-2">
        <input
          type="checkbox"
          id="notifications"
          {...register('notifications')}
          className="h-4 w-4 rounded border-input"
        />
        <label htmlFor="notifications" className="text-sm font-medium">
          Enable notifications
        </label>
      </div>

      <div className="space-y-2">
        <label htmlFor="theme" className="text-sm font-medium">
          Theme
        </label>
        <select
          id="theme"
          {...register('theme')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <option value="light">Light</option>
          <option value="dark">Dark</option>
          <option value="system">System</option>
        </select>
      </div>

      {error && (
        <p className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}

      {success && (
        <p className="text-sm text-green-600" role="status">
          Settings updated successfully!
        </p>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="inline-flex h-10 items-center justify-center rounded-md bg-primary text-primary-foreground px-4 hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50"
      >
        {isPending ? 'Saving...' : 'Save Changes'}
      </button>
    </form>
  )
}
"""


def _generate_password_reset_form(design_system: dict, version_info: dict) -> str:
    """Generate a password reset form with React Hook Form + Zod."""
    return """'use client'

import { useState, useTransition } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const passwordResetSchema = z.object({
  email: z.string().email({ message: 'Please enter a valid email address' }),
})

type PasswordResetFormData = z.infer<typeof passwordResetSchema>

export function PasswordResetForm() {
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [isPending, startTransition] = useTransition()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<PasswordResetFormData>({
    resolver: zodResolver(passwordResetSchema),
  })

  const onSubmit = async (data: PasswordResetFormData) => {
    setError(null)
    setSuccess(false)
    startTransition(async () => {
      try {
        // TODO: Implement actual password reset logic
        console.log('Password reset requested for:', data.email)
        setSuccess(true)
      } catch (err) {
        setError('Failed to send reset email')
      }
    })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          aria-describedby={errors.email ? 'email-error' : undefined}
          aria-invalid={errors.email ? 'true' : undefined}
        />
        {errors.email && (
          <p id="email-error" className="text-sm text-destructive" role="alert">
            {errors.email.message}
          </p>
        )}
      </div>

      {error && (
        <p className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}

      {success && (
        <p className="text-sm text-green-600" role="status">
          If an account exists with that email, you'll receive a password reset link shortly.
        </p>
      )}

      <button
        type="submit"
        disabled={isPending}
        className="inline-flex h-10 w-full items-center justify-center rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50"
      >
        {isPending ? 'Sending...' : 'Send Reset Link'}
      </button>
    </form>
  )
}
"""


# ============ PAGE TEMPLATE GENERATION ============

def generate_page(page_type: str, design_system: dict, version_info: dict) -> str:
    """Generate a complete page template."""
    generators = {
        "landing": _generate_landing_page,
        "dashboard-layout": _generate_dashboard_layout,
        "auth": _generate_auth_page,
        "settings": _generate_settings_page,
        "404": _generate_404_page,
    }
    generator = generators.get(page_type, _generate_landing_page)
    return generator(design_system, version_info)


def _generate_landing_page(design_system: dict, version_info: dict) -> str:
    """Generate a landing page with hero, features, testimonials, pricing, CTA."""
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    style_name = design_system.get("style", {}).get("name", "Minimalism")

    return f"""// Landing Page — Generated by ui-craft
// Style: {style_name}

export default function LandingPage() {{
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <a href="/" className="text-xl font-bold">
            YourBrand
          </a>
          <div className="hidden md:flex md:gap-6">
            <a href="#features" className="text-sm font-medium text-muted-foreground hover:text-primary">
              Features
            </a>
            <a href="#pricing" className="text-sm font-medium text-muted-foreground hover:text-primary">
              Pricing
            </a>
            <a href="#testimonials" className="text-sm font-medium text-muted-foreground hover:text-primary">
              Testimonials
            </a>
            <a href="/login" className="text-sm font-medium text-muted-foreground hover:text-primary">
              Login
            </a>
            <a href="/signup" className="inline-flex h-9 items-center justify-center rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground hover:bg-primary/90">
              Get Started
            </a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container py-24 md:py-32">
        <div className="mx-auto max-w-2xl text-center">
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
            Build something amazing
          </h1>
          <p className="mt-6 text-lg text-muted-foreground">
            A complete solution for your next project. Fast, accessible, and beautiful.
          </p>
          <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:justify-center">
            <a
              href="/signup"
              className="inline-flex h-11 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground hover:bg-primary/90"
            >
              Get Started Free
            </a>
            <a
              href="#features"
              className="inline-flex h-11 items-center justify-center rounded-md border border-border bg-background px-8 text-sm font-medium hover:bg-muted"
            >
              Learn More
            </a>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="border-t bg-muted/50 py-24">
        <div className="container">
          <h2 className="text-3xl font-bold text-center">Features</h2>
          <p className="mt-4 text-center text-muted-foreground">
            Everything you need to build modern applications.
          </p>
          <div className="mt-16 grid gap-8 md:grid-cols-3">
            {{['Feature 1', 'Feature 2', 'Feature 3'].map((feature) => (
              <div key={{feature}} className="rounded-xl border bg-card p-6">
                <h3 className="text-xl font-semibold">{{feature}}</h3>
                <p className="mt-2 text-sm text-muted-foreground">
                  Description of {{feature.toLowerCase()}} goes here.
                </p>
              </div>
            ))}}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-24">
        <div className="container">
          <h2 className="text-3xl font-bold text-center">Testimonials</h2>
          <div className="mt-16 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {{[
              {{ name: 'User 1', role: 'Developer', quote: 'Amazing product!' }},
              {{ name: 'User 2', role: 'Designer', quote: 'Best tool I\'ve used.' }},
              {{ name: 'User 3', role: 'CEO', quote: 'Highly recommended.' }},
            ].map((testimonial) => (
              <div key={{testimonial.name}} className="rounded-xl border bg-card p-6">
                <p className="text-muted-foreground">"{{testimonial.quote}}"</p>
                <div className="mt-4">
                  <p className="font-semibold">{{testimonial.name}}</p>
                  <p className="text-sm text-muted-foreground">{{testimonial.role}}</p>
                </div>
              </div>
            ))}}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="border-t bg-muted/50 py-24">
        <div className="container">
          <h2 className="text-3xl font-bold text-center">Pricing</h2>
          <div className="mt-16 grid gap-8 md:grid-cols-3 max-w-4xl mx-auto">
            {{[
              {{ name: 'Starter', price: '$9', features: ['Feature A', 'Feature B'] }},
              {{ name: 'Pro', price: '$29', features: ['Feature A', 'Feature B', 'Feature C'] }},
              {{ name: 'Enterprise', price: '$99', features: ['Feature A', 'Feature B', 'Feature C', 'Feature D'] }},
            ].map((plan) => (
              <div key={{plan.name}} className="rounded-xl border bg-card p-6 text-center">
                <h3 className="text-xl font-semibold">{{plan.name}}</h3>
                <p className="mt-2 text-3xl font-bold">{{plan.price}}<span className="text-sm font-normal text-muted-foreground">/mo</span></p>
                <ul className="mt-6 space-y-2">
                  {{plan.features.map((feature) => (
                    <li key={{feature}} className="text-sm text-muted-foreground">
                      ✓ {{feature}}
                    </li>
                  ))}}
                </ul>
                <button className="mt-6 inline-flex h-10 w-full items-center justify-center rounded-md bg-primary text-primary-foreground hover:bg-primary/90">
                  Get Started
                </button>
              </div>
            ))}}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24">
        <div className="container text-center">
          <h2 className="text-3xl font-bold">Ready to get started?</h2>
          <p className="mt-4 text-muted-foreground">
            Join thousands of users who are already building with our platform.
          </p>
          <a
            href="/signup"
            className="mt-8 inline-flex h-11 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground hover:bg-primary/90"
          >
            Start Free Trial
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-12">
        <div className="container">
          <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
            <p className="text-sm text-muted-foreground">
              © 2024 YourBrand. All rights reserved.
            </p>
            <div className="flex gap-4">
              <a href="#" className="text-sm text-muted-foreground hover:text-primary">
                Privacy
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-primary">
                Terms
              </a>
              <a href="#" className="text-sm text-muted-foreground hover:text-primary">
                Contact
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}}
"""


def _generate_dashboard_layout(design_system: dict, version_info: dict) -> str:
    """Generate a dashboard layout with sidebar, header, and content area."""
    return """// Dashboard Layout — Generated by ui-craft

import { ReactNode } from 'react'

interface DashboardLayoutProps {
  children: ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r bg-background">
        <div className="flex h-16 items-center border-b px-6">
          <a href="/" className="text-xl font-bold">
            Dashboard
          </a>
        </div>
        <nav className="space-y-1 p-4">
          {[
            { label: 'Overview', href: '/dashboard', icon: '📊' },
            { label: 'Analytics', href: '/dashboard/analytics', icon: '📈' },
            { label: 'Users', href: '/dashboard/users', icon: '👥' },
            { label: 'Settings', href: '/dashboard/settings', icon: '⚙️' },
          ].map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground"
            >
              <span>{item.icon}</span>
              {item.label}
            </a>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <div className="ml-64">
        {/* Header */}
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b bg-background/95 backdrop-blur px-6">
          <h1 className="text-lg font-semibold">Dashboard</h1>
          <div className="flex items-center gap-4">
            <button className="inline-flex h-9 items-center justify-center rounded-md border border-border px-3 text-sm hover:bg-muted">
              🔔
            </button>
            <div className="h-8 w-8 rounded-full bg-muted" />
          </div>
        </header>

        {/* Page Content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
"""


def _generate_auth_page(design_system: dict, version_info: dict) -> str:
    """Generate an auth page with login, signup, and password reset."""
    return """// Auth Page — Generated by ui-craft
// Includes login, signup, and password reset forms

export default function AuthPage({ type = 'login' }: { type?: 'login' | 'signup' | 'reset' }) {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold">
            {type === 'login' && 'Welcome back'}
            {type === 'signup' && 'Create an account'}
            {type === 'reset' && 'Reset your password'}
          </h1>
          <p className="mt-2 text-sm text-muted-foreground">
            {type === 'login' && 'Enter your credentials to access your account'}
            {type === 'signup' && 'Enter your details to get started'}
            {type === 'reset' && "Enter your email and we'll send you a reset link"}
          </p>
        </div>

        {/* Forms are imported from components/auth/ */}
        <div className="rounded-xl border bg-card p-6 shadow-sm">
          {/* LoginForm, SignupForm, or PasswordResetForm goes here */}
        </div>

        <div className="text-center text-sm text-muted-foreground">
          {type === 'login' && (
            <>
              Don't have an account?{' '}
              <a href="/signup" className="text-primary hover:underline">
                Sign up
              </a>
            </>
          )}
          {type === 'signup' && (
            <>
              Already have an account?{' '}
              <a href="/login" className="text-primary hover:underline">
                Sign in
              </a>
            </>
          )}
          {type === 'reset' && (
            <>
              Remember your password?{' '}
              <a href="/login" className="text-primary hover:underline">
                Sign in
              </a>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
"""


def _generate_settings_page(design_system: dict, version_info: dict) -> str:
    """Generate a settings page with tabs and form sections."""
    return """// Settings Page — Generated by ui-craft

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Settings</h2>
        <p className="text-muted-foreground">
          Manage your account settings and preferences.
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b">
        <nav className="flex gap-6" aria-label="Settings tabs">
          {['Profile', 'Security', 'Notifications', 'Billing'].map((tab) => (
            <button
              key={tab}
              className="border-b-2 border-transparent pb-3 text-sm font-medium text-muted-foreground hover:text-foreground"
              aria-selected={tab === 'Profile'}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>

      {/* Settings Form */}
      <div className="max-w-2xl">
        {/* SettingsForm component goes here */}
        <p className="text-muted-foreground">
          Import SettingsForm from components/settings/SettingsForm.tsx
        </p>
      </div>
    </div>
  )
}
"""


def _generate_404_page(design_system: dict, version_info: dict) -> str:
    """Generate a 404 not found page."""
    return """// 404 Page — Generated by ui-craft

export default function NotFoundPage() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-muted-foreground">404</h1>
        <p className="mt-4 text-xl text-muted-foreground">
          Page not found
        </p>
        <p className="mt-2 text-muted-foreground">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <a
          href="/"
          className="mt-8 inline-flex h-10 items-center justify-center rounded-md bg-primary px-6 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          Go Home
        </a>
      </div>
    </div>
  )
}
"""


# ============ COMPONENT TEST GENERATION ============

def generate_component_test(component_type: str, design_system: dict, version_info: dict) -> str:
    """Generate a test file for a component."""
    generators = {
        "button": _generate_button_test,
        "card": _generate_card_test,
        "input": _generate_input_test,
        "modal": _generate_modal_test,
        "navbar": _generate_navbar_test,
    }
    generator = generators.get(component_type, _generate_button_test)
    return generator(design_system, version_info)


def _generate_button_test(design_system: dict, version_info: dict) -> str:
    """Generate tests for Button component."""
    return """// Button.test.tsx — Generated by ui-craft
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe, toHaveNoViolations } from 'jest-axe'
import { Button } from './button'

expect.extend(toHaveNoViolations)

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument()
  })

  it('renders different variants', () => {
    const { rerender } = render(<Button variant="default">Default</Button>)
    expect(screen.getByRole('button')).toHaveClass('bg-primary')

    rerender(<Button variant="secondary">Secondary</Button>)
    expect(screen.getByRole('button')).toHaveClass('bg-secondary')

    rerender(<Button variant="outline">Outline</Button>)
    expect(screen.getByRole('button')).toHaveClass('border')

    rerender(<Button variant="ghost">Ghost</Button>)
    expect(screen.getByRole('button')).toHaveClass('hover:bg-muted')

    rerender(<Button variant="destructive">Destructive</Button>)
    expect(screen.getByRole('button')).toHaveClass('bg-destructive')
  })

  it('renders different sizes', () => {
    const { rerender } = render(<Button size="default">Default</Button>)
    expect(screen.getByRole('button')).toHaveClass('h-10')

    rerender(<Button size="sm">Small</Button>)
    expect(screen.getByRole('button')).toHaveClass('h-9')

    rerender(<Button size="lg">Large</Button>)
    expect(screen.getByRole('button')).toHaveClass('h-11')
  })

  it('handles click events', async () => {
    const user = userEvent.setup()
    const onClick = vi.fn()
    render(<Button onClick={onClick}>Click me</Button>)

    await user.click(screen.getByRole('button'))
    expect(onClick).toHaveBeenCalledTimes(1)
  })

  it('can be disabled', () => {
    render(<Button disabled>Disabled</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('has no accessibility violations', async () => {
    const { container } = render(<Button>Accessible Button</Button>)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
"""


def _generate_card_test(design_system: dict, version_info: dict) -> str:
    """Generate tests for Card component."""
    return """// Card.test.tsx — Generated by ui-craft
import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './card'

expect.extend(toHaveNoViolations)

describe('Card', () => {
  it('renders correctly', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Test Title</CardTitle>
          <CardDescription>Test Description</CardDescription>
        </CardHeader>
        <CardContent>Test Content</CardContent>
        <CardFooter>Test Footer</CardFooter>
      </Card>
    )

    expect(screen.getByText('Test Title')).toBeInTheDocument()
    expect(screen.getByText('Test Description')).toBeInTheDocument()
    expect(screen.getByText('Test Content')).toBeInTheDocument()
    expect(screen.getByText('Test Footer')).toBeInTheDocument()
  })

  it('renders interactive variant', () => {
    render(<Card variant="interactive">Interactive Card</Card>)
    expect(screen.getByText('Interactive Card').parentElement).toHaveClass('hover:shadow-md')
  })

  it('applies custom className', () => {
    render(<Card className="custom-class">Custom</Card>)
    expect(screen.getByText('Custom').parentElement).toHaveClass('custom-class')
  })

  it('has no accessibility violations', async () => {
    const { container } = render(
      <Card>
        <CardHeader>
          <CardTitle>Accessible Card</CardTitle>
        </CardHeader>
        <CardContent>Content</CardContent>
      </Card>
    )
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
"""


def _generate_input_test(design_system: dict, version_info: dict) -> str:
    """Generate tests for Input component."""
    return """// Input.test.tsx — Generated by ui-craft
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe, toHaveNoViolations } from 'jest-axe'
import { Input } from './input'

expect.extend(toHaveNoViolations)

describe('Input', () => {
  it('renders correctly', () => {
    render(<Input placeholder="Enter text" />)
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument()
  })

  it('renders with label', () => {
    render(<Input label="Email" />)
    expect(screen.getByLabelText('Email')).toBeInTheDocument()
  })

  it('shows error state', () => {
    render(<Input label="Email" error="Invalid email" />)
    expect(screen.getByRole('alert')).toHaveTextContent('Invalid email')
    expect(screen.getByLabelText('Email')).toHaveAttribute('aria-invalid', 'true')
  })

  it('shows hint text', () => {
    render(<Input label="Password" hint="Must be at least 8 characters" />)
    expect(screen.getByText('Must be at least 8 characters')).toBeInTheDocument()
  })

  it('handles user input', async () => {
    const user = userEvent.setup()
    render(<Input placeholder="Type here" />)

    await user.type(screen.getByPlaceholderText('Type here'), 'Hello')
    expect(screen.getByPlaceholderText('Type here')).toHaveValue('Hello')
  })

  it('can be disabled', () => {
    render(<Input disabled placeholder="Disabled" />)
    expect(screen.getByPlaceholderText('Disabled')).toBeDisabled()
  })

  it('has no accessibility violations', async () => {
    const { container } = render(<Input label="Accessible Input" />)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
"""


def _generate_modal_test(design_system: dict, version_info: dict) -> str:
    """Generate tests for Modal component."""
    return """// Modal.test.tsx — Generated by ui-craft
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { axe, toHaveNoViolations } from 'jest-axe'
import { Modal } from './modal'

expect.extend(toHaveNoViolations)

describe('Modal', () => {
  it('renders when open', () => {
    render(
      <Modal open={true} onClose={() => {}}>
        <p>Modal content</p>
      </Modal>
    )
    expect(screen.getByRole('dialog')).toBeInTheDocument()
    expect(screen.getByText('Modal content')).toBeInTheDocument()
  })

  it('does not render when closed', () => {
    render(
      <Modal open={false} onClose={() => {}}>
        <p>Modal content</p>
      </Modal>
    )
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('calls onClose when Escape is pressed', async () => {
    const user = userEvent.setup()
    const onClose = vi.fn()
    render(
      <Modal open={true} onClose={onClose}>
        <p>Modal content</p>
      </Modal>
    )

    await user.keyboard('{Escape}')
    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it('calls onClose when clicking overlay', async () => {
    const user = userEvent.setup()
    const onClose = vi.fn()
    render(
      <Modal open={true} onClose={onClose}>
        <p>Modal content</p>
      </Modal>
    )

    await user.click(screen.getByRole('dialog'))
    expect(onClose).toHaveBeenCalledTimes(1)
  })

  it('has no accessibility violations', async () => {
    const { container } = render(
      <Modal open={true} onClose={() => {}}>
        <p>Accessible Modal</p>
      </Modal>
    )
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
"""


def _generate_navbar_test(design_system: dict, version_info: dict) -> str:
    """Generate tests for Navbar component."""
    return """// Navbar.test.tsx — Generated by ui-craft
import { render, screen } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { Navbar } from './navbar'

expect.extend(toHaveNoViolations)

const mockItems = [
  { label: 'Home', href: '/', active: true },
  { label: 'About', href: '/about' },
  { label: 'Contact', href: '/contact' },
]

describe('Navbar', () => {
  it('renders correctly', () => {
    render(<Navbar items={mockItems} logo="TestLogo" />)
    expect(screen.getByText('TestLogo')).toBeInTheDocument()
    expect(screen.getByText('Home')).toBeInTheDocument()
    expect(screen.getByText('About')).toBeInTheDocument()
    expect(screen.getByText('Contact')).toBeInTheDocument()
  })

  it('marks active item', () => {
    render(<Navbar items={mockItems} />)
    expect(screen.getByText('Home')).toHaveAttribute('aria-current', 'page')
  })

  it('has navigation landmark', () => {
    render(<Navbar items={mockItems} />)
    expect(screen.getByRole('navigation')).toBeInTheDocument()
  })

  it('has no accessibility violations', async () => {
    const { container } = render(<Navbar items={mockItems} />)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
"""


# ============ ICON LIBRARY INTEGRATION ============

def detect_icon_library(project_dir: str) -> str | None:
    """Detect which icon library is installed in the project."""
    import json
    pkg_path = Path(project_dir) / "package.json"
    if not pkg_path.exists():
        return None

    try:
        with open(pkg_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    except (json.JSONDecodeError, IOError):
        return None

    icon_libs = [
        "lucide-react",
        "@heroicons/react",
        "@phosphor-icons/react",
        "@tabler/icons-react",
        "react-icons",
    ]
    for lib in icon_libs:
        if lib in deps:
            return lib
    return None


def generate_icon_component(icon_name: str, icon_library: str, size: int = 24) -> str:
    """Generate an icon wrapper component."""
    if icon_library == "lucide-react":
        return f"""import {{ {icon_name} }} from 'lucide-react'
import {{ cn }} from '@/lib/utils'

interface IconProps {{
  className?: string
  size?: number
  'aria-label'?: string
}}

export function Icon({{ className, size = {size}, 'aria-label': ariaLabel, ...props }}: IconProps) {{
  return (
    <{icon_name}
      className={{cn("shrink-0", className)}}
      size={{size}}
      aria-hidden={{ariaLabel ? undefined : "true"}}
      role={{ariaLabel ? "img" : undefined}}
      aria-label={{ariaLabel}}
      {{...props}}
    />
  )
}}
"""
    elif icon_library == "@heroicons/react":
        return f"""import {{ {icon_name}Icon }} from '@heroicons/react/24/outline'
import {{ cn }} from '@/lib/utils'

interface IconProps {{
  className?: string
  size?: number
  'aria-label'?: string
}}

export function Icon({{ className, size = {size}, 'aria-label': ariaLabel, ...props }}: IconProps) {{
  return (
    <{icon_name}Icon
      className={{cn("shrink-0", className)}}
      width={{size}}
      height={{size}}
      aria-hidden={{ariaLabel ? undefined : "true"}}
      role={{ariaLabel ? "img" : undefined}}
      aria-label={{ariaLabel}}
      {{...props}}
    />
  )
}}
"""
    else:
        return f"""// Generic icon wrapper for {icon_library}
import {{ cn }} from '@/lib/utils'

interface IconProps {{
  className?: string
  size?: number
  'aria-label'?: string
}}

export function Icon({{ className, size = {size}, 'aria-label': ariaLabel, ...props }}: IconProps) {{
  return (
    <span
      className={{cn("inline-flex shrink-0 items-center justify-center", className)}}
      style={{{{ width: size, height: size }}}}
      aria-hidden={{ariaLabel ? undefined : "true"}}
      role={{ariaLabel ? "img" : undefined}}
      aria-label={{ariaLabel}}
      {{...props}}
    />
  )
}}
"""


# ============ SHADCN/UI INTEGRATION ============

def generate_shadcn_install_command(components: list[str]) -> str:
    """Generate shadcn/ui install command for a list of components."""
    if not components:
        return ""
    return f"npx shadcn@latest add {' '.join(components)}"


def generate_shadcn_theme_config(design_system: dict) -> str:
    """Generate shadcn/ui theme configuration."""
    colors = design_system.get("colors", {})
    return f"""// shadcn/ui theme configuration
// Generated by ui-craft
// Import this in your tailwind.config.ts or globals.css

import type {{ Config }} from "tailwindcss"

const config: Config = {{
  darkMode: ["class"],
  content: [
    "./pages/**/*.{{ts,tsx}}",
    "./components/**/*.{{ts,tsx}}",
    "./app/**/*.{{ts,tsx}}",
    "./src/**/*.{{ts,tsx}}",
  ],
  theme: {{
    container: {{
      center: true,
      padding: "2rem",
      screens: {{
        "2xl": "1400px",
      }},
    }},
    extend: {{
      colors: {{
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {{
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        }},
        secondary: {{
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        }},
        destructive: {{
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        }},
        muted: {{
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        }},
        accent: {{
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        }},
        popover: {{
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        }},
        card: {{
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        }},
      }},
      borderRadius: {{
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      }},
    }},
  }},
  plugins: [require("tailwindcss-animate")],
}}

export default config
"""


def generate_shadcn_globals_css(design_system: dict) -> str:
    """Generate shadcn/ui globals.css with CSS variables."""
    colors = design_system.get("colors", {})
    return f"""@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {{
  :root {{
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: {colors.get("primary", "#2563EB")};
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }}

  .dark {{
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }}
}}

@layer base {{
  * {{
    @apply border-border;
  }}
  body {{
    @apply bg-background text-foreground;
  }}
}}
"""
