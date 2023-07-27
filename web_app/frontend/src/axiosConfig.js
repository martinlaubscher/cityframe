import axios from "axios";

// Determine if we're in development or production
const isDevelopment = process.env.NODE_ENV !== 'production';

// Set the base URL depending on the environment
const baseURL = isDevelopment ? 'http://127.0.0.1:8000' : '';

// Create an instance of axios with predefined config
const instance = axios.create({
    baseURL
});

export default instance;