import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Signup() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:5000/signup', { username, password });
      alert(res.data.message);
      navigate('/');
    } catch {
      alert('Username already exists');
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      <input placeholder="Username" onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleSignup}>Sign up</button>
    </div>
  );
}

export default Signup;
