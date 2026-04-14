(function () {
  // ===== Menu Mobile =====
  var nav = document.querySelector(".nav");
  var toggle = document.querySelector(".nav-toggle");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (window.matchMedia("(max-width: 768px)").matches) {
          nav.classList.remove("is-open");
          toggle.setAttribute("aria-expanded", "false");
          toggle.setAttribute("aria-label", "Abrir menu");
        }
      });
    });
  }

  // ===== Ano no Rodapé =====
  var yearEl = document.getElementById("ano");
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  // ===== Autenticação no Cabeçalho =====
  var loginItem   = document.getElementById("nav-login-item");
  var usuarioItem = document.getElementById("nav-usuario-item");
  var usuarioNome = document.getElementById("nav-usuario-nome");
  var sairBtn     = document.getElementById("nav-sair-btn");

  if (loginItem && usuarioItem && usuarioNome && sairBtn) {
    var nome = sessionStorage.getItem("usuario_nome");

    if (nome) {
      loginItem.style.display = "none";
      usuarioItem.style.display = "flex";
      usuarioItem.style.alignItems = "center";
      usuarioNome.textContent = "Olá, " + nome.split(" ")[0];
    }

    sairBtn.addEventListener("click", function () {
      sessionStorage.removeItem("usuario_nome");
      sessionStorage.removeItem("usuario_email");
      loginItem.style.display = "";
      usuarioItem.style.display = "none";
    });
  }
})();
