export default function ListItem (props){
    console.log(props.data.busy)

    function handleClick(){
        console.log("clicked")
    }
    return(
        <div className="listItem" onClick={handleClick}>
            place id={props.id}, time={props.data.time}, busy={props.data.busy}
        </div>
    )

}
