//import ListItem from "./ListItem.jsx"

export default function Droplist (props){
    console.log(props.results)

    //const oneplace=true //temp variable for if the list is of one place or all of them. Should be passed in as a prop later
    //console.log("Droplist:", props.results)
    /*
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
    })*/
    
    return(
        <div className="droplist">
            <h2>{props.results.place.properties.zone}</h2>
            <button onClick={props.hideList}>X</button>
            <h4>Time: {props.results.rank.dt_iso}</h4>
            <h3>rank: {props.results.rank.rank}</h3>
        </div>
    )

}