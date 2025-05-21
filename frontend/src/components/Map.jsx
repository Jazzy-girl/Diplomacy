import React from "react";
import react, { useState, useEffect } from "react"
import territories from "../assets/territories.json"


function Map({game_id}){
    const [hover, setHover] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [unitData, setUnitData] = useState([]);
    const [terrData, setTerrData] = useState([])

    useEffect(()=>{
        async function fetchData() {
            try{
                const res = await fetch('http://localhost:8000/api/units/list/').then((res)=>{
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

    return (<div className="relative w-[800px] h-auto"><svg width={window.innerWidth} height={window.innerHeight} viewBox={`0 0 ${window.innerWidth/3} ${window.innerHeight/3}`} className="w-[800px] h-auto border shadow-md">
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
                    fontSize="5"
                    fill="#000"
                    textAnchor="middle"
                    pointerEvents="none"
                    >{id}</text>
                )}
                </g>
            ))}

        {unitData.filter((u) => u.game === Number(game_id)).map((unit)=>{
            console.log("Rendering unit at:", unit.location);
            const territory = territories[unit.location];
            if(!territory || !territory.unitPos) return null;
            const [cx, cy] = territory.unitPos;
            return(
           <circle
           key={unit.id}
           cx={cx}
           cy={cy}
           r="3"
           stroke="black"
           strokeWidth="1"
           pointerEvents="none"
           fill={unit.owner==="T"? "red" : "blue"}/>
            );
        })}
        </svg>
        </div>
    );
}

export default Map