import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { requestPasswordReset } from "../api";

function ForgotPassword() {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();

        setMessage("");
        setError("");

        if (!email.trim()) {
            setError("Please enter your email.");
            return;
        }

        try {
            const data = await requestPasswordReset(email.trim());
            setMessage(data.message);
        } catch (error) {
            setError(error.message || "Unable to request password recovery.");
        }
    };

    return (
        <main>
            <section className="login-section">
                <h2>Forgot Password</h2>

                <p>
                    Enter your registered email address
                    to begin password recovery.
                </p>

                {error && <p>{error}</p>}
                {message && <p>{message}</p>}

                <form onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="email">
                            Email
                        </label>

                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(event) =>
                                setEmail(event.target.value)
                            }
                        />
                    </div>

                    <button type="submit">
                        Continue
                    </button>
                </form>

                <p className="auth-switch">
                    Remember your password?{" "}
                    <button
                        type="button"
                        className="auth-link-button"
                        onClick={() => navigate("/login")}
                    >
                        Back to Login
                    </button>
                </p>
            </section>
        </main>
    );
}

export default ForgotPassword;
