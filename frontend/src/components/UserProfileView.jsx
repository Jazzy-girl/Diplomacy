import { useEffect, useState } from "react";
import { ACCESS_TOKEN } from "../constants";

function UserProfileView({userId}){
    const [loading, setLoading] = useState(false);
    const [userData, setUserData] = useState({
        username: "",
        pronouns: "",
    });

    const token = localStorage.getItem(ACCESS_TOKEN);
    useEffect(()=>{
        fetch(`http://localhost:8000/api/user/${userId}/`,
            {
                headers:{
                    "Authorization": `Bearer ${token}`,
                },
            }
        ).then((res)=>{
            if(!res.ok){
                alert("Failed to fetch user");
            }
            return res.json();
        }).then((data)=>{
            setUserData({username: data.username, pronouns: data.pronouns})
        }).catch((error)=>alert(`THIS IS AN ERROR HERE: ${error.message}`));
    }, [token]);

    return <>
        <h1>User Info</h1>
        <label htmlFor="">Username: {userData.username}</label>
        <br />
        <label htmlFor="">Pronouns: {userData.pronouns}</label>
    </>
}
export default UserProfileView;