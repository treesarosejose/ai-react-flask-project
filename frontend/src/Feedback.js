import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';

function Feedback() {
  const location = useLocation();
  const username = location.state.username;
  const [text, setText] = useState('');
  const [emotion, setEmotion] = useState('');

 const submitFeedback = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username, text: text }) 
    });
    const data = await res.json();
    setEmotion(res.data.Emotion); // display sentiment
  } catch (error) {
    console.error('Error sending feedback:', error);
    alert('Failed to send feedback. Make sure backend is running.');
  }
};

  return (
    <div>
      <h2>Submit Feedback</h2>
      <textarea placeholder="Your feedback" onChange={e => setText(e.target.value)}></textarea>
      <button onClick={submitFeedback}>Submit</button>
      {emotion && <p>Emotion: {emotion}</p>}
    </div>
  );
}

export default Feedback;
