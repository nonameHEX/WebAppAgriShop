function toggleMenu(){
    document.getElementById('nav').classList.toggle('visible')
}

document.getElementById("hamburger").addEventListener("click", toggleMenu)

document.getElementById("nav").addEventListener("click", toggleMenu)