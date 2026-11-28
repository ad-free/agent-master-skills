#!/usr/bin/env bash
# Build both arms of the shadcn-orders fixture into $1 from a pinned shadcn-admin commit (MIT, satnaing).
#   $1/with-template : full shadcn-admin template, ugly Orders page added at /orders
#   $1/no-template   : same stack (React 19, Tailwind v4, shadcn/ui components, default theme), only the Orders page
#   $1/design-lock   : no-template + a locked DESIGN.md, theme tokens and approved list-pattern screenshots
set -euo pipefail
OUT=$(realpath -m "$1"); HERE=$(cd "$(dirname "$0")" && pwd)
SHA=${SHA:-5d9072d}
SRC=$OUT/.src
rm -rf "${OUT:?}/with-template" "${OUT:?}/no-template" "${OUT:?}/design-lock"; mkdir -p "$OUT"
[ -d "$SRC" ] || git clone -q https://github.com/satnaing/shadcn-admin.git "$SRC"
git -C "$SRC" fetch -q --depth 1 origin "$SHA" 2>/dev/null || true; git -C "$SRC" checkout -q "$SHA"

# Arm B: with template
W=$OUT/with-template; mkdir -p "$W"; (cd "$SRC" && git archive HEAD) | tar -x -C "$W"
mkdir -p "$W/src/features/orders" "$W/src/routes/_authenticated/orders"
cp "$HERE/orders/index.tsx" "$HERE/orders/data.ts" "$W/src/features/orders/"
cat > "$W/src/routes/_authenticated/orders/index.tsx" <<'TSX'
import { createFileRoute } from '@tanstack/react-router'
import { Orders } from '@/features/orders'

export const Route = createFileRoute('/_authenticated/orders/')({
  component: Orders,
})
TSX
cp "$HERE/orders/routeTree.gen.ts" "$W/src/routeTree.gen.ts"  # generated once at $SHA by the router plugin
# Sidebar entry right after Dashboard
python3 - "$W/src/components/layout/data/sidebar-data.ts" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
a="""          url: '/',
          icon: LayoutDashboard,
        },"""
assert s.count(a)==1
s=s.replace(a, a+"""
        {
          title: 'Orders',
          url: '/orders',
          icon: Package,
        },""")
open(p,'w').write(s)
PY
printf '# Northwind Supply admin\n\nInstall: `npm install`. Run: `npm run dev` (http://localhost:5173). The orders page is at /orders\n(`src/features/orders`). `src/features/orders/data.ts` mirrors the API; do not change it.\n' > "$W/README.md"

# Arm A: same stack, no template pages or layout
N=$OUT/no-template; mkdir -p "$N/src/features"
for f in package.json index.html tsconfig.json tsconfig.app.json tsconfig.node.json components.json eslint.config.js .prettierrc public; do
  [ -e "$W/$f" ] && cp -r "$W/$f" "$N/"; done
cp -r "$W/src/components" "$W/src/lib" "$W/src/hooks" "$W/src/styles" "$W/src/context" "$W/src/vite-env.d.ts" "$N/src/"
rm -rf "${N:?}/src/components/layout" "${N:?}/src/components/data-table"
find "$N/src/components" -maxdepth 1 -type f -delete
find "$N/src" -name '*.test.*' -delete
rm -f "${N:?}/src/context/font-provider.tsx" "${N:?}/src/context/search-provider.tsx"  # need template-only modules
cp -r "$W/src/features/orders" "$N/src/features/"
cat > "$N/src/main.tsx" <<'TSX'
import { StrictMode } from 'react'
import ReactDOM from 'react-dom/client'
import { Orders } from '@/features/orders'
import './styles/index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Orders />
  </StrictMode>
)
TSX
cat > "$N/vite.config.ts" <<'TS'
import path from 'path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } },
})
TS
printf '# Northwind Supply admin\n\nInstall: `npm install`. Run: `npm run dev` (http://localhost:5173). The orders page is the app root\n(`src/features/orders`). `src/features/orders/data.ts` mirrors the API; do not change it.\n' > "$N/README.md"
# Arm C: no-template + the design lock a designer (or the owner with the agent) would hand over
L=$OUT/design-lock; cp -r "$N" "$L"
cp "$HERE/design-lock/DESIGN.md" "$L/DESIGN.md"; cp "$HERE/design-lock/theme.css" "$L/src/styles/theme.css"
mkdir -p "$L/design"; cp "$HERE/design-lock/design/"*.png "$HERE/design-lock/design/list-pattern.html" "$L/design/"
printf '# Northwind Supply admin\n\nInstall: `npm install`. Run: `npm run dev` (http://localhost:5173). The orders page is the app root\n(`src/features/orders`). `src/features/orders/data.ts` mirrors the API; do not change it. Design: `DESIGN.md` (locked).\n' > "$L/README.md"
echo "built $W, $N and $L"
