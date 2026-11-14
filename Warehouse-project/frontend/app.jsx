import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import PackageListPage from './pages/PackageListPage'
import AddPackagePage from './pages/AddPackagePage'
import PackageDetailPage from './pages/PackageDetailPage'
import DispatchPage from './pages/DispatchPage'
import LoginPage from './pages/LoginPage'

function App() {
    return (
        <BrowserRouter>
            <div className="app">
                <h1>Warehouse Dispatch Management</h1>

                <nav>
                    <Link to="/login">Login</Link>
                    <Link to="/">Packages</Link>
                    <Link to="/add">Add Package</Link>
                    <Link to="/dispatch">Dispatch</Link>
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