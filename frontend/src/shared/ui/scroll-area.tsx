import type { PropsWithChildren } from 'react'
export function ScrollArea({ children, className = '' }: PropsWithChildren<{ className?: string }>) { return <div className={className} style={{overflow:'auto', height:'100%'}}>{children}</div> }
