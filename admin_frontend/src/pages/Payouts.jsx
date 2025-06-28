import api from '../api';
  const [employees, setEmployees] = useState([]);
  const emptyForm = {
    id: null,
    user_id: '',
    name: '',
    phone: '',
    bank: '',
    amount: '',
    payout_type: 'Аванс',
    method: '💳 На карту',
    status: 'Ожидает',
    sync_to_bot: false,
  };
  const [formData, setFormData] = useState(emptyForm);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState('');
  const [employeeFilter, setEmployeeFilter] = useState('');
  const [period, setPeriod] = useState('');
  const [status, setStatus] = useState('');
  const [type, setType] = useState('');
  const [method, setMethod] = useState('');
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');
  const [selected, setSelected] = useState([]);
    loadEmployees();
    try {
      const params = {
        payout_type: type || undefined,
        status: status || undefined,
        method: method || undefined,
      };
      if (employeeFilter) params.employee_id = employeeFilter;
      if (period !== 'lastSalary') {
        params.from_date = fromDate || undefined;
        params.to_date = toDate || undefined;
      }
      const res = await api.get('payouts/', { params });
      setPayouts(res.data);
    } catch (err) {
      console.error(err);
    }
  async function loadEmployees() {
    try {
      const res = await api.get('employees/');
      setEmployees(res.data);
    } catch (err) {
      console.error(err);
    }
  }

    try {
      await api.put(`payouts/${id}/status`, { status: 'Одобрено' });
      load();
    } catch (err) {
      console.error(err);
    }
    try {
      await api.put(`payouts/${id}/status`, { status: 'Отказано' });
      load();
    } catch (err) {
      console.error(err);
    }
  }

  async function markPaid(id) {
    try {
      await api.put(`payouts/${id}/status`, { status: 'Выплачен' });
      load();
    } catch (err) {
      console.error(err);
    }
  function handleSelect(id) {
    const emp = employees.find((e) => String(e.id) === id);
    if (emp) {
      setFormData((f) => ({
        ...f,
        user_id: emp.id,
        name: emp.name,
        phone: emp.phone || '',
        bank: emp.bank || emp.card_number || '',
      }));
    }
  }

  async function saveForm() {
    try {
      const payload = {
        ...formData,
        amount: Number(formData.amount || 0),
      };
      if (formData.id) {
        await api.put(`payouts/${formData.id}`, payload);
      } else {
        await api.post('payouts/', payload);
      }
      setShowForm(false);
      setFormData(emptyForm);
      load();
    } catch (err) {
      console.error(err);
      alert('Ошибка при сохранении выплаты');
    }
  }

  function toggleSelect(id, checked) {
    setSelected((prev) =>
      checked ? [...prev, id] : prev.filter((x) => x !== id)
    );
  }

  async function deleteSelected() {
    if (!selected.length) return;
    if (!window.confirm('Удалить выбранные выплаты?')) return;
    try {
      await api.delete('payouts/', { params: { ids: selected.join(',') } });
      setSelected([]);
      load();
    } catch (err) {
      console.error(err);
    }
  }

  const lastSalary = {};
  payouts.forEach((p) => {
    if (
      p.payout_type === 'Зарплата' &&
      ['Одобрено', 'Выплачен'].includes(p.status)
    ) {
      const ts = new Date(p.timestamp);
      const id = String(p.user_id);
      if (!lastSalary[id] || ts > lastSalary[id]) lastSalary[id] = ts;
    }
  });

  const filtered = payouts.filter((p) => {
    if (
      !(p.name?.toLowerCase().includes(filter.toLowerCase()) ||
        String(p.user_id).includes(filter))
    )
      return false;
    if (employeeFilter && String(p.user_id) !== employeeFilter) return false;
    if (status && p.status !== status) return false;
    if (type && p.payout_type !== type) return false;
    if (method && p.method !== method) return false;
    const ts = p.timestamp ? new Date(p.timestamp) : null;
    if (period === 'lastSalary') {
      if (p.payout_type !== 'Аванс') return false;
      const last = lastSalary[String(p.user_id)];
      if (last && ts && ts <= last) return false;
    } else {
      if (fromDate && ts && ts < new Date(fromDate)) return false;
      if (toDate && ts && ts > new Date(toDate)) return false;
    }
    return true;
  });

  const totalAmount = filtered.reduce((sum, p) => sum + Number(p.amount || 0), 0);
  const totalCount = filtered.length;

      <div className="flex gap-2">
        <button
          className="bg-green-600 text-white px-3 py-2 rounded"
          onClick={() => {
            setFormData(emptyForm);
            setShowForm(true);
          }}
        >
          Добавить выплату
        </button>
        <button
          className="bg-red-600 text-white px-3 py-2 rounded disabled:opacity-50"
          disabled={!selected.length}
          onClick={deleteSelected}
        >
          🗑 Удалить выбранные
        </button>
      </div>
      <div className="flex flex-wrap gap-2 items-end">
        <input
          className="border p-2 flex-grow"
          placeholder="Поиск"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
        <select
          className="border p-2"
          value={employeeFilter}
          onChange={(e) => setEmployeeFilter(e.target.value)}
        >
          <option value="">Все сотрудники</option>
          {employees.map((e) => (
            <option key={e.id} value={e.id}>
              {e.name}
            </option>
          ))}
        </select>
        <select
          className="border p-2"
          value={type}
          onChange={(e) => setType(e.target.value)}
        >
          <option value="">Все типы</option>
          <option value="Аванс">Аванс</option>
          <option value="Зарплата">Зарплата</option>
        </select>
        <select
          className="border p-2"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        >
          <option value="">Все статусы</option>
          <option value="Одобрено">Одобрено</option>
          <option value="Отказано">Отклонено</option>
          <option value="Ожидает">Ожидает</option>
          <option value="Выплачен">Выплачен</option>
        </select>
        <select
          className="border p-2"
          value={method}
          onChange={(e) => setMethod(e.target.value)}
        >
          <option value="">Все способы</option>
          <option value="💳 На карту">На карту</option>
          <option value="💵 Из кассы">Из кассы</option>
        </select>
        <select
          className="border p-2"
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
        >
          <option value="">Произвольный период</option>
          <option value="lastSalary">С последней ЗП</option>
        </select>
        <input
          type="date"
          className="border p-2"
          value={fromDate}
          onChange={(e) => setFromDate(e.target.value)}
          disabled={period === 'lastSalary'}
        />
        <input
          type="date"
          className="border p-2"
          value={toDate}
          onChange={(e) => setToDate(e.target.value)}
          disabled={period === 'lastSalary'}
        />
        <button className="bg-blue-600 text-white px-3 py-2 rounded" onClick={load}>Обновить</button>
        <a
          className="bg-gray-600 text-white px-3 py-2 rounded"
          href={`/api/payouts/export.pdf?payout_type=${type}&status=${status}&method=${method}&employee_id=${employeeFilter}&from_date=${period==='lastSalary'?'':fromDate}&to_date=${period==='lastSalary'?'':toDate}`}
          target="_blank"
        >
          PDF
        </a>
      </div>
              <th className="p-2"></th>
              <th className="p-2 text-left">Метод</th>
              <th className="p-2 text-left">Телефон / Банк</th>
              <th className="p-2 text-left">Статус</th>
              <th className="p-2 text-left">Дата</th>
              <th className="p-2 text-left">user_id</th>
            {Array.isArray(filtered) &&
              filtered.map((p) => (
                  <td className="p-2">
                    <input
                      type="checkbox"
                      checked={selected.includes(String(p.id))}
                      onChange={(e) =>
                        toggleSelect(String(p.id), e.target.checked)
                      }
                    />
                  </td>
                  <td className="p-2">{p.method}</td>
                  <td className="p-2">
                    {p.method === '💳 На карту' ? `${p.phone} / ${p.bank}` : '—'}
                  </td>
                  <td className="p-2">{p.status}</td>
                  <td className="p-2">{p.timestamp}</td>
                  <td className="p-2">{p.user_id}</td>
                    <button
                      className="text-blue-600"
                      onClick={() => {
                        setFormData({ ...p, id: p.id });
                        setShowForm(true);
                      }}
                    >
                      ✏️
                    </button>
                    {p.status === 'Одобрено' && (
                      <button className="text-blue-600" onClick={() => markPaid(p.id)}>
                        Выплачен
                      </button>
                    )}
      <div>
        Всего: {totalCount} заявок на сумму {totalAmount} ₽
      </div>
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-4 space-y-2 rounded shadow w-80">
            <h2 className="text-lg font-bold mb-2">{formData.id ? 'Редактирование' : 'Новая выплата'}</h2>
            <select className="border p-2 w-full" value={formData.user_id} onChange={(e) => handleSelect(e.target.value)}>
              <option value="">Сотрудник</option>
              {employees.map((e) => (
                <option key={e.id} value={e.id}>
                  {e.name}
                </option>
              ))}
            </select>
            <input className="border p-2 w-full" placeholder="Сумма" value={formData.amount} onChange={(e) => setFormData({ ...formData, amount: e.target.value })} />
            <select className="border p-2 w-full" value={formData.payout_type} onChange={(e) => setFormData({ ...formData, payout_type: e.target.value })}>
              <option value="Аванс">Аванс</option>
              <option value="Зарплата">Зарплата</option>
            </select>
            <select className="border p-2 w-full" value={formData.method} onChange={(e) => setFormData({ ...formData, method: e.target.value })}>
              <option value="💳 На карту">На карту</option>
              <option value="💵 Из кассы">Из кассы</option>
            </select>
            <input className="border p-2 w-full" placeholder="Телефон" value={formData.phone} onChange={(e) => setFormData({ ...formData, phone: e.target.value })} />
            <input className="border p-2 w-full" placeholder="Банк" value={formData.bank} onChange={(e) => setFormData({ ...formData, bank: e.target.value })} />
            <select className="border p-2 w-full" value={formData.status} onChange={(e) => setFormData({ ...formData, status: e.target.value })}>
              <option value="Ожидает">Ожидает</option>
              <option value="Одобрено">Одобрено</option>
              <option value="Отказано">Отказано</option>
              <option value="Выплачен">Выплачен</option>
            </select>
            <label className="flex items-center gap-1 text-sm">
              <input type="checkbox" checked={formData.sync_to_bot} onChange={(e) => setFormData({ ...formData, sync_to_bot: e.target.checked })} />
              Отразить в боте
            </label>
            <div className="flex justify-end space-x-2 pt-2">
              <button className="bg-gray-300 px-3 py-1 rounded" onClick={() => { setShowForm(false); setFormData(emptyForm); }}>Отмена</button>
              <button className="bg-blue-600 text-white px-3 py-1 rounded" onClick={saveForm}>Сохранить</button>
            </div>
          </div>
        </div>
      )}
    load();
  }, []);

  async function load() {
    const res = await axios.get('/api/payouts');
    setPayouts(res.data);
  }

  async function approve(id) {
    await axios.put(`/api/payouts/${id}`, { status: 'approved' });
    load();
  }

  async function reject(id) {
    await axios.put(`/api/payouts/${id}`, { status: 'rejected' });
    load();
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <h2 className="text-2xl font-semibold tracking-tight text-gray-800">Запросы на выплаты</h2>

      <div className="overflow-auto border rounded shadow">
        <table className="min-w-full divide-y divide-gray-200 bg-white text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-gray-600 font-medium">Сотрудник</th>
              <th className="px-4 py-3 text-left text-gray-600 font-medium">Сумма</th>
              <th className="px-4 py-3 text-left text-gray-600 font-medium">Тип</th>
              <th className="px-4 py-3 text-left text-gray-600 font-medium">Действия</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {payouts.map((p) => (
              <tr key={p.id} className="hover:bg-gray-50">
                <td className="px-4 py-2">{p.name}</td>
                <td className="px-4 py-2 text-blue-800 font-medium">{p.amount} ₽</td>
                <td className="px-4 py-2 capitalize">{p.payout_type}</td>
                <td className="px-4 py-2 space-x-2">
                  <button
                    onClick={() => approve(p.id)}
                    className="inline-flex items-center text-green-600 hover:text-green-800"
                    title="Одобрить"
                  >
                    <CheckCircle size={18} className="mr-1" /> Одобрить
                  </button>
                  <button
                    onClick={() => reject(p.id)}
                    className="inline-flex items-center text-red-600 hover:text-red-800"
                    title="Отклонить"
                  >
                    <XCircle size={18} className="mr-1" /> Отклонить
                  </button>
                </td>
              </tr>
            ))}
            {payouts.length === 0 && (
              <tr>
                <td colSpan="4" className="px-4 py-3 text-center text-gray-500 italic">
                  Нет активных запросов на выплаты
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
