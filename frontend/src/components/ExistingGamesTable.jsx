import { useState, useEffect } from "react";

function ExistingGamesTable() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(()=>{
        async function fetchData(){
            try{
                const res = await fetch('http://localhost:8000/api/games/list/').then((res)=>{
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
                <caption>Existing Games</caption>
                <thead>
                    <tr>
                        <th>Game Id</th>
                        <th>Game Name</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item)=>{return(
                        <tr key={item.id}>
                            <td>{item.id}</td>
                            <td>{item.name}</td>
                        </tr>
                    )})}
                </tbody>
            </table>
        ):(<p>No data available.</p>)}
        </>
    );
}

export default ExistingGamesTable