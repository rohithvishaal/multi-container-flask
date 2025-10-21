document.addEventListener("DOMContentLoaded", (event) => {
    const quote = document.getElementById("quote")
    const author = document.getElementById("author")

    function loadQuote() {
        fetch("http://localhost/quote").then(response => response.json()).then(data => {
            quote.innerText = data["quote"][2]
            author.innerText = data["quote"][1]
            console.log(data)
        })
    }
    loadQuote()
    const button = document.getElementById("random-quote")
    button.addEventListener("click", loadQuote)
})

