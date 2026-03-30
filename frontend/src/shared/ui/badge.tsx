import type { PropsWithChildren } from 'react'

export function Badge({ children, className = '' }: PropsWithChildren<{ className?: string; variant?: string }>) {
  return <span className={className}>{children}</span>
}
