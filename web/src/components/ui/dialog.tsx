"use client"

import * as React from "react"
import { Dialog } from "radix-ui"
import { cn } from "@/lib/utils"
import { XIcon } from "lucide-react"

function DialogContent({
    className,
    children,
    ...props
}: React.ComponentProps<typeof Dialog.Content>) {
    return (
        <Dialog.Portal>
            <Dialog.Overlay className="fixed inset-0 z-50 bg-black/50 data-open:animate-in data-closed:animate-out data-closed:fade-out-0 data-open:fade-in-0" />
            <Dialog.Content
                className={cn(
                    "fixed left-1/2 top-1/2 z-50 grid w-full max-w-3xl -translate-x-1/2 -translate-y-1/2 gap-4 rounded-lg bg-card p-6 shadow-lg ring-1 ring-foreground/10 duration-200 data-open:animate-in data-closed:animate-out data-closed:fade-out-0 data-open:fade-in-0 data-closed:zoom-out-95 data-open:zoom-in-95",
                    className
                )}
                {...props}
            >
                {children}
                <Dialog.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2">
                    <XIcon className="size-4" />
                    <span className="sr-only">关闭</span>
                </Dialog.Close>
            </Dialog.Content>
        </Dialog.Portal>
    )
}

function DialogHeader({ className, ...props }: React.ComponentProps<"div">) {
    return <div className={cn("flex flex-col gap-1.5", className)} {...props} />
}

function DialogTitle({ className, ...props }: React.ComponentProps<typeof Dialog.Title>) {
    return (
        <Dialog.Title
            className={cn("text-sm font-semibold", className)}
            {...props}
        />
    )
}

function DialogDescription({ className, ...props }: React.ComponentProps<typeof Dialog.Description>) {
    return (
        <Dialog.Description
            className={cn("text-xs text-muted-foreground", className)}
            {...props}
        />
    )
}

export { DialogContent, DialogHeader, DialogTitle, DialogDescription }
