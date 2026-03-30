import type { ButtonHTMLAttributes, PropsWithChildren } from 'react'

type Props = PropsWithChildren<ButtonHTMLAttributes<HTMLButtonElement> & { variant?: string; size?: string }>

export function Button({ children, className = '', ...props }: Props) {
  return <button className={`fab-btn ${className}`.trim()} {...props}>{children}</button>
}
