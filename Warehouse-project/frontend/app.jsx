import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import PackageListPage from './PackageListPage'
import AddPackagePage from './AddPackagePage'
import PackageDetailPage from './PackageDetailPage'
import DispatchPage from './DispatchPage'
import LoginPage from './LoginPage'

function App() {

    const role = localStorage.getItem("role")

    function logout() {
        localStorage.clear()
        window.location.href = "/login"
    }

    return (
        <BrowserRouter>

            <div className="app">

                <h1>Warehouse Dispatch Management</h1>

                <nav>
                    <Link to="/login">Login</Link>

                    <Link to="/">Packages</Link>

                    <Link to="/add">Add Package</Link>

                    <Link to="/dispatch">Dispatch</Link>

                    {role && (
                        <span>{role}</span>
                    )}

                    {role && (
                        <button onClick={logout}>
                            Logout
                        </button>
                    )}
                </nav>

                <Routes>
                    <Route path="/login" element={<LoginPage />} />

                    <Route path="/" element={<PackageListPage />} />

                    <Route path="/add" element={<AddPackagePage />} />

                    <Route path="/package/:id" element={<PackageDetailPage />} />

                    <Route path="/dispatch" element={<DispatchPage />} />
                </Routes>

            </div>

        </BrowserRouter>
    )
}

export default App