import { useState, useEffect } from 'react'
import API_URL from '../api'

function DispatchPage() {

    const [dispatches, setDispatches] = useState([])

    const [destination, setDestination] = useState("")
    const [vehicle, setVehicle] = useState("")
    const [packageIds, setPackageIds] = useState("")

    async function loadDispatches() {

        const res = await fetch(`${API_URL}/dispatches`, {
            headers: {
                "token": localStorage.getItem("access_token")
            }
        })

        const data = await res.json()

        setDispatches(data)
    }

    useEffect(() => {
        loadDispatches()
    }, [])

    async function createDispatch(e) {

        e.preventDefault()

        const ids = packageIds.split(",").map(id => Number(id.trim()))

        const res = await fetch(`${API_URL}/dispatches`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "token": localStorage.getItem("access_token")
            },
            body: JSON.stringify({
                destination: destination,
                vehicle: vehicle,
                package_ids: ids
            })
        })

        if (res.ok) {

            alert("Dispatch created successfully")

            setDestination("")
            setVehicle("")
            setPackageIds("")

            loadDispatches()

        }
        else {
            alert("Unable to create dispatch")
        }
    }

    return (
        <div>
            <h2>Create Dispatch</h2>

            <form onSubmit={createDispatch}>
                <input
                    placeholder="Destination"
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                    required
                />

                <input
                    placeholder="Vehicle"
                    value={vehicle}
                    onChange={(e) => setVehicle(e.target.value)}
                    required
                />

                <input
                    placeholder="Package IDs (1,2,3)"
                    value={packageIds}
                    onChange={(e) => setPackageIds(e.target.value)}
                    required
                />

                <button type="submit">
                    Create Dispatch
                </button>
            </form>

            <h2>All Dispatches</h2>

            {dispatches.map((item) => (
                <div className="dispatch-card" key={item.id}>
                    <h3>Dispatch #{item.id}</h3>
                    <p>Destination: {item.destination}</p>
                    <p>Vehicle: {item.vehicle}</p>
                    <p>Status: {item.dispatch_status}</p>
                    <p>Date: {item.dispatch_date}</p>
                </div>
            ))}
        </div>
    )
}

export default DispatchPage