// Handles communication with backend API + configured in config.js

const API_BASE_URL = window.CONFIG.current_api;

const API = {
    admin: {    // ADMIN
        loginCheck: async (credential) => {     // Login check
            try {
                const response = await fetch(`${API_BASE_URL}/admin/login_check`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ credential })
                });
                return await response.json();
            } catch (error) {
                console.error("Login API Error:", error);
                return { ok: false, error: "Server unreachable" };
            }
        },

        issueCert: async (certData) => {    // Certificate issue 
            try {
                const response = await fetch(`${API_BASE_URL}/api/admin/issue`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(certData)
                });
                return await response.json();
            } catch (error) {
                console.error("Issuance API Error:", error);
                return { ok: false, error: "Failed to connect to backend" };
            }
        }
    },

    public: {   // PUBLIC
        fetchStudentCerts: async (email) => {   // Fetch all certs for a student
            try {
                const response = await fetch(`${API_BASE_URL}/student/certificates?email=${email}`);
                return await response.json();
            } catch (error) {
                console.error("Fetch Certs API Error:", error);
                return { ok: false, error: "Database connection failed" };
            }
        },

        verifyCert: async (email, txHash) => {  // Verify certificate
            try {
                const response = await fetch(`${API_BASE_URL}/employer/verify`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email: email, tx_hash: txHash })
                });
                return await response.json();
            } catch (error) {
                console.error("Verification API Error:", error);
                return { ok: false, error: "Verification server is offline" };
            }
        }
    }
};

// Expose the API for all scripts
window.API = API;