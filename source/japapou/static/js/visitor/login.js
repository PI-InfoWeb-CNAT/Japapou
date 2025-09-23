let card = document.querySelector(".card");
let loginButao = document.querySelector(".loginButao")
let CadastroButao = document.querySelector(".CadastroButao")

loginButao.onclick = () =>{
    card.classList.remove("CadastroActive")
    card.classList.add("LoginActive")
}
CadastroButao.onclick = () =>{
    card.classList.remove("LoginActive")
    card.classList.add("CadastroActive")
}