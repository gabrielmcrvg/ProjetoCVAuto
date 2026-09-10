"use strict";

function mostrarErroAuth(mensagem) {
  const el = document.getElementById("auth-erro");
  el.textContent = mensagem;
  el.hidden = false;
}

function esconderErroAuth() {
  document.getElementById("auth-erro").hidden = true;
}

async function loginComCredenciais(email, senha) {
  const corpo = new URLSearchParams();
  corpo.set("username", email);
  corpo.set("password", senha);
  const resposta = await fetch("/usuarios/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: corpo,
  });
  const dados = await resposta.json().catch(() => null);
  if (!resposta.ok) {
    throw new Error((dados && dados.detail) || "Nao foi possivel entrar");
  }
  salvarToken(dados.access_token);
}

async function verificarSessaoExistente() {
  if (!obterToken()) return;
  try {
    await api("/usuarios/me");
    await irParaTelaCorreta();
  } catch (erro) {
    if (erro.status === 401) {
      limparToken();
    }
  }
}

document.getElementById("form-login").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  esconderErroAuth();
  const email = document.getElementById("login-email").value;
  const senha = document.getElementById("login-senha").value;
  try {
    await loginComCredenciais(email, senha);
    await irParaTelaCorreta();
  } catch (erro) {
    mostrarErroAuth(erro.message);
  }
});

document.getElementById("form-registro").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  esconderErroAuth();
  const email = document.getElementById("registro-email").value;
  const senha = document.getElementById("registro-senha").value;
  try {
    await api("/usuarios/registrar", { method: "POST", body: { email, senha } });
    await loginComCredenciais(email, senha);
    await irParaTelaCorreta();
  } catch (erro) {
    mostrarErroAuth(erro.message);
  }
});

document.getElementById("ir-para-registro").addEventListener("click", (ev) => {
  ev.preventDefault();
  document.getElementById("form-login").hidden = true;
  document.getElementById("form-registro").hidden = false;
  esconderErroAuth();
});

document.getElementById("ir-para-login").addEventListener("click", (ev) => {
  ev.preventDefault();
  document.getElementById("form-registro").hidden = true;
  document.getElementById("form-login").hidden = false;
  esconderErroAuth();
});

verificarSessaoExistente();
