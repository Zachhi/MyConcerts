function changeColor() {
    // change the overall color

    // change the toggle button
    console.log(btn.classList)
    document.getElementById("star-btn").classList.toggle("starred");
    const btn = document.getElementById("star-btn");

    // store what the new mode is
    /*if (localStorage.getItem("star") == "true") {
        localStorage.setItem("star", "false");
        btn.style.color = "gray";
        console.log(btn.value);
    } else {
        localStorage.setItem("star", "true");
        btn.style.color = "yellow";
        console.log(btn.value);
    } */
}