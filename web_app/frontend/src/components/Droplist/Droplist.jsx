import ListItem from "./ListItem.jsx"

export default function Droplist (props){

    //const oneplace=true //temp variable for if the list is of one place or all of them. Should be passed in as a prop later
    //console.log("Droplist:", props.results)
    const items=props.results.items.map(item=> {
        const scoreId=props.results.score.find(id=>id.id===item.id)
        return (item.data.map(hour=> {
            const scoreHour=scoreId.data.find(time=>time.time===hour.time)
            return(
               <ListItem 
               key={[item.id, hour.time]}
               id={item.id}
               data={hour}
               score={scoreHour.score}
               />
            )
        }))
    })
    
    return(
        <div className="droplist">
            <h2>{props.results.name}</h2>
            <button onClick={props.hideList}>X</button>
            {items}
        </div>
    )

}