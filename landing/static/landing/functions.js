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