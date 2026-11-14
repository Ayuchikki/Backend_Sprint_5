import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import API_URL from './api'

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

        if (res.ok) {
            setPackages(data)
        }
        else {
            alert(data.detail || "Unable to load packages")
        }
    }

    useEffect(() => {
        loadPackages()
    }, [])

    async function searchPackages() {

        if (search === "") {
            loadPackages()
            return
        }

        const res = await fetch(`${API_URL}/search/${encodeURIComponent(search)}`, {
            headers: {
                "token": localStorage.getItem("access_token")
            }
        })

        const data = await res.json()

        if (res.ok) {
            setPackages(data)
        }
        else {
            alert(data.detail || "Search failed")
        }
    }

    async function deletePackage(id) {

        if (localStorage.getItem("role") !== "admin") {
            alert("Only admin can delete packages")
            return
        }

        const res = await fetch(`${API_URL}/packages/${id}`, {
            method: "DELETE",
            headers: {
                "token": localStorage.getItem("access_token")
            }
        })

        if (res.ok) {
            alert("Package deleted")
            loadPackages()
        }
        else {
            alert("Unable to delete package")
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

                        {localStorage.getItem("role") === "admin" && (
                            <button onClick={() => deletePackage(item.id)}>
                                Delete
                            </button>
                        )}

                    </div>

                ))}

            </div>

        </div>
    )
}

export default PackageListPage