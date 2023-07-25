export default function ListItem (props){

    function handleClick(){
        console.log("clicked")
    }
    
    return(
        <div className="listItem" onClick={handleClick}>
            <h4>time: {props.data.time}</h4>
            <h3>Suitability score={props.score}</h3>
            <p>place id={props.id},  busy={props.data.busyness}</p>
        </div>
    )

}
