import React from "react";
import react, { useState, useEffect } from "react"
import territories from "../assets/territories.json"
import 
/*
Planned Method:
Use JSON to store:
- static map data
- default unit locations and country owners

When starting a game:
- Read the JSON file, make an entry into the "Territories" table for each territory including the territory name and if it has a supply center, default owner
- and make an entry into the "Units" table for each unit

Does this work? Is there a better way to do this?

Would it be better for the "Units" table to have a column for game_id, and either owner_player_id foreign key, or country_owner (TEXT) where the PlayersGames table has game_id, player_id, and assigned country (TEXT)

*/
function Map({game_id}){
    const [hover, setHover] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [unitData, setUnitData] = useState([]);
    const [terrData, setTerrData] = useState([])

    useEffect(()=>{
        async function fetchData() {
            try{
                const res = await fetch('http://localhost:8000/api/units/list')
                .then((res)=>{
                    if(!res.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    return res.json();
                }).then((data)=>{setUnitData(data)});
            }catch(e){
                setError(e);
            }finally{
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    if(loading){
        return <p>Loading data...</p>;
    }

    if(error){
        return <p>Error: {error.message}</p>;
    }

    const map = <div className="flex justify-end p-4"><svg width={window.innerWidth} height={window.innerHeight} viewBox={`0 0 ${window.innerWidth/3} ${window.innerHeight/3}`} className="w-[800px] h-auto border shadow-md">
        {Object.entries(territories).map(([id, territory])=>
            (<g key={id}>
                <path
                key={id}
                d={territory.path}
                fill={hover===id ? "#BA8E23" : "#ff0"}
                stroke="#333"
                strokeWidth={1}
                onMouseEnter={()=>setHover(id)}
                onMouseLeave={()=>setHover("")}
                onClick={()=>alert(`Territory: ${id}`)}
                />
                {territory.labelPos && (
                    <text
                    x={territory.labelPos[0]}
                    y={territory.labelPos[1]}
                    fontSize="10"
                    fill="#000"
                    textAnchor="middle"
                    pointerEvents="none"
                    >{id}</text>
                )}
                </g>
            ))}
            </svg></div>;
    
    const units = <svg width={window.innerWidth} height={window.innerHeight} viewBox={`0 0 ${window.innerWidth/3} ${window.innerHeight/3}`} className="w-[800px] h-auto border shadow-md">
        {unitData.filter((item)=> item.game === game_id).map((unit)=>{
            const territory = territories[unit.territory];
            if(!territory || !territory.unitPos) return null;
            const [cx, cy] = territory.unitPos;
           <circle
           key={unit.id}
           cx={cx}
           cy={cy}
           r="6"
           stroke="black"
           strokeWidth="4"
           fill={unit.owner==="T"? "red" : "blue"}/>;
        })}
        </svg>
    
    return<>{map}{units}</>
}

export default Map