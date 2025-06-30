import { useEffect, useState } from 'react';
import { Cake } from 'lucide-react';
import api from '../api';

export default function Birthdays() {
  const [list, setList] = useState([]);

  async function load() {
    try {
      const res = await api.get('birthdays/');
      setList(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    load();
    window.refreshPage = load;
  }, []);

  function formatDate(dateStr) {
    if (!dateStr) return 'Неверная дата';
    let date = new Date(dateStr);
    if (isNaN(date)) {
      const parts = dateStr.split('.');
      if (parts.length === 3) {
        const [d, m, y] = parts;
        date = new Date(`${y}-${m}-${d}`);
      }
    }
    if (isNaN(date)) {
      return 'Неверная дата';
    }
    return date.toLocaleDateString('ru-RU');
  }

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-semibold tracking-tight text-gray-800 flex items-center gap-2">
        <Cake size={24} /> Ближайшие дни рождения
      </h2>
      <button className="bg-blue-600 text-white px-3 py-2 rounded" onClick={load}>
        Обновить
      </button>
      {list.length === 0 && (
        <p className="text-gray-500 italic">Нет сотрудников с ближайшими днями рождения.</p>
      )}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {list.map((b) => (
          <div
            key={b.id}
            className="bg-white p-4 rounded-lg shadow border hover:bg-gray-50 transition"
          >
            <div className="text-lg font-medium text-gray-800">{b.full_name}</div>
            <div className="text-sm text-gray-600 mt-1">🎂 {formatDate(b.birthdate)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
