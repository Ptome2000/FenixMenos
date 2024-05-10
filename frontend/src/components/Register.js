import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function Register() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        curso: '',
        foto: null
    });

    const [cursos, setCursos] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/api/cursos/')
            .then(response => response.json())
            .then(data => setCursos(data))
            .catch(error => console.error('Error fetching cursos:', error));
    }, []);


    const handleChange = (e) => {
        if (e.target.name === 'foto') {
            setFormData({...formData, [e.target.name]: e.target.files[0]});
        } else {
            setFormData({...formData, [e.target.name]: e.target.value});
        }

    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const data = new FormData();
        Object.keys(formData).forEach(key => data.append(key, formData[key]));

        const response = await fetch('http://localhost:8000/register/', {
            method: 'POST',
            body: data
        });
        const responseData = await response.json();
        if (response.ok) {
            console.log('Registration successful', responseData);
            window.location.href = "http://localhost:8000/FenixMenos/login";
        } else {
            console.log('Registration failed', responseData);
        }
    };

    return (
        <div className="container min-vh-100 d-flex justify-content-center align-items-center">
            <div className="row">
                <div className="col-md-20">
                  <form onSubmit={handleSubmit} className="card card-body">
                    <div className="mb-3">
                      <label className="form-label">Username:</label>
                      <input
                          type="text"
                          className="form-control"
                          name="username"
                          value={formData.username}
                          onChange={handleChange}
                          placeholder="Insira o seu Username"
                          required
                      />
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Email:</label>
                      <input
                          type="email"
                          className="form-control"
                          name="email"
                          value={formData.email}
                          onChange={handleChange}
                          placeholder="Insira o seu Email"
                          required
                      />
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Password:</label>
                      <input
                          type="password"
                          className="form-control"
                          name="password"
                          value={formData.password}
                          onChange={handleChange}
                          placeholder="Insira a sua Password"
                          required
                      />
                    </div>
                    <div className="mb-3">
                      <label className="form-label">Curso:</label>
                      <select
                          className="form-select"
                          name="curso"
                          value={formData.curso}
                          onChange={handleChange}
                          required
                      >
                        <option value="">Selecione um curso</option>
                        {cursos.map(curso => (
                            <option key={curso.id} value={curso.id}>{curso.designacao}</option>
                        ))}
                      </select>
                    </div>
                          <div className="mb-3">
                            <label className="form-label" htmlFor="foto">Upload Foto (Opcional):</label>
                            <input
                                type="file"
                                className="form-control"
                                id="foto"
                                name="foto"
                                onChange={handleChange}
                            />
                        </div>
                        <button type="submit" className="btn btn-primary btn-block">Registrar</button>
                    </form>
                </div>
            </div>
        </div>
    );
}
export default Register;