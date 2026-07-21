"use client"

import { useSyncExternalStore } from "react"
import { useTheme } from "next-themes"
import { MoonIcon, SunIcon } from "lucide-react"
import { Button } from "@/components/ui/button"

function useMounted() {
    return useSyncExternalStore(
        () => () => {},
        () => true,
        () => false
    )
}

export function ThemeToggle() {
    const { resolvedTheme, setTheme } = useTheme()
    const mounted = useMounted()
    const isDark = resolvedTheme === "dark"

    // 服务端和客户端始终渲染相同 DOM 结构（Button + 图标），
    // mounted 仅影响图标内容，suppressHydrationWarning 消除内容差异警告。
    return (
        <Button variant="ghost" size="icon" onClick={() => setTheme(isDark ? "light" : "dark")} aria-label="切换主题" suppressHydrationWarning>
            {mounted && isDark ? <SunIcon className="size-4" /> : <MoonIcon className="size-4" />}
        </Button>
    )
}
