import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Download, BarChartBig } from 'lucide-react';
import api from '../api';

export default function Reports() {
  const [employees, setEmployees] = useState([]);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadEmployees();
  }, []);

  async function loadEmployees() {
    try {
      const res = await api.get('employees/');
      setEmployees(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  async function load() {
    setLoading(true);
    try {
      const res = await axios.get('/api/analytics/sales');
      setData(res.data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-semibold tracking-tight text-gray-800 flex items-center gap-2">
        <BarChartBig size={24} /> Отчёты по продажам
      </h2>

      <div className="overflow-x-auto shadow rounded bg-white">
        <table className="min-w-full text-sm table-auto">
          <thead className="bg-gray-200">
            <tr>
              <th className="p-2 text-left">Сотрудник</th>
              <th className="p-2 text-left">PDF профиль</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(employees) &&
              employees.map((e) => (
                <tr key={e.id} className="border-b odd:bg-gray-50">
                  <td className="p-2">{e.name}</td>
                  <td className="p-2">
                    <a
                      className="text-blue-600"
                      href={`/api/employees/${e.id}/profile.pdf`}
                    >
                      Скачать
                    </a>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      <div className="flex flex-wrap gap-3">
        <button
          onClick={load}
          disabled={loading}
          className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded shadow hover:bg-blue-700 disabled:opacity-50"
        >
          📊 Загрузить аналитику
        </button>
        <a
          href="/api/salary/report"
          className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded shadow hover:bg-green-700"
        >
          <Download size={16} /> Скачать отчёт (PDF)
        </a>
      </div>

      {data && (
        <div className="bg-gray-100 p-4 rounded-lg border">
          <h3 className="text-lg font-medium text-gray-700 mb-2">Результаты:</h3>
          <ul className="space-y-1 text-gray-800">
            <li>💰 Сумма по ремонту: <strong>{data.repair_sum} ₽</strong></li>
            <li>🔧 Кол-во услуг по ремонту: <strong>{data.repair_count}</strong></li>
            <li>🧴 Сумма по косметике: <strong>{data.cosmetics_sum} ₽</strong></li>
            <li>📦 Кол-во товаров: <strong>{data.cosmetics_count}</strong></li>
            <li className="text-sm text-gray-500 mt-2">Обновлено: {new Date(data.updated_at).toLocaleString()}</li>
          </ul>
        </div>
      )}

      {!data && <p className="text-gray-500 italic">Аналитика пока не загружена.</p>}
    </div>
  );
}
