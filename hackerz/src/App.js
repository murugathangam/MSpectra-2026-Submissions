import { useState, useEffect } from "react";

export default function App() {
  const [task, setTask] = useState({
    topic: "",
    date: "",
    time: "",
    type: "email draft",
    email: ""
  });

  const [tasks, setTasks] = useState([]);

  const handleChange = (e) => {
    setTask({ ...task, [e.target.name]: e.target.value });
  };

  const addTask = async () => {
    await fetch("http://localhost:5000/add-task", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(task)
    });

    setTask({
      topic: "",
      date: "",
      time: "",
      type: "email draft",
      email: ""
    });

    fetchTasks();
  };

  const fetchTasks = async () => {
    const res = await fetch("http://localhost:5000/tasks");
    const data = await res.json();
    setTasks(data);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div style={{
      fontFamily: "Arial",
      background: "#0f172a",
      minHeight: "100vh",
      color: "white",
      padding: 30
    }}>
      <h1>🚀 AI Task Scheduler</h1>

      <div style={{
        background: "#1e293b",
        padding: 20,
        borderRadius: 12,
        marginBottom: 30
      }}>
        <h3>Add Task</h3>

        <input name="topic" placeholder="Topic" onChange={handleChange} /><br /><br />
        <input type="date" name="date" onChange={handleChange} /><br /><br />
        <input type="time" name="time" onChange={handleChange} /><br /><br />

        <select name="type" onChange={handleChange}>
          <option value="email draft">Email Draft</option>
          <option value="reminder">Reminder</option>
        </select><br /><br />

        <input name="email" placeholder="Email" onChange={handleChange} /><br /><br />

        <button onClick={addTask} style={{
          padding: "10px 20px",
          borderRadius: 8,
          background: "#3b82f6",
          color: "white",
          border: "none"
        }}>
          Add Task
        </button>
      </div>

      <h3>📋 Tasks</h3>

      {tasks.map((t, i) => (
        <div key={i} style={{
          background: "#1e293b",
          padding: 15,
          marginBottom: 10,
          borderRadius: 10
        }}>
          <b>{t.topic}</b><br />
          📅 {t.date} ⏰ {t.time}<br />
          🧠 {t.type}<br />
          ✅ {t.status}
        </div>
      ))}
    </div>
  );
}