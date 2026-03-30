import type { HTMLAttributes } from 'react'

export function Separator(props: HTMLAttributes<HTMLSpanElement> & { orientation?: 'vertical' | 'horizontal' }) {
  return <span {...props} style={{ display: 'inline-block', width: 1, height: 16, background: 'rgba(255,255,255,0.15)', ...(props.style ?? {}) }} />
}
