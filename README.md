# DTA Samples
Esse repositório tem como objetivo disponibilizar diferentes soluções com I.A. utilizando integração com a plataforma **DTA**. Os exemplos disponibilizados aqui possuem também integração com o **DTA Monitor** a fim de melhorar a observabilidade da sua aplicação e facilitar na sua jornada de desenvolvimento. Para reproduzir esses exemplos, você precisará de uma chave válida no DTA.
> Você pode acessar o DTA [aqui](http://dta.totvs.ai/).

> Entre em contato com o time IDeIA para mais informações ou liberação de acessos.

## O que é o DTA?
O **DTA - Digital Trusted Advisor -** é o nome oficial da plataforma que **consolida todo e qualquer projeto que envolva I.A. na TOTVS**. Ele é capaz de **facilitar a criação e implementação de novas iniciativas com I.A**, tanto como ferramenta de produtividade, quanto como uma solução embarcada nos produtos **TOTVS**.

## Pré-requisitos

 - Python >= 3.10.0
 - [Poetry](https://python-poetry.org/) >= 1.0.0
 > Você precisará de uma chave válida no DTA. Acesse no [DTA UI](http://dta.totvs.ai/) para gerar sua chave.

 > O Poetry pode ser instalado facilmente utilizando o comando: `pip install poetry`

### Recommendations
*  [ASDF](https://asdf-vm.com/#/core-manage-asdf?id=install) - para instalar e gerenciar diferentes versões do Python
*  [Direnv](https://github.com/asdf-community/asdf-direnv) - para gerenciar automaticamente múltiplos ambientes virtuais

## Introdução
O repositório possui duas aplicações de exemplo de soluções com A.I. utilizando Python. Cada uma delas está dentro de diferentes pastas na raíz do projeto (`conversation-tools` e `prompt`).

1.  **Aplicação "conversation-tools":**
É um cliente conversacional que é capaz de realizar chamadas à diferentes endpoints para responder determinada requisição do usuário. Esse exemplo utiliza a biblioteca [LangGraph](https://langchain-ai.github.io/langgraph/)🦜🕸️, nela é possível definir endpoints de serviços externos para "resolver" um requisição que precisa de informações complementares ou executar uma ação que um modelo generativo não conseguiria sozinho. Como por exemplo: previsão de tempo, consulta de estoque de determinado produto, envio de e-mails, etc.
<img width="1068" alt="image" src="https://github.com/user-attachments/assets/21af445d-ff34-4ce6-bf28-1a4427e66a20">

2.  **Aplicação "prompt":**
A aplicação "prompt" é uma ferramenta que gera textos de marketing institucionais para determinado produto. Nela é possível selecionar alguns produtos de exemplo, o idioma do texto a ser gerado, a finalidade do texto (texto para um email de divulgação ou para uma postagem em alguma rede social, por exemplo) e realizar uma análise de mercado do público alvo. Esse exemplo simples de utilização de prompts pré definidos para solicitar ao DTA a geração do texto com base em diferentes parâmetros.
<img width="1108" alt="image" src="https://github.com/user-attachments/assets/681f2720-bc0e-47f0-ac45-6596f6a15f9c">


## Instalação

 1. Clone o projeto com:
	```shell
	git clone git@github.com:totvs-ai/dta-samples.git
	```
 2. Acesse o projeto e então a pasta do app que deseja executar (`conversation-tools` ou `prompt`)
 3. Caso não esteja utilizando [Direnv](https://github.com/asdf-community/asdf-direnv), ative seu ambiente virtual com:
	 - **Linux/MacOS:**
		```shell
		pyhton -m venv .venv
		source .venv/bin/activate
		```
	- **Windows:**
		```shell
		pyhton -m venv .venv
		source .venv/Scripts/activate
		```
4. Instale o Poetry, caso não possua:
	```shell
	pip install poetry
	```
5. Instale as dependencias com:
	```shell
	poetry install
	```

## Execução
Para executar a aplicação após a instalação das dependências, crie um arquivo chamado `.env` dentro da pasta do APP e copie o conteudo do arquivo `.env-template` para dentro dele `.env`, e então adicione sua chave do DTA na variavel `DTA_PROXY_KEY`. Você também pode colocar a sua Secret Key e Public Key gerada no DTA Monitor para obter uma observabilidade detalhada das suas interações com os APP.

Com as dependencias instalad e o seu arquivo `.env` devidamente criado, basta rodar o seguinte comando dentro da pasta do APP desejado para executá-lo:
```shell
python run.py
```
Esse comando iniciará uma aplicação Flask, que disponibilizará uma UI e a API. É possível executar todos os exemplos de APP simultaneamente, já que cada APP ficará disponível em portas diferentes, conforme tabela abaixo:
|App                |Pasta                   |Endereço                |
|-------------------|------------------------|------------------------|
|Conversation Tools |`./conversation-tools`  |http://127.0.0.1:5000   |
|Prompts            |`./prompt`              |http://127.0.0.1:5003   |

