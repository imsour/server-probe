const config = {
    REACT_APP_BACKEND_SCHEME: 'http',
    REACT_APP_BACKEND_HOST: 'localhost',
    REACT_APP_BACKEND_PORT: '8000',
    ...process.env
};

const baseUrl = `${config.REACT_APP_BACKEND_SCHEME}://${config.REACT_APP_BACKEND_HOST}:${config.REACT_APP_BACKEND_PORT}/`

export const api = {
    PROBE_STATUS: `${baseUrl}probe_status`,
    PROBE_DATA: `${baseUrl}probe_data`,
    PROBE_START: `${baseUrl}start`,
    PROBE_STOP: `${baseUrl}stop`,
}