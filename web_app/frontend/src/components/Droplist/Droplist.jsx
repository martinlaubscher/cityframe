import ListItem from "./ListItem.jsx"

export default function Droplist (props){

    const oneplace=true //temp variable for if the list is of one place or all of them. Should be passed in as a prop later
    
    const items=props.results.map(item=> {
        return (item.data.map(hour=> {
            return(
               <ListItem 
               key={[item.id, hour.time]}
               id={item.id}
               data={hour}
               />
            )

        }

        ))})
    
    return(
        <div className="droplist">
            <h2>{oneplace? "Zone Name" : "All Zones"}</h2>
            {items}
        </div>
    )

}