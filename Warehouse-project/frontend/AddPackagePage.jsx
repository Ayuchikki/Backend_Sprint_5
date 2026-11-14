import { useState } from 'react'
import API_URL from './api'

function AddPackagePage() {

    const [packageName, setPackageName] = useState("")
    const [destination, setDestination] = useState("")
    const [weight, setWeight] = useState("")

    async function addPackage(e) {

        e.preventDefault()

        const res = await fetch(`${API_URL}/packages`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "token": localStorage.getItem("access_token")
            },
            body: JSON.stringify({
                package_name: packageName,
                destination: destination,
                weight: Number(weight)
            })
        })

        const data = await res.json()

        if (res.ok) {

            alert("Package added successfully")

            setPackageName("")
            setDestination("")
            setWeight("")

        }
        else {
            alert(data.detail || "Unable to add package")
        }
    }

    return (
        <div>
            <h2>Add Package</h2>

            <form onSubmit={addPackage}>

                <label>Package Name</label>
                <input
                    value={packageName}
                    onChange={(e) => setPackageName(e.target.value)}
                    required
                />

                <label>Destination</label>
                <input
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                    required
                />

                <label>Weight</label>
                <input
                    type="number"
                    step="any"
                    min="0.01"
                    value={weight}
                    onChange={(e) => setWeight(e.target.value)}
                    required
                />

                <button type="submit">
                    Add Package
                </button>

            </form>
        </div>
    )
}

export default AddPackagePage