import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer} from 'recharts';
import React, { useState, useEffect } from 'react';

function SensorCard({ label, value, unit, icon }) {
  return (
    <div className="sensor-card">
      <div className="sensor-label">{label}</div>
      <div className="sensor-value">
        {value !== null ? `${value}` : '--'}
        <span className="sensor-unit">{unit}</span>
      </div>
    </div>
  );
}

function SensorChart({ sensor, label, color = '#4caf50' , hours = 200 }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`/api/sensors/history/?sensor=${sensor}&hours=${hours}`)
      .then(response => {
        const formatted = response.data.readings.map(r => ({
          time: new Date(r.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          }),
          value: parseFloat(r.value.toFixed(2))
        }));
        setData(formatted);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [sensor, hours]);

  return (
    <div className="chart-card">
      <div className="chart-title">{label}</div>
      {loading ? (
        <div className = "chart-loading">Loading...</div>
      ) : data.length === 0 ? (
        <div className="chart-loading">No data available</div>
      ) : (
        <ResponsiveContainer width="100%" height={180}>
          <LineChart data = {data}>
            <CartesianGrid strokeDasharray= "3 3" stroke = "#1e2a3a" />
            <XAxis 
              dataKey="time"
              tick={{ fontSize: 10, fill: '#6b7a8d'}}
              interval="preserveStartEnd"
            />
            <YAxis tick = {{ fontSize: 10, fill: '#6b7a8d' }} />
            <Tooltip
              contentStyle = {{
                background: '#0f1923',
                border: '1px solid #1e2a3a',
                borderRadius: '8px',
                color: '#eee'
              }}
            />
            <Line 
              type = "monotone"
              dataKey = "value"
              stroke = {color}
              dot = {false}
              strokeWidth = {2}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

function TimelapseViewer() {
  const [imageUrl, setImageUrl] = useState(null);
  const [timestamp, setTimestamp] = useState(null);

  useEffect(() => {
    axios.get('/api/timelapse/latest/')
      .then(res => {
        setImageUrl(res.data.url);
        setTimestamp(res.data.timestamp);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div className = "chart-card">
      <div className="chart-title">Latest timelapse image</div>
      {imageUrl ? (
        <>
          <img
            src={'http://127.0.0.1:8000${imageUrl}'}
            alt="Latest grow timelapse"
            className="timelapse-img"
          />
          <div className="timelapse-timestamp">
            {timestamp ? new Date(timestamp).toLocaleString() : ''}
          </div>
        </>
      ) : (
        <div className="chart-loading">No timelapse image available</div>
      )}
    </div>
  );
}

function App() {
  const [latest, setLatest] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    const fetchLatest = () => {
      axios.get('/api/sensors/latest/')
        .then(res => {
          setLatest(res.data);
          setLastUpdated(new Date().toLocaleTimeString());
        })
        .catch(err => console.error(err));
    };

    fetchLatest();
    const interval = setInterval(fetchLatest, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const getValue = (key) => {
    if (!latest || !latest[key]) return null;
    return parseFloat(latest[key].value.toFixed(2));
  };

  return (
    <div className="App">
      <header className="header">
        <div className="header-left">
          <h1 className="header-title">Grow Monitor</h1>
          <p className="header-sub">Indoor grow tent dashboard</p>
        </div>
        {lastUpdated && (
          <div className="header-right">
            <span className="live-dot" />
            <span className="live-text">Updated {lastUpdated}</span>
          </div>
        )}
      </header>

      <section className="section">
        <h2 className="section-title">Current Conditions</h2>
        <div className="card-grid">
          <SensorCard label="Temperature" value={getValue('temperature')} unit="°C" />
          <SensorCard label="Humidity" value={getValue('humidity')} unit="%" />
          <SensorCard label="Pressure" value={getValue('pressure')} unit="hPa" />
          <SensorCard label="Light" value={getValue('light')} unit="lux" />
          <SensorCard label="Soil 1 Moisture" value={getValue('soil_moisture_1')} unit="%" />
          <SensorCard label="Soil 2 Moisture" value={getValue('soil_moisture_2')} unit="%" />
          <SensorCard label="Soil 3 Moisture" value={getValue('soil_moisture_3')} unit="%" />
          <SensorCard label="Soil 4 Moisture" value={getValue('soil_moisture_4')} unit="%" />
        </div>
      </section>

      <section className="section">
        <h2 classname="section-title">Historical Data</h2>
        <div className="chart-grid">
          <SensorChart sensor="temperature" label="Temperature (°C)" color="#ff5722" />
          <SensorChart sensor="humidity" label="Humidity (%)" color="#2196f3" />
          <SensorChart sensor="pressure" label="Pressure (hPa)" color="#9c27b0" />
          <SensorChart sensor="light" label="Light (lux)" color="#ffeb3b" />
        </div>
      </section>

      <section className="section">
        <h2 className="section-title">Camera</h2>
        <div className="chart-grid">
          <TimelapseViewer />
        </div>
      </section>
    </div>
  );
}

export default App;
