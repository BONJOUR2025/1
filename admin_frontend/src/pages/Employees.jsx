import { useState, useEffect } from 'react';
import {
  UserPlus,
  Trash2,
  Pencil,
  Camera,
  FileDown,
} from 'lucide-react';
import api from '../api';
import EmployeeForm from '../components/EmployeeForm';

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [filterName, setFilterName] = useState('');
  const [filterPhone, setFilterPhone] = useState('');
  const [selected, setSelected] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formMode, setFormMode] = useState('create');
  const [current, setCurrent] = useState(null);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      const res = await api.get('employees/');
      setEmployees(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  function formatDateRu(value) {
    if (!value) return '';
    return new Date(value).toLocaleDateString('ru-RU');
  }

  function startCreate() {
    setFormMode('create');
    setCurrent(null);
    setShowForm(true);
  }

  function startEdit(emp) {
    setFormMode('edit');
    setCurrent(emp);
    setShowForm(true);
  }

  function toggleSelect(id, checked) {
    setSelected((prev) => (checked ? [...prev, id] : prev.filter((x) => x !== id)));
  }

  async function deleteSelected() {
    if (!selected.length) return;
    if (!window.confirm('Удалить выбранных сотрудников?')) return;
    for (const id of selected) {
      await api.delete(`employees/${id}`);
    }
    setSelected([]);
    load();
  }


  const filtered = employees.filter(
    (e) =>
      e.full_name.toLowerCase().includes(filterName.toLowerCase()) &&
      e.phone.toLowerCase().includes(filterPhone.toLowerCase())
  );

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <h2 className="text-2xl font-semibold">Сотрудники</h2>
      <div className="flex flex-wrap gap-2 items-center">
        <input
          className="border p-2 flex-grow"
          placeholder="Фильтр по ФИО"
          value={filterName}
          onChange={(e) => setFilterName(e.target.value)}
        />
        <input
          className="border p-2 flex-grow"
          placeholder="Фильтр по телефону"
          value={filterPhone}
          onChange={(e) => setFilterPhone(e.target.value)}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded-xl flex items-center gap-1"
          onClick={startCreate}
        >
          <UserPlus size={16} /> Добавить сотрудника
        </button>
        <button
          className="bg-red-600 text-white px-4 py-2 rounded-xl flex items-center gap-1 disabled:opacity-50"
          disabled={!selected.length}
          onClick={deleteSelected}
        >
          <Trash2 size={16} /> Удалить выбранных
        </button>
      </div>
      <div className="overflow-auto border rounded shadow bg-white">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="p-2"></th>
              <th className="p-2 text-left">ID</th>
              <th className="p-2 text-left">Фото</th>
              <th className="p-2 text-left">Имя</th>
              <th className="p-2 text-left">ФИО</th>
              <th className="p-2 text-left">Телефон</th>
              <th className="p-2 text-left">День рождения</th>
              <th className="p-2 text-left">Должность</th>
              <th className="p-2 text-left">Роль</th>
              <th className="p-2 text-left">Создан</th>
              <th className="p-2"></th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {filtered.map((e) => (
              <tr
                key={e.id}
                className={`${e.is_admin ? 'bg-orange-50' : ''} ${
                  e.status !== 'active' ? 'bg-neutral-100' : ''
                }`}
              >
                <td className="p-2">
                  <input
                    type="checkbox"
                    checked={selected.includes(e.id)}
                    onChange={(ev) => toggleSelect(e.id, ev.target.checked)}
                  />
                </td>
                <td className="p-2">{e.id}</td>
                <td className="p-2">
                  {e.photo_url ? (
                    <img
                      src={e.photo_url}
                      alt=""
                      className="w-8 h-8 rounded-full object-cover cursor-pointer"
                      onClick={() => window.open(e.photo_url, '_blank')}
                    />
                  ) : (
                    <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                      <Camera size={14} className="text-gray-500" />
                    </div>
                  )}
                </td>
                <td className="p-2">{e.name}</td>
                <td className="p-2">{e.full_name}</td>
                <td className="p-2">{e.phone}</td>
                <td className="p-2">{formatDateRu(e.birthdate)}</td>
                <td className="p-2">{e.position}</td>
                <td className="p-2">{e.is_admin ? 'Админ' : 'Пользователь'}</td>
                <td className="p-2">{new Date(e.created_at).toLocaleDateString()}</td>
                <td className="p-2 text-right">
                  <button className="text-blue-600" onClick={() => startEdit(e)}>
                    <Pencil size={16} />
                  </button>
                  <a
                    href={`/api/employees/${e.id}/profile.pdf`}
                    className="text-gray-600 ml-2"
                    title="Скачать PDF"
                  >
                    <FileDown size={16} />
                  </a>
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan="11" className="p-4 text-center text-gray-500">
                  Нет сотрудников
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {showForm && (
        <EmployeeForm
          mode={formMode}
          initialData={current}
          onClose={() => setShowForm(false)}
          onSaved={load}
        />
      )}
    </div>
  );
}

