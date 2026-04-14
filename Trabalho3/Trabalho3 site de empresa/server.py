# -*- coding: utf-8 -*-
"""
Servidor local da Async Tecnologia
Python 3 — sem dependências externas
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import hashlib
import re
import uuid
import datetime
import threading

PORT = 3000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
SALT_GLOBAL = "async_salt_2024"

# Lock para thread-safety ao manipular o arquivo de usuários
users_lock = threading.Lock()

# Garante que pasta data e arquivo users.json existem
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        f.write("[]")


def ler_usuarios():
    with users_lock:
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []


def salvar_usuarios(usuarios):
    with users_lock:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=2, ensure_ascii=False)


def hash_senha(senha, salt_usuario=None):
    """
    Gera hash seguro da senha usando salt global + salt individual do usuário.
    Se salt_usuario for None, gera um novo salt.
    """
    if salt_usuario is None:
        salt_usuario = uuid.uuid4().hex[:16]
    hash_final = hashlib.sha256((senha + SALT_GLOBAL + salt_usuario).encode("utf-8")).hexdigest()
    return hash_final, salt_usuario


def resposta_json(handler, status, dados):
    corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(corpo)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(corpo)


def validar_email(email):
    """Validação mais completa de e-mail."""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None


def sanitizar_string(texto, max_len=200):
    """Remove caracteres problemáticos e limita tamanho."""
    if not isinstance(texto, str):
        return ""
    texto = texto.strip()
    if len(texto) > max_len:
        texto = texto[:max_len]
    return texto


def rota_registrar(handler, body):
    nome = sanitizar_string(body.get("nome", ""))
    email = sanitizar_string(body.get("email", "")).lower()
    senha = body.get("senha", "")

    if not nome or not email or not senha:
        return resposta_json(handler, 400, {"erro": "Preencha todos os campos."})

    if len(nome) < 2:
        return resposta_json(handler, 400, {"erro": "Nome muito curto."})

    if not validar_email(email):
        return resposta_json(handler, 400, {"erro": "E-mail inválido."})

    if len(senha) < 6:
        return resposta_json(handler, 400, {"erro": "A senha deve ter pelo menos 6 caracteres."})

    usuarios = ler_usuarios()

    for u in usuarios:
        if u["email"] == email:
            return resposta_json(handler, 409, {"erro": "Este e-mail já está cadastrado."})

    hash_final, salt_usuario = hash_senha(senha)

    novo = {
        "id": str(uuid.uuid4()),
        "nome": nome,
        "email": email,
        "senha": hash_final,
        "salt": salt_usuario,
        "criadoEm": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    usuarios.append(novo)
    salvar_usuarios(usuarios)
    resposta_json(handler, 201, {"mensagem": "Cadastro realizado com sucesso!"})


def rota_login(handler, body):
    email = sanitizar_string(body.get("email", "")).lower()
    senha = body.get("senha", "")

    if not email or not senha:
        return resposta_json(handler, 400, {"erro": "Preencha e-mail e senha."})

    usuarios = ler_usuarios()
    usuario = None
    for u in usuarios:
        if u["email"] == email:
            # Usa o salt do usuário para verificar a senha
            hash_informado, _ = hash_senha(senha, u.get("salt", ""))
            if u["senha"] == hash_informado:
                usuario = u
            break

    if not usuario:
        return resposta_json(handler, 401, {"erro": "E-mail ou senha incorretos."})

    resposta_json(handler, 200, {
        "mensagem": "Login realizado com sucesso!",
        "usuario": {"nome": usuario["nome"], "email": usuario["email"]}
    })


class AsyncHandler(SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        if tamanho == 0:
            return resposta_json(self, 400, {"erro": "Corpo da requisição vazio."})

        raw = self.rfile.read(tamanho)
        try:
            body = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return resposta_json(self, 400, {"erro": "JSON inválido."})

        if self.path == "/api/registrar":
            rota_registrar(self, body)
        elif self.path == "/api/login":
            rota_login(self, body)
        else:
            resposta_json(self, 404, {"erro": "Rota não encontrada."})

    def log_message(self, format, *args):
        # Suprime logs de arquivos estáticos, mostra apenas as chamadas de API
        if "/api/" in args[0]:
            print("[API] " + format % args)


def run_server():
    os.chdir(BASE_DIR)
    servidor = HTTPServer(("", PORT), AsyncHandler)
    print("")
    print("  Servidor Async rodando em http://localhost:" + str(PORT))
    print("  Site principal: http://localhost:" + str(PORT) + "/index.html")
    print("  Tela de login:  http://localhost:" + str(PORT) + "/login.html")
    print("")
    print("  Para parar: pressione Ctrl+C")
    print("")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor encerrado.")


if __name__ == "__main__":
    run_server()
