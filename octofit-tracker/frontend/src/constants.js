export const API_BASE_URL = 
  process.env.REACT_APP_CODESPACE 
    ? `https://${process.env.REACT_APP_CODESPACE}-8000.app.github.dev/api` 
    : 'http://localhost:8000/api';