interface BadgeProps {
  label: string
  variant: 'success' | 'warning' | 'danger' | 'info' | 'neutral'
}

const styles: Record<BadgeProps['variant'], { bg: string; color: string }> = {
  success: { bg: 'var(--success-bg)', color: 'var(--success)' },
  warning: { bg: 'var(--warning-bg)', color: 'var(--warning)' },
  danger:  { bg: 'var(--danger-bg)',  color: 'var(--danger)' },
  info:    { bg: 'var(--accent-light)', color: 'var(--accent)' },
  neutral: { bg: '#f1f5f9', color: '#64748b' },
}

export default function Badge({ label, variant }: BadgeProps) {
  const s = styles[variant]
  return (
    <span style={{
      display: 'inline-block',
      padding: '2px 10px',
      borderRadius: 999,
      fontSize: 12,
      fontWeight: 600,
      background: s.bg,
      color: s.color,
    }}>
      {label}
    </span>
  )
}
