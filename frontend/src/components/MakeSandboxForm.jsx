import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants";

function MakeSandboxForm(){
    const [name, setName] = useState("");
    const navigate = useNavigate();
    const [id, setId] = useState();
    const token = localStorage.getItem(ACCESS_TOKEN);

    useEffect(()=>{
        if(!token){
            alert("No token!!");
            return;
        }

        fetch("http://localhost:8000/api/user/",
            {
                headers:{
                    "Authorization": `Bearer ${token}`,
                },
            }
        ).then((res)=>{
            if(!res.ok){
                alert("Failed to fetch user")
            }
            return res.json();
        }).then((data)=>{setId(data.id)})
        .catch((error)=>alert(error.message));
    }, [token]);

    const handleSubmit = async (e) =>{
        e.preventDefault();
        const newSandbox = {name, creator: Number(id)};
        try{
            const res = await fetch('http://localhost:8000/api/create/sandbox/',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newSandbox)
            });
            if(!res.ok) throw new Error(res.status);
            console.log('Game created!!');
            setName('');
            const data = await res.json();
            const sandboxId = data.id;
            navigate(`/sandbox/ID/${sandboxId}`);
        }catch (error){
            console.error();
        }
        
    }

    return(
        <form onSubmit={handleSubmit}>
            <label >New Sandbox</label>
            <label >Title: <input
            type="text"
            value={name}
            onChange={(e)=>setName(e.target.value)}
            /></label>
            <button type="submit">Create Sandbox</button>
        </form>
    )
}

export default MakeSandboxForm