import { useState } from "react";
import { registerUser } from "../api";
import { useNavigate } from "react-router-dom";

function Register() {
    const navigate = useNavigate();

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
            const data = await registerUser(
                email,
                password
            );

            console.log(
                "Registration successful:",
                data
            );

            navigate("/");

        } catch (error) {
            setError(
                error.message || "Registration failed."
            );
        }
    };

    return (
        <main>
            <section className="register-section">

                <h2>Register</h2>

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

                    <button type="submit">
                        Register
                    </button>

                </form>

                <p className="auth-switch">
                    Already have an account?{" "}
                    <button
                        type="button"
                        className="auth-link-button"
                        onClick={() => navigate("/login")}
                    >
                        Login
                    </button>
                </p>

            </section>
        </main>
    );
}

export default Register;