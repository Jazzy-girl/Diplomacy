import Map from "../components/Map";
import { useParams } from "react-router-dom"

function Sandbox(){
    const {id} = useParams();
    return <Map game={false} id={id}/>
}

export default Sandbox