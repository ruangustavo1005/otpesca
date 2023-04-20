# OTPesca

## Descrição

Um bot básico utilizando Python, OpenCV e PyAutoGui para automatizar a pesca

## Pré-requisitos

- Python 3.7 (pode ser instalado pela Microsoft Store)

## Executando

### Pescando

- Deixe o OTPokémon aberto
- Nas configurações, aba "Interface", altere a Opacidade para 100%
- Habilite a barra de pesca e deixe a mesma em cima da água
- Habilite também a aba de batalha, e deixe habilitada somente a opção "Esconder Pokémon Selvagem"
![Exemplo de Battle](README/Exemplo%20Battle.jpg)
- Basta executar o arquivo `exe.bat`
- Com ele em execução, basta segurar a tecla "PAUSE" para que ele seja iniciado. Após isso, o bot pode ser pausado utilizando a tecla "PAUSE" por alguns segundos

### Captura automática de pokémons

- Você pode utilizar a pokebola que preferir
- Configure uma pokebola na barra de atalhos inferior, e atribua a tecla a tecla "P" a ela
- Com isso, ele deve automatizar a pesca dos pokemons que você configurar na pasta `img/pokes` (você pode copiar as imagens da pasta `img/pokes.exe` para ter uma base e criar novas como preferir)
- Para adicionar mais pokemons à lista de capturáveis, adicione um print do mesmo à pasta `img/pokes` e adicione um registro de configurações para o mesmo no arquivo `capturaveis.json`
- Atenção ao adicionar o print, ele deve ser feito com cautela e deve conter apenas detalhes do pokemon, evitando pedaços do chão ou árvores no print (pescar em locais com árvores pode atrapalhar a execução dessa etapa)
- No console, são exibidos os limiares de captura à cada tick de execução do programa. Você pode usar isso para refinar as configurações de captura de cada pokémon