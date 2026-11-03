import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function Login() {
    const navigate = useNavigate();
    const { login } = useContext(AuthContext);

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();

        setError("");

        if (!email.trim()) {
            setError("Please enter your email.");
            return;
        }

        if (!password) {
            setError("Please enter your password.");
            return;
        }

        try {
            const data = await login(
                email,
                password
            );

            console.log(
                "Login successful:",
                data
            );

            navigate("/");

        } catch (error) {
            setError(
                error.message || "Login failed."
            );
        }
    };

    return (
        <main>
            <section className="login-section">

                <h2>Login</h2>

                {error && (
                    <p>{error}</p>
                )}

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

                    <div>
                        <label htmlFor="password">
                            Password
                        </label>

                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(event) =>
                                setPassword(event.target.value)
                            }
                        />
                    </div>

                    <a
                        href="/forgot-password"
                        onClick={(event) => {
                            event.preventDefault();
                            navigate("/forgot-password");
                        }}
                        className="forgot-password-link"
                    >
                        Forgot password?
                    </a>

                    <button type="submit">
                        Login
                    </button>

                </form>

                <p className="auth-switch">
                    Don't have an account?{" "}
                    <button
                        type="button"
                        className="auth-link-button"
                        onClick={() => navigate("/register")}
                    >
                        Signup
                    </button>
                </p>

            </section>
        </main>
    );
}

export default Login;