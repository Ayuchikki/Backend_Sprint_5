import {useState} from 'react'
import {useNavigate} from 'react-router-dom'
import API_URL from '../api'
function AddPackagePage() {
    const navigate = useNavigate()
    const [name, setName] = useState("")
    const [destination, setDestination] = useState("")
    const [weight, setWeight] = useState("")

    async function addPackage(e) {
        e.preventDefault()
        const res = await fetch(`${API_URL}/packages`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                package_name: name,
                destination: destination,
                weight: Number(weight)
            })
        })

        if (res.ok) {
            alert("Package added successfully")
            navigate("/")
        }
        else {
            alert("Unable to add package")
        }
    }
    return (
        <div>
            <h2>Add New Package</h2>
            <form onSubmit={addPackage}>
                <input
                    placeholder="Package Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
                <input
                    placeholder="Destination"
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Weight"
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