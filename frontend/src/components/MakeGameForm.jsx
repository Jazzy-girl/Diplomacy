import { useState } from "react"
import { useNavigate } from "react-router-dom";

function MakeGameForm(){
    const [name, setName] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) =>{
        e.preventDefault();
        const newGame = {name};
        try{
            const res = await fetch('http://localhost:8000/api/create/game/',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newGame)
            });
            if(!res.ok) throw new Error(res.status);
            console.log('Game created!!');
            setName('');
            const data = await res.json();
            const gameId = data.id;
            navigate(`/game/ID/${gameId}`);
        }catch (error){
            console.error();
        }
        
    }

    return(
        <form onSubmit={handleSubmit}>
            <label >New Game</label>
            <label >Title: <input
            type="text"
            value={name}
            onChange={(e)=>setName(e.target.value)}
            /></label>
            <button type="submit">Create Game</button>
        </form>
    )
}

export default MakeGameForm