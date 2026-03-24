// Automatically switches between Local and Prod based on the browser URL
const CONFIG = {
    get current_api() {
        if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
            return "http://localhost:5000/api";
        } else {
            return "https://minor-project-mzi2.onrender.com/api";
        }
    }
};

window.CONFIG = CONFIG;