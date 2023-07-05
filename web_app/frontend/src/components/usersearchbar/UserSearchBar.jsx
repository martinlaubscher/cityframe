import"./UserSearchBarCSS.css"

export default function UserSearchBar(){
    return (
        <div className="usersearch-container">
            <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasBottom" aria-controls="offcanvasBottom">Toggle bottom offcanvas</button>
                <div class="offcanvas offcanvas-bottom" tabindex="-1" id="offcanvasBottom" aria-labelledby="offcanvasBottomLabel">
                    <div class="offcanvas-header">
                    <h5 class="offcanvas-title" id="offcanvasBottomLabel">Offcanvas bottom</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                  </div>
                <div class="offcanvas-body small">
                     ...
                </div>
            </div>
        </div>
    )
}