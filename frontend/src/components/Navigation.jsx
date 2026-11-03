import { Link } from "react-router-dom";

function Navigation() {
    return (
        <nav className="navigation">
            <Link to="/">Home</Link>
            <Link to="/history">Search History</Link>
            <Link to="/documents">Documents</Link>
            <Link to="/settings">Settings</Link>
        </nav>
    );
}

export default Navigation;