import { useEffect, useState } from 'react';

const initialUsers = [
  { id: 1, nombre: 'Ana Gómez', email: 'ana@sigam.com', rol: 'Administrador' },
  { id: 2, nombre: 'Carlos Ruiz', email: 'carlos@sigam.com', rol: 'Operador' }
];

const emptyForm = {
  nombre: '',
  email: '',
  rol: 'Operador'
};

function App() {
  const [usuarios, setUsuarios] = useState(() => {
    const savedUsers = localStorage.getItem('sigam-usuarios');
    return savedUsers ? JSON.parse(savedUsers) : initialUsers;
  });

  const [form, setForm] = useState(emptyForm);

  useEffect(() => {
    localStorage.setItem('sigam-usuarios', JSON.stringify(usuarios));
  }, [usuarios]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!form.nombre.trim() || !form.email.trim()) {
      alert('Por favor completa nombre y correo.');
      return;
    }

    const nuevoUsuario = {
      id: Date.now(),
      nombre: form.nombre.trim(),
      email: form.email.trim(),
      rol: form.rol
    };

    setUsuarios((prev) => [nuevoUsuario, ...prev]);
    setForm(emptyForm);
  };

  return (
    <div className="app-shell">
      <div className="panel">
        <h1>SIGAM</h1>
        <p className="subtitle">Crear y leer usuarios</p>

        <form onSubmit={handleSubmit} className="user-form">
          <div className="field-group">
            <label htmlFor="nombre">Nombre</label>
            <input
              id="nombre"
              name="nombre"
              type="text"
              value={form.nombre}
              onChange={handleChange}
              placeholder="Ej: Laura Pérez"
            />
          </div>

          <div className="field-group">
            <label htmlFor="email">Correo</label>
            <input
              id="email"
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              placeholder="ejemplo@sigam.com"
            />
          </div>

          <div className="field-group">
            <label htmlFor="rol">Rol</label>
            <select id="rol" name="rol" value={form.rol} onChange={handleChange}>
              <option value="Administrador">Administrador</option>
              <option value="Operador">Operador</option>
              <option value="Conductor">Conductor</option>
            </select>
          </div>

          <button type="submit">Crear usuario</button>
        </form>
      </div>

      <div className="panel list-panel">
        <div className="list-header">
          <h2>Usuarios registrados</h2>
          <span>{usuarios.length}</span>
        </div>

        <div className="user-list">
          {usuarios.map((usuario) => (
            <article key={usuario.id} className="user-card">
              <div>
                <strong>{usuario.nombre}</strong>
                <p>{usuario.email}</p>
              </div>
              <span className="rol-tag">{usuario.rol}</span>
            </article>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
