import { useState } from 'react'
import API_URL from '../api'

function LoginPage() {

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    async function login(e) {
        e.preventDefault()

        const res = await fetch(`${API_URL}/login?username=${username}&password=${password}`, {
            method: "POST"
        })

        const data = await res.json()

        if (res.ok) {
            localStorage.setItem("access_token", data.access_token)
            localStorage.setItem("refresh_token", data.refresh_token)

            alert("Login successful")
            window.location.href = "/"
        }
        else {
            alert("Invalid username or password")
        }
    }

    return (
        <div>
            <h2>Login</h2>

            <form onSubmit={login}>
                <input
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button type="submit">Login</button>
            </form>
        </div>
    )
}

export default LoginPage