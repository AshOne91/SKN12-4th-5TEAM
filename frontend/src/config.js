const config = {
    API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
    CHATBOT_API_URL: process.env.REACT_APP_CHATBOT_API_URL || 'http://localhost:8000/chatbot',
    ACCOUNT_API_URL: process.env.REACT_APP_ACCOUNT_API_URL || 'http://localhost:8000/account',
    SEQUENCE: parseInt(process.env.REACT_APP_SEQUENCE) || 0,
    DEFAULT_TIMEOUT: parseInt(process.env.REACT_APP_DEFAULT_TIMEOUT) || 30000,
  };
  
  export default config;