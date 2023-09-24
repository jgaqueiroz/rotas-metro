const mainDiv = document.getElementById('main');
const selectOrigem = document.getElementById('origem');
const selectDestino = document.getElementById('destino');
const blocoDestino = document.getElementById('bloco-destino');
const loading = document.getElementById('loading');

selectOrigem.addEventListener('change', () => {
    // Desabilitando a mesma estação no select de DESTINO
    selectDestino.selectedIndex = 0;
    const selectedText = selectOrigem.options[selectOrigem.selectedIndex].textContent;
    for (let i = 0; i < selectDestino.options.length; i++) {
        const option = selectDestino.options[i];
        if (option.textContent === selectedText || i == 0) {
            option.disabled = true;
        } else {
            option.disabled = false;
        }
    }
    // Exibindo o bloco de DESTINO
    setTimeout(() => {
        blocoDestino.style.display = 'block';
        setTimeout(() => {
            blocoDestino.classList.add('ativo');
        }, 1);
    }, 1);
});

selectDestino.addEventListener('change', () => {
    selectOrigem.disabled = true;
    selectOrigem.style.opacity = .5;
    selectDestino.disabled = true;
    selectDestino.style.opacity = .5;
    loading.style.display = 'inline-block';

    var url = "rota/" + selectOrigem.value + "/" + selectDestino.value;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                mainDiv.innerHTML = xhr.responseText;
            } else {
                console.error("Erro na requisição: " + xhr.status);
            }
        }
    };
    xhr.open("GET", url, true);
    xhr.send();
});