# API Smped
[![pipeline status](https://gitlab.com/LABXP2018/smped-api/badges/master/pipeline.svg)](https://gitlab.com/LABXP2018/smped-api/commits/master)
# Instalação e execução
Para instalar as dependências
```
pip install -r app/requirements.txt
```
Para executar o servidor de desenvolvimento
```
python app/main.py
```
Para executar os testes
```
PYTHONPATH=$PWD/app pytest
```
# Integração contínua
* Os testes são executados para todos os commits feitos, independente da branch.
* As mudanças devem passar pela branch `dev` através de Merge Requests antes de irem para a master.
* O pipeline de `build` e `deploy` só é executado na `master`. A imagem é publicada no _registry_ do GitLab e atualizada no cluster Kubernetes.
# Rotas
## Auth
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
## Accounts
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

Para todos os usuários criados a senha padrão é vazia, e temos uma flag `firstLogin` que indica se o usuário pode modificar sua senha através de um `PATCH` em `/accounts/<id>` sem estar autenticado. Depois desse procedimento, a flag é desabilitada e não se pode mais alterar os dados sem autenticação.

## Forms
A listagem de formulários criados é pública e está disponível em `/forms`. Além disso podemos obter/modificar/deletar informações de um formulário em `/forms/<formid>`, e criar um formulário em `/forms` com o método `POST`. O modelo de JSON é o seguinte:
```
    'version': {
            'type': 'string',
            'required': True
    },
    'owner': {
        'type': 'string',
        'data_relation': {
            'resource': 'accounts',
            'field': 'username',
            'embeddable': True
        },
        'required': True
    },
    'name': {
        'type': 'string',
        'minlength': 5,
        'required': True
    },
    'office': {
        'type': 'string',
        'allowed': ['smped', 'smdhc'],
        'required': True
    },
    'activity': {
        'type': 'string',
        'required': True
    },
    'fields': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                '_id': {
                    'type': 'objectid',
                    'default_setter': 'generateid',
                    'required': True
                },
                'label': {
                    'type': 'string',
                    'required': True,
                },
                'type': {
                    'type': 'string',
                    'allowed': ['number', 'text'],
                    'required': True
                },
                'required': {
                    'type': 'boolean',
                    'required': True
                },
                'order': {
                    'type': 'integer',
                    'required': True
                }
            }
        }
    }
```
## Answers
A rota `/answers` aceita os métodos `GET` e `POST` com autenticação para listagem de criação de respostas para um form. A rota `/answers/<id>` aceita o métodos `GET`, `PATCH` e `DELETE`. O modelo do banco é o seguinte
```
    'form_id': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'forms',
            'field': '_id',
            'embeddable': True
        },
        'required': True
    },
    'email': {
        'type': 'string',
        'regex': r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
        'required': True,
    },
    'values': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'field_id': {
                    'type': 'objectid',
                    'required': True
                },
                'value': {
                    'type': ['string','number'],
                    'required': True
                }
            }
        }
    }
```
## Emails
Para enviar emails, devemos mandar um objeto do tipo
```
{
    "subject": "string",
    "message": "string",
    "emails": ["string"]
}
```
para a rota `/email`, com o método `POST` e com autentição. Um bug presente é que 