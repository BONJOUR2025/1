import { useState } from 'react';
import api from '../api';

export default function EmployeeForm({ mode = 'create', initialData, onClose, onSaved }) {
  const [form, setForm] = useState(
    initialData || {
      name: '',
      full_name: '',
      phone: '',
      card_number: '',
      bank: '',
      birthdate: '',
      note: '',
      status: 'active',
      position: '',
      is_admin: false,
      sync_to_bot: false,
    }
  );
  const [file, setFile] = useState(null);
  const [errors, setErrors] = useState({});

  function handleChange(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  function validate() {
    const err = {};
    if (!form.name.trim()) err.name = 'Обязательное поле';
    if (!form.phone.trim()) err.phone = 'Обязательное поле';
    if (!form.birthdate) err.birthdate = 'Обязательное поле';
    if (!form.status) err.status = 'Обязательное поле';
    setErrors(err);
    return Object.keys(err).length === 0;
  }

  async function submit() {
    if (!validate()) return;
    const payload = {
      name: form.name,
      full_name: form.full_name,
      phone: form.phone,
      card_number: form.card_number || '',
      bank: form.bank || '',
      birthdate: form.birthdate || null,
      note: form.note || '',
      status: form.status,
      position: form.position || '',
      is_admin: !!form.is_admin,
    };
    try {
      let id = form.id;
      if (mode === 'edit' && id) {
        await api.put(`employees/${id}`, payload);
      } else {
        const res = await api.post('employees/', payload);
        id = res.data.id;
      }
      if (file) {
        const fd = new FormData();
        fd.append('file', file);
        await api.post(`employees/${id}/photo`, fd);
      }
      if (onSaved) onSaved();
      onClose();
    } catch (err) {
      console.error(err);
      alert('Ошибка при сохранении');
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-4 space-y-2 rounded shadow w-80">
        <h2 className="text-lg font-bold mb-2">
          {mode === 'edit' ? 'Редактировать сотрудника' : 'Добавить сотрудника'}
        </h2>
        <input
          className="border p-2 w-full"
          placeholder="Имя"
          value={form.name}
          onChange={(e) => handleChange('name', e.target.value)}
        />
        {errors.name && <div className="text-red-600 text-sm">{errors.name}</div>}
        <input
          className="border p-2 w-full"
          placeholder="ФИО"
          value={form.full_name}
          onChange={(e) => handleChange('full_name', e.target.value)}
        />
        <input
          className="border p-2 w-full"
          placeholder="Телефон"
          value={form.phone}
          onChange={(e) => handleChange('phone', e.target.value)}
        />
        {errors.phone && <div className="text-red-600 text-sm">{errors.phone}</div>}
        <input
          className="border p-2 w-full"
          placeholder="Номер карты"
          value={form.card_number}
          onChange={(e) => handleChange('card_number', e.target.value)}
        />
        <input
          className="border p-2 w-full"
          placeholder="Банк"
          value={form.bank}
          onChange={(e) => handleChange('bank', e.target.value)}
        />
        <input
          className="border p-2 w-full"
          placeholder="Должность"
          value={form.position}
          onChange={(e) => handleChange('position', e.target.value)}
        />
        <input
          type="date"
          className="border p-2 w-full"
          value={form.birthdate}
          onChange={(e) => handleChange('birthdate', e.target.value)}
        />
        {errors.birthdate && <div className="text-red-600 text-sm">{errors.birthdate}</div>}
        <textarea
          className="border p-2 w-full"
          placeholder="Заметка"
          value={form.note}
          onChange={(e) => handleChange('note', e.target.value)}
        />
        <select
          className="border p-2 w-full"
          value={form.status}
          onChange={(e) => handleChange('status', e.target.value)}
        >
          <option value="active">active</option>
          <option value="inactive">inactive</option>
        </select>
        {errors.status && <div className="text-red-600 text-sm">{errors.status}</div>}
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={form.sync_to_bot}
            onChange={(e) => handleChange('sync_to_bot', e.target.checked)}
          />
          Отразить в боте
        </label>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={form.is_admin}
            onChange={(e) => handleChange('is_admin', e.target.checked)}
          />
          Администратор
        </label>
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <div className="flex justify-end gap-2 pt-2">
          <button className="bg-gray-300 px-3 py-1 rounded-xl" onClick={onClose}>Отмена</button>
          <button className="bg-blue-600 text-white px-3 py-1 rounded-xl" onClick={submit}>Сохранить</button>
        </div>
      </div>
    </div>
  );
}
