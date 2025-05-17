import { useEffect, useState } from "react"
import { ACCESS_TOKEN } from "../constants"


function Home(){
    const [username, setUsername] = useState("");

    useEffect(()=>{
        const token = localStorage.getItem(ACCESS_TOKEN);

        if(!token){
            alert("No token!!");
            return;
        }

        fetch("http://localhost:8000/api/current-user/",
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
        }).then((data)=>setUsername(data.username))
        .catch((error)=>alert(error.message));
    }, []);
    return <div>{username}</div>
}

export default Home