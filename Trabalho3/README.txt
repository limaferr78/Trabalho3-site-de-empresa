# Async Tecnologia — Servidor Python 2.7

## Como rodar

A princípio precisará ter instalado no pc o Python 2.7 

### 1. Abra o PowerShell ou Prompt de Comando na pasta do projeto

Clique com o botão direito dentro da pasta enquanto segura Shift,
e escolha "Abrir janela do PowerShell aqui"
(ou "Abrir janela de comando aqui")

### 2. Execute o servidor

```
python server.py
```

### 3. Acesse no navegador

- Site principal: http://localhost:3000/index.html
- Tela de login:  http://localhost:3000/login.html

### 4. Para parar o servidor

Pressione Ctrl+C no terminal

---

## Estrutura

```
/
├── server.py          ← Servidor Python (sem dependências extras)
├── index.html         ← Página principal
├── login.html         ← Tela de login e cadastro
├── css/style.css      ← Estilos
├── js/main.js         ← JS do site
├── images/            ← Imagens e SVGs
└── data/
    └── users.json     ← Usuários cadastrados (criado automaticamente)
```

## Como funciona

- Dados salvos em data/users.json
- Senhas armazenadas com hash SHA-256 (nunca em texto puro)
- Sessão via sessionStorage — dura enquanto a aba estiver aberta
- Nome do usuário aparece no header após login
