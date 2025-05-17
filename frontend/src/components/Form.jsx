import { useState } from "react";
import api from "../api"
import { Link, useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css"

function Form({route, method}){
    const [email, setEmail] = useState()
    const [username, setUsername] = useState()
    const [password1, setPassword1] = useState()
    const [password2, setPassword2] = useState()
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const name = method === "login" ? "Login" : "Register"

    const handleSubmit = async (e) => {
        setLoading(true)
        e.preventDefault();
        //Submit the user and password
        try{
            const res = await api.post(
                route, 
                method === "login" ? {email, password1, password1: password2} : {email, username, password1, password2}
            );
            if (method === "login"){
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/");
            }else{
                //alert("Registration successful. Please check your email to verify your accout.")
                //navigate("/login");
                navigate("/verify-email");
            }

        }catch(error){
            if (error.response) {
            console.error("Registration error:", error.response.data);
            alert(JSON.stringify(error.response.data));
            } else {
            console.error("Unknown error", error);
            alert("Something went wrong.");
            }
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
        value={password1}
        onChange={(e)=>setPassword1(e.target.value)}
        placeholder="Password"
        required
        />
        {method !=="login"&&
        <>
            <label htmlFor="" className="label-input">Password (again)</label>
            <input className="form-input"
            type="password"
            value={password2}
            onChange={(e)=>setPassword2(e.target.value)}
            placeholder="Password"
            required
            />
        </>}
        <button className="form-button" type="submit" >{name}</button>
        
    </form>
}

export default Form