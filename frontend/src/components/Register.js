import React, { useState } from 'react';

function Register() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        curso: '',
        genero: '',
        foto: null
    });

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
            body: data  // Usando FormData para suportar upload de arquivo
        });
        const responseData = await response.json();
        if (response.ok) {
            console.log('Registration successful', responseData);
        } else {
            console.log('Registration failed', responseData);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                            <label className="form-label">Username:</label>
                            <input
                                type="text"
                                className="form-control"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
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
                                required
                            />
                        </div>

                        <div className="mb-3">
                        <select name="curso" value={formData.curso} onChange={handleChange}>
                            {/* Opções do curso */}
                        </select>
                        </div>
                        <div className="mb-3">
                        <select name="genero" value={formData.genero} onChange={handleChange}>
                            {/* Opções de gênero */}
                        </select>
                        </div>
                <input type="file" name="foto" onChange={handleChange} />
                <button type="submit">Register</button>
            </form>
        </div>
    );
}

export default Register;

/*
import React, { useState } from 'react';

function Register() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const response = await fetch('http://localhost:8000/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        const data = await response.json();
        if (response.ok) {
            console.log('Registration successful', data);
            // Pós-registro, como redirecionar para outra página
        } else {
            console.log('Registration failed', data);
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <form onSubmit={handleSubmit} className="card card-body">
                        <div className="mb-3">
                            <label className="form-label">Username:</label>
                            <input
                                type="text"
                                className="form-control"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
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
                                required
                            />
                        </div>
                        <button type="submit" className="btn btn-primary">Register</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Register;


 */