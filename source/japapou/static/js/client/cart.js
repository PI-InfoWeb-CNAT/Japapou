const elementoSelect = document.getElementsByClassName("frete-dropdown");

const opcoes = elementoSelect[0].options;

const totalValor = document.getElementsByClassName("total-valor")[0]

console.log(opcoes);
for (let i=0; i < opcoes.length; i++) {
    const opcaoAtual = opcoes[i];

    console.log(`Opção ${i + 1}: Texto é "${opcaoAtual.textContent}" e Valor é "${opcaoAtual.value}"`);
}



