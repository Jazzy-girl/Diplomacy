import { useState, useEffect } from "react";
import Map from "./Map";
import { Link } from "react-router-dom";
function YourSandboxesTable() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(()=>{
        async function fetchData(){
            try{
                const res = await fetch('http://localhost:8000/api/list/sandbox/').then((res)=>{
                        if(!res.ok){
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return res.json();
                    }
                ).then((data)=>{setData(data);});
                
            }catch (e){
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

    return(
        <>
        {data.length > 0 ? (            <table>
                <caption>Your Sandboxes</caption>
                <thead>
                    <tr>
                        <th>Sandbox Id</th>
                        <th>Sandbox Name</th>
                        <th>Date Created</th>
                        <th>Current Year/Season</th>
                        <th>Link to View Sandbox</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item)=>{return(
                        <tr key={item.id}>
                            <td>{item.id}</td>
                            <td>{item.name}</td>
                            <td>{item.created_date}</td>
                            <td>{`${item.season} ${item.year}`}</td>
                            <th><Link to={`/sandbox/ID/${item.id}`}>View Sandbox</Link></th>
                        </tr>
                    )})}
                </tbody>
            </table>
        ):(<p>No data available.</p>)}
        </>
    );
}

export default YourSandboxesTable