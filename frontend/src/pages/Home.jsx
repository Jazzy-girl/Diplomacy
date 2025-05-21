import { useEffect, useState } from "react"
import { ACCESS_TOKEN } from "../constants"
import {Link} from "react-router-dom"
import ExistingGamesTable from "../components/ExistingGamesTable"

function Home(){
    
    return <>
    <div className="py-8 text-red-100">Home</div>
    <p><Link to="/settings">Your Settings</Link></p>
    <p><Link to="/create">Make a New Game</Link></p>
    <ExistingGamesTable/>
    </>
}

export default Home