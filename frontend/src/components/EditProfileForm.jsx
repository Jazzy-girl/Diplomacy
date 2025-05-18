import { useState, useEffect } from "react";
import { ACCESS_TOKEN } from "../constants";
import {jwtDecode} from "jwt-decode";
import api from "../api";

function EditProfileForm({route}){
    /*
        Things to edit (currently):
        - username
        - pronouns (can be null)
    */

    const [username, setUsername] = useState("");
    const [pronouns, setPronouns] = useState("");
    const [loading, setLoading] = useState(false);
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
        }).then((data)=>{setUsername(data.username);setPronouns(data.pronouns);})
        .catch((error)=>alert(error.message));
    }, [token]);

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        //Alter data
        try{
            const res = await api.put('api/user/update/', {username, pronouns},{
                headers: {
                    Authorization: `Bearer ${token}`,
                }
                },
            );
            alert(`Data updated successfully`);
            window.location.reload();
        }catch (error){
            alert(error.message);
        }
    }

    return <form onSubmit={handleSubmit}>
        <h1>User Info</h1>
        <label>Displayed name</label>
        <input type="text" value={username} onChange={(e)=>setUsername(e.target.value)} placeholder={username}/>
        <label htmlFor="">Pronouns</label>
        <input type="text" value={pronouns} onChange={(e)=>setPronouns(e.target.value)} placeholder={pronouns}/>
        <button type="submit">Submit Changes</button>
    </form>
}

export default EditProfileForm;