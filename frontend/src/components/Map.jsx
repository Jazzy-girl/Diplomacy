import React from "react";
import react, { useState, useEffect } from "react"
import territories from "../assets/territories.json"


function Map({game, id}){
    const [hover, setHover] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [unitData, setUnitData] = useState([]);
    const [terrData, setTerrData] = useState([]);

    const [selectedTerr, setSelectedTerr] = useState(null);
    const [firstTerr, setFirstTerr] = useState(null);
    const [secondTerr, setSecondTerr] = useState(null);
    const [linePoints, setLinePoints] = useState(null);

    useEffect(()=>{
        async function fetchData() {
            try{
                const res = await fetch('http://localhost:8000/api/list/unit/').then((res)=>{
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

    //Basic implementation as a naive example. Must be changed.
    const handleClick = (territory)=>{
        const [cx, cy] = territories[territory].unitPos;

        if(selectedTerr===null){
            setSelectedTerr(territory);
            setFirstTerr({x: cx, y: cy});
            alert("first click!")
        }else if(selectedTerr === territory){
            setSelectedTerr(null);
            setFirstTerr(null);
            setSecondTerr(null);
            alert("clicked same spot!")
        }else{
            alert("second click:" + territory)
            setSecondTerr({x: cx, y: cy});
            setLinePoints({
                x1: firstTerr.x,
                y1: firstTerr.y,
                x2: cx,
                y2: cy
            });
            setSelectedTerr(null);
            setFirstTerr(null);
            setSecondTerr(null);
            
        }
    };
    
    
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
                onClick={()=>handleClick(id)}
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

        {unitData.filter((u) => {if(game==true) return u.game === Number(id); else return u.sandbox === (Number.id);}).map((unit)=>{
            console.log("Rendering unit at:", unit.territory);
            const territory = territories[unit.territory];
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

        {linePoints!==null && (
            <line
            x1={linePoints.x1}
            y1={linePoints.y1}
            x2={linePoints.x2}
            y2={linePoints.y2}
            stroke="black"
            strokeWidth="2"/>
        )}
        </svg>
        </div>
    );
}

export default Map