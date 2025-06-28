import { useEffect, useState } from 'react';
import axios from 'axios';
import { CheckCircle, XCircle } from 'lucide-react';

export default function Payouts() {
  const [payouts, setPayouts] = useState([]);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      const res = await axios.get('/api/payouts');
      setPayouts(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  async function approve(id) {
    try {
      await axios.put(`/api/payouts/${id}`, { status: 'approved' });
      load();
    } catch (err) {
      console.error(err);
    }
  }

  async function reject(id) {
    try {
      await axios.put(`/api/payouts/${id}`, { status: 'rejected' });
      load();
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <h2 className="text-2xl font-semibold tracking-tight text-gray-800">
        Запросы на выплаты
      </h2>

      <div className="overflow-auto border rounded shadow">
        <table className="min-w-full divide-y divide-gray-200 bg-white text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-gray-600 font-medium">
                Сотрудник
              </th>
              <th className="px-4 py-3 text-left text-gray-600 font-medium">
                Сумма
              </th>
              <th className="px-4 py-3 text-left text-gray-600 font-medium">Тип</th>
              <th className="px-4 py-3 text-left text-gray-600 font-medium">
                Действия
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {payouts.map((p) => (
              <tr key={p.id} className="hover:bg-gray-50">
                <td className="px-4 py-2">{p.name}</td>
                <td className="px-4 py-2 text-blue-800 font-medium">
                  {p.amount} ₽
                </td>
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
                <td
                  colSpan="4"
                  className="px-4 py-3 text-center text-gray-500 italic"
                >
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
