import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import API_URL from '../api'

function PackageListPage() {

    const [packages, setPackages] = useState([])
    const [search, setSearch] = useState("")

    async function loadPackages() {

        const res = await fetch(`${API_URL}/packages`, {
            headers: {
                "token": localStorage.getItem("access_token")
            }
        })

        const data = await res.json()
        setPackages(data)
    }

    useEffect(() => {
        loadPackages()
    }, [])

    async function searchPackages() {

        if (search === "") {
            loadPackages()
            return
        }

        const res = await fetch(`${API_URL}/search/${search}`, {
            headers: {
                "token": localStorage.getItem("access_token")
            }
        })

        const data = await res.json()
        setPackages(data)
    }

    async function deletePackage(id) {

        const res = await fetch(`${API_URL}/packages/${id}`, {
            method: "DELETE",
            headers: {
                "token": localStorage.getItem("access_token")
            }
        })

        if (res.ok) {
            loadPackages()
        }
    }

    return (
        <div>
            <h2>All Packages</h2>

            <div>
                <input
                    placeholder="Search package"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />

                <button onClick={searchPackages}>
                    Search
                </button>

                <button onClick={loadPackages}>
                    Show All
                </button>
            </div>

            <div className="packages">
                {packages.map((item) => (
                    <div className="package-card" key={item.id}>
                        <h3>{item.package_name}</h3>
                        <p>Destination: {item.destination}</p>
                        <p>Weight: {item.weight}</p>
                        <p>Status: {item.status}</p>

                        <Link to={`/package/${item.id}`}>
                            View Details
                        </Link>

                        <br />

                        <button onClick={() => deletePackage(item.id)}>
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default PackageListPage