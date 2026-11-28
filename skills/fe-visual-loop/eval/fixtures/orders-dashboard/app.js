function money(n) { return '$' + n.toFixed(2); }

function render(rows) {
  var tb = document.querySelector('#orders tbody');
  tb.innerHTML = '';
  rows.forEach(function (o) {
    var tr = document.createElement('tr');
    tr.innerHTML = '<td>' + o.id + '</td><td>' + o.date + '</td><td>' + o.customer + '</td><td>' + o.email +
      '</td><td>' + o.items + '</td><td>' + money(o.amount) + '</td><td class="st-' + o.status + '">' + o.status +
      '</td><td><button>View</button><button>Edit</button><button class="del">Delete</button></td>';
    tr.querySelector('.del').onclick = function () { tr.remove(); };
    tb.appendChild(tr);
  });
}

function kpis(rows) {
  document.getElementById('k-count').textContent = rows.length;
  document.getElementById('k-rev').textContent = money(rows.filter(function (o) { return o.status !== 'refunded' && o.status !== 'cancelled'; })
    .reduce(function (s, o) { return s + o.amount; }, 0));
  document.getElementById('k-pending').textContent = rows.filter(function (o) { return o.status === 'pending'; }).length;
  document.getElementById('k-refund').textContent = rows.filter(function (o) { return o.status === 'refunded'; }).length;
}

function filter() {
  var q = document.getElementById('q').value.toLowerCase();
  var st = document.getElementById('status').value;
  render(window.ORDERS.filter(function (o) {
    return (!st || o.status === st) && (!q || (o.id + o.customer + o.email).toLowerCase().indexOf(q) >= 0);
  }));
}

document.getElementById('go').onclick = filter;
kpis(window.ORDERS);
render(window.ORDERS);
