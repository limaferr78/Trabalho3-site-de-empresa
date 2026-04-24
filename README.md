# Async Tecnologia — Servidor Local

Sistema de login e cadastro com servidor HTTP local em Python 3.

Trabalho simples para a faculdade

## Requisitos

- Python 3.6 ou superior
- Navegador moderno (Chrome, Firefox, Edge, Safari)

## Como executar

1. Abra o terminal na pasta do projeto
2. Execute o servidor:
   ```bash
   python server.py
   ```
3. Acesse no navegador:
   - Site: http://localhost:3000/index.html
   - Login: http://localhost:3000/login.html

## Estrutura do projeto

```
.
├── server.py          # Servidor HTTP (Python 3)
├── index.html         # Página principal
├── login.html         # Página de login/cadastro
├── css/
│   └── style.css      # Estilos
├── js/
│   └── main.js        # JavaScript do menu e autenticação
├── data/
│   └── users.json     # Banco de dados de usuários
└── images/            # Imagens do site
```

## Funcionalidades

- **Cadastro de usuários**: nome, e-mail e senha (mínimo 6 caracteres)
- **Login**: autenticação com e-mail e senha
- **Hash de senha**: cada usuário tem um *salt* único + *salt* global
- **Thread-safe**: proteção contra corrupção do JSON com requisições simultâneas
- **Validação**: e-mail válido, campos obrigatórios

## API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/registrar` | Cadastra novo usuário |
| POST | `/api/login` | Autentica usuário |

## Melhorias implementadas

1. **Migração Python 2 → 3**: usa `http.server` em vez de `BaseHTTPServer`
2. **Segurança**: *hash* de senha com *salt* individual por usuário
3. **Thread-safety**: *lock* para acesso ao arquivo JSON
4. **Validação**: melhor validação de e-mail e sanitização de entradas
5. **Organização**: JavaScript unificado no main.js

## Para parar o servidor

Pressione `Ctrl+C` no terminal.
