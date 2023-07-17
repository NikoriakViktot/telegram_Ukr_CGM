import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/telegram', // URL нашого FastAPI сервера
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
