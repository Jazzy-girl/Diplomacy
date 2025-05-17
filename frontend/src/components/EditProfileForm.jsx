import { useState, useEffect } from "react";
import { ACCESS_TOKEN } from "../constants";
import {jwtDecode} from "jwt-decode";

function EditProfileForm({route, method}){
    /*
        Things to edit (currently):
        - username
        - pronouns (can be null)
    */

        const [username, setUsername] = useState("");
        const token = localStorage.getItem(ACCESS_TOKEN);
        useEffect(()=>{
            if(token){
                try{
                    const decodedToken = jwtDecode(token);
                    const user = decodedToken.username;
                    setUsername(user);
                    
                }catch (error){
                    if (error.response) {
                        console.error("Registration error:", error.response.data);
                        alert(JSON.stringify(error.response.data));
                    } else {
                        console.error("Unknown error", error);
                        alert("Something went wrong.");
                    }
                }
            }else{
                alert("No token");
            }});


        return <>
            <label htmlFor="">{username}</label>
        </>;
}

export default EditProfileForm;