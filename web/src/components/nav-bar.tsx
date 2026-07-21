import { NavLink } from 'react-router-dom'
import { Search, Sparkles, Workflow } from 'lucide-react'
import { cn } from '@/lib/utils'
import { ThemeToggle } from '@/components/theme-toggle'

const NAV_ITEMS = [
  { to: '/fuzzy', label: '模糊匹配', icon: Sparkles },
  { to: '/batch', label: '批量查询', icon: Search },
  { to: '/flow', label: '节点图', icon: Workflow },
] as const

export function NavBar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto flex h-14 max-w-screen-2xl items-center gap-6 px-6">
        <NavLink to="/batch" className="flex items-center gap-2 font-semibold tracking-tight">
          <span className="inline-flex size-7 items-center justify-center rounded bg-primary text-xs text-primary-foreground">
            CR
          </span>
          <span className="hidden sm:inline">跨系统一致性查询</span>
        </NavLink>

        <nav className="flex items-center gap-1 text-sm">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                cn(
                  'inline-flex items-center gap-1.5 rounded-md px-3 py-1.5 transition-colors',
                  isActive
                    ? 'bg-accent font-medium text-accent-foreground'
                    : 'text-muted-foreground hover:bg-accent/50 hover:text-foreground',
                )
              }
            >
              <Icon className="size-4" />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="flex-1" />
        <ThemeToggle />
      </div>
    </header>
  )
}
