
import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { resetPassword } from "../api";

function ResetPassword() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();

    const token = searchParams.get("token");

    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError("");
        setMessage("");

        if (!token) {
            setError("Invalid or missing password-reset token.");
            return;
        }

        if (password.length < 8) {
            setError("Password must be at least 8 characters long.");
            return;
        }

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        try {
            const data = await resetPassword(token, password);

            setMessage(data.message);

            setPassword("");
            setConfirmPassword("");

            setTimeout(() => {
                navigate("/login");
            }, 2000);
        } catch (error) {
            setError(error.message || "Unable to reset password.");
        }
    };

    return (
        <div className="reset-password-page">
            <h2>Reset Password</h2>
            <p>Enter your new password below.</p>

            {error && <p role="alert">{error}</p>}
            {message && <p role="status">{message}</p>}

            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="new-password">
                        New Password
                    </label>
                    <input
                        id="new-password"
                        type="password"
                        value={password}
                        onChange={(event) =>
                            setPassword(event.target.value)
                        }
                        autoComplete="new-password"
                        required
                    />
                </div>

                <div>
                    <label htmlFor="confirm-password">
                        Confirm New Password
                    </label>
                    <input
                        id="confirm-password"
                        type="password"
                        value={confirmPassword}
                        onChange={(event) =>
                            setConfirmPassword(event.target.value)
                        }
                        autoComplete="new-password"
                        required
                    />
                </div>

                <button type="submit">
                    Reset Password
                </button>
            </form>

            <button
                type="button"
                onClick={() => navigate("/login")}
            >
                Back to Login
            </button>
        </div>
    );
}

export default ResetPassword;
