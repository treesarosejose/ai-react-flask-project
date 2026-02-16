import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:5000/login', { username, password });
      if (res.data.isAdmin) {
        navigate('/admin');
      } else {
        navigate('/feedback', { state: { username } });
      }
    } catch {
      alert('Invalid credentials');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input placeholder="Username" onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
      <p onClick={() => navigate('/signup')}>New user? Sign up here</p>
    </div>
  );
}

export default Login;
