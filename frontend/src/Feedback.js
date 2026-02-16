import React, { useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';

function Feedback() {
  const location = useLocation();
  const username = location.state.username;
  const [message, setMessage] = useState('');
  const [sentiment, setSentiment] = useState('');

  const submitFeedback = async () => {
    const res = await axios.post('http://127.0.0.1:5000/feedback', { username, message });
    setSentiment(res.data.sentiment);
  };

  return (
    <div>
      <h2>Submit Feedback</h2>
      <textarea placeholder="Your feedback" onChange={e => setMessage(e.target.value)}></textarea>
      <button onClick={submitFeedback}>Submit</button>
      {sentiment && <p>Sentiment: {sentiment}</p>}
    </div>
  );
}

export default Feedback;
