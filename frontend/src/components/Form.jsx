import { useState } from "react";
import api from "../api"
import { Link, useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css"

function Form({route, method}){
    const [email, setEmail] = useState()
    const [username, setUsername] = useState()
    const [password, setPassword] = useState()
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const name = method === "login" ? "Login" : "Register"

    const handleSubmit = async (e) => {
        setLoading(true)
        e.preventDefault();
        //Submit the user and password
        try{
            const res = await api.post(route, 
                method === "login" ? {email, password} : {email, username, password});
            if (method==="login"){
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/");
            }else{
                navigate("/login");
            }

        }catch(error){
            alert(error);
        }finally{
            setLoading(false)
        }
    }

    return <form onSubmit={handleSubmit} className="form-container">
        <h1>{name}</h1>
        {method==="register" && <p>Already have an account? <Link to="/login">Login Here</Link></p>}
        {method==="login" && <p>Don't have an account? <Link to="/register">Register Here</Link></p>}
        <label htmlFor="emailInput" className="label-input">Email</label>
        <input id="emailInput"
        className="form-input"
        type="email"
        value={email}
        onChange={(e)=>setEmail(e.target.value)}
        placeholder="email"
        required
        />
        {method !=="login" && (
            <>
            <label htmlFor="" className="label-input">Username</label>
            <input className="form-input"
            type="text"
            value={username}
            onChange={(e)=>setUsername(e.target.value)}
            placeholder="username"
            required
            />
            </>
        )}
        <label htmlFor="" className="label-input">Password</label>
        <input className="form-input"
        type="password"
        value={password}
        onChange={(e)=>setPassword(e.target.value)}
        placeholder="Password"
        required
        />
        <button className="form-button" type="submit" >{name}</button>
        
    </form>
}

export default Form