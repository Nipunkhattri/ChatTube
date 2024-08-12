import axios from 'axios';

const Api = axios.create({
    baseURL :"http://localhost:5000/"
    // baseURL:"https://ramson-perfumes.onrender.com/"
    // baseURL:"https://ramson-perfumes.vercel.app/"
})
  
const getToken = () => {
    const token = localStorage.getItem('token');
    if (!token) {
      return null; 
    }
    return token;
};
  
// Add bearer token to headers if available
Api.interceptors.request.use(config => {
const token = getToken();
if (token) {
    config.headers.Authorization = `Bearer ${token}`;
}
return config;
});

export const login = (login) => Api.post('/auth/login',login);
export const register = (register) => Api.post('/auth/register',register);
export const process = (videolink) => Api.post('/llm/extract_text',videolink);
export const check = (id) => Api.get(`/llm/${id}`);
export const getall = () => Api.get('/llm/GetallIds');
export const Answer = (Askquery) => Api.post('/llm/query',Askquery);
export const GetHistoryById = (id) => Api.get(`/llm/getHistory/${id}`);