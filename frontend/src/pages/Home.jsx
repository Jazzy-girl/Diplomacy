import { useEffect, useState } from "react"
import { ACCESS_TOKEN } from "../constants"
import {Link} from "react-router-dom"
import ExistingGamesTable from "../components/ExistingGamesTable"
import YourSandboxesTable from "../components/YourSandboxesTable"

function Home(){
    
    return <>
    <div className="py-8 text-red-100">Home</div>
    <p><Link to="/settings">Your Settings</Link></p>
    <p><Link to="/create/sandbox">Make a New Sandbox</Link></p>
    <YourSandboxesTable/>
    </>
}

export default Home