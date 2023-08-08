import axios from 'axios';

/**
 * The default
 * @type {AxiosInstance}
 */
const arthurAxios = axios.create({
    baseURL: 'http://localhost:8000/',
    headers: { 'Content-Type': 'application/json' },
    timeout: 1000 * 60, //60 seconds
});


export default arthurAxios;
