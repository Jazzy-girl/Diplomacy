import { useParams } from "react-router-dom"
import UserProfileView from "../components/UserProfileView"

function ViewProfile(){
    const {id} = useParams();
    return <UserProfileView userId={id}/>
}

export default ViewProfile