function changeColor() {
    // change the overall color

    // change the toggle button
    
    // document.getElementById("star-btn").classList.toggle("starred");
    btn = document.getElementById("star-btn");
    console.log(btn.classList)
    // store what the new mode is
    if (localStorage.getItem("star") == "true") {
        localStorage.setItem("star", "false");
        btn.style.color = "gray";
        console.log(btn.style.color);
    } else {
        localStorage.setItem("star", "true");
        btn.style.color = "yellow";
        console.log(btn.style.color);
    }
}

function filterTiles(filter) {
    if (filter == "date")
    {

        /*eventsTemp = ticket_master_request('', '', 1, date.today().strftime("%Y-%m-%d"), '', 'x');
        
        localStorage.setItem("events", events);
        console.log(events);
        render(request, "landing/home.html", {"events": event, "page": page, 'title':'Landing'})
        console.log(render);
        */
        updateEvents(request, page, '', '', 1, date.today().strftime("%Y-%m-%d"), '', 'x');
    }
    else if (filter == "distance")
    {
        
    }
    else if (filter == "price")
    {

    }
    else if (filter == "genre")
    {

    }
}