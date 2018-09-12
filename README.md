# API do backend
[![pipeline status](https://gitlab.com/LABXP2018/smped-api/badges/master/pipeline.svg)](https://gitlab.com/LABXP2018/smped-api/commits/master)
## Obtenção de token
O token é criado com o método `POST` na rota `/auth/tokens` passando um JSON com o formato:
```
{
    "username": "<user>",
    "password": "<passwd>"
}
```
ou com um `POST` em `/auth/refresh` passando o `refresh_token`:
```
{
    "access_token": "<token>"
}
```
Como retorno temos:
```
{
    "access_token": "<token>",
    "refresh_token": "<token>" (só com user/passwd)
}
```
que são tokens do tipo JWT que decodificados contém informações sobre as _roles_ no formato a seguir:
```
{
    "sub": "refresh | authentication ",
    "exp": "<datetime com a validade do token>",
    "username": "<username>",
    "role": [<roles>]
}
```
## Criação de usuários
Somente um usuário com a _role_ `admin` ou `superuser` pode manipular ou acessar a _collection_ `accounts`. Temos um usuário administrador já no banco que está especificado no arquivo _secrets_ do Google Drive. Além disso temos um usuário com a _role_ "user" com as credenciais:
```
Username: user
Password: password
```

Com o _token_ do usuário administrador, podemos criar um usuário com o método `POST` em `/accounts` seguindo o seguinte formato:
```
'username': {
    'type': 'string',
    'minlength': 1,
    'required': True,
    'unique': True,
},
'password': {
    'type': 'string',
    'minlength': 5,
    'required': True,
},
'email': {
    'type': 'email',
    'minlength': 3,
    'required': True,
    'unique': True,
},
'roles':{
    'type': 'list',
    'allowed': ['user', 'superuser', 'admin'],
    'required': True,
}
```
Podemos também usar os métodos `PATCH` e `DELETE` em `/accounts/:id` para editar e deletar um usuário passando o JSON com o formato acima.

