import axios from "axios";

const token = localStorage.getItem('access') ? JSON.parse(localStorage.getItem('access')) : "";
const refresh_token = localStorage.getItem('refresh') ? JSON.parse(localStorage.getItem('refresh')) : "";
const baseUrl = "http://localhost:8000/api/v1";
console.log(`Bearer ${token}`)
const AxiosInstance = axios.create({
  baseURL: baseUrl,
  headers: {Authorization: localStorage.getItem('access') ? `Bearer ${token}` : null},
});

AxiosInstance.defaults.headers.post['Content-Type'] = 'application/json';

export default AxiosInstance;