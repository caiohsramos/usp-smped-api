# Teste da API Eve com autenticação OAuth2

## Execução
Para iniciar os containers
```
docker-compose up
```

## Autenticação
Primeiro temos que criar um código de cliente para a nossa aplicação fictícia. Acessamos `https://localhost:5000/oauth/management`. Autorizamos o acesso inseguro e colocamos as credenciais
```
Usuário: admin
Senha: admin
```
Agora podemos clicar no botão `Add Client` e gerar um novo código de cliente.

Além disso, vamos criar um usuário que terá acesso a API (por meio da aplição fictícia mecionada acima). Preenchemos os campos de clicamos em `Add User`.

## Obter um token
Com o código de cliente e um usuário cadastrado, podemos fazer a requisição de um _token_ usando o método `POST` na url `https://localhost:5000/oauth/token` passando os parâmetros
```
username: <user>
password: <password>
grant_type: "password"
client_id: <client_id>
```

## Operações no banco
Com o token, temos acesso ao banco. Podemos usar o `GET` na URL `https://localhost:5000/` para testar.
### Adicionando uma entrada
Método `POST` na URL `https://localhost:5000/people` passando o JSON
```
{
    "firstname": "Caio",
    "lastname": "Ramos"
}
```
### Recuperando uma entrada
Método `GET` na URL `https://localhost:5000/people/Ramos`

### Deletando/alterando uma entrada
Método `DELETE`/`PATCH`(neste caso com parâmetros) na URL `https://localhost:5000/people/<id>`

# Documentação da API
[Eve - Python](http://python-eve.org)