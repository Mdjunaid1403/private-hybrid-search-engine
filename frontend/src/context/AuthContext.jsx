import { createContext, useState, useEffect } from "react";
import {
    loginUser,
    getCurrentUser
 } from "../api";

export const AuthContext = createContext();

function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [authLoading, setAuthLoading] = useState(true);

    useEffect(() => {
        const restoreAuthentication = async () => {
            const token = localStorage.getItem(
                "access_token"
            );

            if (!token) {
                setAuthLoading(false);
                return;
            }

            try {
                const data = await getCurrentUser();

                setUser(data.user);

            } catch (error) {
                localStorage.removeItem(
                    "access_token"
                );

                setUser(null);

            } finally {
                setAuthLoading(false);
            }
        };

        restoreAuthentication();
    }, []);

    const isAuthenticated = user !== null;

    const login = async (email, password) => {
        const data = await loginUser(
            email,
            password
        );

        localStorage.setItem(
            "access_token",
            data.access_token
        );

        setUser(data.user);

        return data;
    };

    const logout = () => {
        localStorage.removeItem(
            "access_token"
        );

        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                setUser,
                isAuthenticated,
                authLoading,
                login,
                logout
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export default AuthProvider;