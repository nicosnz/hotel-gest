import type { ReactNode } from 'react'

interface Column<T> {
  key: keyof T | string
  header: string
  render?: (row: T) => ReactNode
}

interface TableProps<T> {
  columns: Column<T>[]
  data: T[]
}

export default function Table<T extends { id: string | number }>({ columns, data }: TableProps<T>) {
  return (
    <div style={{
      background: 'var(--card-bg)',
      borderRadius: 'var(--radius)',
      boxShadow: 'var(--shadow)',
      overflow: 'hidden',
      border: '1px solid var(--border)',
    }}>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#f8fafc', borderBottom: '1px solid var(--border)' }}>
              {columns.map((col) => (
                <th
                  key={String(col.key)}
                  style={{
                    padding: '12px 16px',
                    textAlign: 'left',
                    fontSize: 12,
                    fontWeight: 600,
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                    color: 'var(--text-secondary)',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr
                key={row.id}
                style={{
                  borderBottom: i < data.length - 1 ? '1px solid var(--border)' : 'none',
                  transition: 'background 0.1s',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.background = '#f8fafc')}
                onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
              >
                {columns.map((col) => (
                  <td
                    key={String(col.key)}
                    style={{
                      padding: '14px 16px',
                      fontSize: 14,
                      color: 'var(--text-primary)',
                    }}
                  >
                    {col.render
                      ? col.render(row)
                      : String((row as Record<string, unknown>)[String(col.key)] ?? '')}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
