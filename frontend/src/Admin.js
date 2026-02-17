import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Admin() {
  const [feedbacks, setFeedbacks] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/admin/feedbacks')
      .then(res => setFeedbacks(res.data))
      .catch(err => console.log(err));
  }, []);

  return (
    <div>
      <h2>Admin Feedback Panel</h2>
      <table border="1">
        <thead>
          <tr>
            <th>Username</th>
            <th>text</th>
            <th>Emotion</th>
          </tr>
        </thead>
        <tbody>
          {feedbacks.map((f, i) => (
            <tr key={i}>
              <td>{f[0]}</td>
              <td>{f[1]}</td>
              <td>{f[2]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Admin;
