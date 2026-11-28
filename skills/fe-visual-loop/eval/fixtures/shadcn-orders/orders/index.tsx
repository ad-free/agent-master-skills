import { useState } from 'react'
import { orders, type Order } from './data'

const money = (n: number) => '$' + n.toFixed(2)
const statusColor: Record<string, string> = { paid: 'green', shipped: 'green', pending: 'orange', refunded: 'red', cancelled: 'red' }
const btn = { background: '#1e73be', color: '#fff', border: 'none', padding: '6px 11px', margin: 2 }

export function Orders() {
  const [rows, setRows] = useState<Order[]>(orders)
  const [q, setQ] = useState('')
  const [status, setStatus] = useState('')

  const filter = () =>
    setRows(orders.filter((o) => (!status || o.status === status) &&
      (!q || (o.id + o.customer + o.email).toLowerCase().includes(q.toLowerCase()))))
  const revenue = orders.filter((o) => o.status !== 'refunded' && o.status !== 'cancelled').reduce((s, o) => s + o.amount, 0)

  return (
    <div style={{ padding: '17px 40px', fontFamily: 'Arial, sans-serif', fontSize: 14, color: '#333' }}>
      <h1 style={{ fontSize: 22, margin: '5px 0 20px 0' }}>Orders</h1>
      <div style={{ overflow: 'hidden', marginBottom: 30 }}>
        {[['Total orders', orders.length], ['Revenue', money(revenue)],
          ['Pending', orders.filter((o) => o.status === 'pending').length],
          ['Refunded', orders.filter((o) => o.status === 'refunded').length]].map(([label, v]) => (
          <div key={label} style={{ float: 'left', width: 250, border: '1px solid #000', padding: 12, marginRight: 15 }}>
            <div>{label}</div>
            <div style={{ fontSize: 18, color: '#1e73be', marginTop: 8 }}>{v}</div>
          </div>
        ))}
      </div>
      <div style={{ marginBottom: 12 }}>
        <input id='q' placeholder='search' value={q} onChange={(e) => setQ(e.target.value)} style={{ padding: 4, border: '1px solid #999' }} />
        <select id='status' value={status} onChange={(e) => setStatus(e.target.value)} style={{ padding: 4, border: '1px solid #999' }}>
          <option value=''>all</option>
          {['paid', 'pending', 'shipped', 'refunded', 'cancelled'].map((s) => <option key={s}>{s}</option>)}
        </select>
        <button id='go' style={btn} onClick={filter}>Search</button>
        <button style={btn}>Export CSV</button>
        <button style={btn}>New order</button>
      </div>
      <table style={{ width: 1100, borderCollapse: 'collapse' }}>
        <thead>
          <tr>{['ID', 'Date', 'Customer', 'Email', 'Items', 'Amount', 'Status', 'Actions'].map((h) => (
            <th key={h} style={{ background: '#eee', textAlign: 'left', padding: 6, border: '1px solid #ccc' }}>{h}</th>))}</tr>
        </thead>
        <tbody>
          {rows.map((o) => (
            <tr key={o.id}>
              {[o.id, o.date, o.customer, o.email, o.items, money(o.amount)].map((v, i) => (
                <td key={i} style={{ padding: 6, border: '1px solid #ccc' }}>{v}</td>))}
              <td style={{ padding: 6, border: '1px solid #ccc', color: statusColor[o.status] }}>{o.status}</td>
              <td style={{ padding: 6, border: '1px solid #ccc' }}>
                <button style={btn}>View</button><button style={btn}>Edit</button>
                <button style={btn} onClick={() => setRows(rows.filter((r) => r.id !== o.id))}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
