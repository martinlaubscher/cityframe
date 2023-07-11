import ListItem from "./ListItem"

export default function Droplist (props){

    
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
            <h2>Wow check out this list</h2>
            {items}
        </div>
    )

}