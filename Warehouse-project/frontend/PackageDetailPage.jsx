import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import API_URL from '../api'

function PackageDetailPage() {

    const { id } = useParams()
    const [item, setItem] = useState(null)

    useEffect(() => {
        async function loadPackage() {

            const res = await fetch(`${API_URL}/packages/${id}`, {
                headers: {
                    "token": localStorage.getItem("access_token")
                }
            })

            const data = await res.json()
            setItem(data)
        }

        loadPackage()
    }, [id])

    async function updatePackage(e) {

        e.preventDefault()

        const res = await fetch(`${API_URL}/packages/${id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "token": localStorage.getItem("access_token")
            },
            body: JSON.stringify({
                package_name: item.package_name,
                destination: item.destination,
                weight: Number(item.weight),
                status: item.status
            })
        })

        if (res.ok) {
            alert("Package updated successfully")
        }
        else {
            alert("Unable to update package")
        }
    }

    if (!item) {
        return <p>Loading...</p>
    }

    return (
        <div>
            <h2>Package Details</h2>

            <form onSubmit={updatePackage}>
                <label>Package Name</label>

                <input
                    value={item.package_name}
                    onChange={(e) => setItem({
                        ...item,
                        package_name: e.target.value
                    })}
                />

                <label>Destination</label>

                <input
                    value={item.destination}
                    onChange={(e) => setItem({
                        ...item,
                        destination: e.target.value
                    })}
                />

                <label>Weight</label>

                <input
                    type="number"
                    value={item.weight}
                    onChange={(e) => setItem({
                        ...item,
                        weight: e.target.value
                    })}
                />

                <label>Status</label>

                <select
                    value={item.status}
                    onChange={(e) => setItem({
                        ...item,
                        status: e.target.value
                    })}
                >
                    <option value="Pending">Pending</option>
                    <option value="Dispatched">Dispatched</option>
                    <option value="Delivered">Delivered</option>
                </select>

                <button type="submit">
                    Update Package
                </button>
            </form>
        </div>
    )
}

export default PackageDetailPage