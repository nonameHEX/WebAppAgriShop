window.onload = function () {
    let suffix = window.location.pathname

    //check pages that interact with cart
    if (suffix == '/' || suffix == '/cart') {

        // keep scroll position
        let scrollpos = localStorage.getItem('scrollpos')
        if (scrollpos) {
            window.scrollTo(0, scrollpos);// go to saved scroll pos
            localStorage.removeItem('scrollpos') //remove scroll pos
        }

        // save scroll poss
        window.onbeforeunload = function (e) {
            localStorage.setItem('scrollpos', window.scrollY)
        };
    }
    updateCartCountText() //update product count in navbar
}

function updateCartCountText() {
    let cart = document.getElementById("cart")
    let productCount = `\n(${products.length})`

    if (products.length == 0) {
        cart.innerText = cart.innerText.replace(productCount, '') // remove product count from nav
    } else {
        if (cart != null) if (!cart.innerText.includes(productCount)) {
            cart.innerText += productCount // add product count to nav
        }
    }
}

// implement auto scroll on "Add to cart" buttons via event listener
let add_to_cart = document.getElementsByClassName("add_to_cart")
for (let i = 0; i < add_to_cart.length; i++) add_to_cart[i].addEventListener("click", function () {
    localStorage.setItem('scrollpos', window.scrollY)

    let with_service = add_to_cart[i].parentNode.children[3].children[1].checked

    //send service checkbox value
    $.ajax({
        url: '/cart/add/service', type: 'POST', data: {"with_service": with_service}
    }).done(function () {
        //trigger route
        let add = add_to_cart[i].previousElementSibling
        add.click()
    });
})

// add counter to prevent recursion
let counter = 0;
// add ajax call to machine detail page
if (window.location.pathname.split("/")[1] == 'detail' && counter == 0) {
    let add_from_detail = document.getElementsByClassName("btn")[0]
    add_from_detail.addEventListener("click", function () {
        let with_service = add_from_detail.parentNode.children[1].children[1].checked
        let form = add_from_detail.parentNode;
        //send service checkbox value
        $.ajax({
            url: '/cart/add/service', type: 'POST', data: {"with_service": with_service}
        }).done(function () {
            //trigger route
            form.submit()
            counter++
        });
    })
}

// change service option value from cart
let cart_checkbox = document.getElementsByClassName("cart_checkbox")
for (let i = 0; i < cart_checkbox.length; i++) cart_checkbox[i].addEventListener("click", function () {
    //send service checkbox value
    let with_service = cart_checkbox[i].checked
    $.ajax({
        url: '/cart/update/service', type: 'POST', data: {"with_service": with_service, "index": i}
    }).done(function () {
        //trigger route

    });
})
