// Local/prod config

const CONFIG = {
    ENV_INDEX: 0,   //0: local, 1: prod
    
    API_URLS: [
        "http://localhost:5000/api",
        ""  // RENDER link
    ],

    get current_api() {
        return this.API_URLS[this.ENV_INDEX];
    }
};

window.CONFIG = CONFIG;