import Map from "../components/Map";
import { useParams } from "react-router-dom"

function PlayGame(){
    const {id} = useParams();
    return <Map game={true} id={id}/>
}

export default PlayGame