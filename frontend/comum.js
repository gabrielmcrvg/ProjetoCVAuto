"use strict";

/* ============================================================
   COMUM: token, helpers genericos e cliente de API.
   Carregado por index.html, criar-curriculo.html e builder.html.
   ============================================================ */

const CHAVE_TOKEN = "cvauto_token";

function obterToken() {
  return localStorage.getItem(CHAVE_TOKEN);
}

function salvarToken(tok) {
  localStorage.setItem(CHAVE_TOKEN, tok);
}

function limparToken() {
  localStorage.removeItem(CHAVE_TOKEN);
}

function exigirAutenticacao() {
  if (!obterToken()) {
    window.location.href = "index.html";
    return false;
  }
  return true;
}

function sair() {
  limparToken();
  window.location.href = "index.html";
}

function escapeHtml(texto) {
  if (texto === null || texto === undefined) return "";
  return String(texto)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function mostrarToast(mensagem, erro) {
  const toast = document.getElementById("toast");
  toast.textContent = mensagem;
  toast.classList.toggle("erro", !!erro);
  toast.hidden = false;
  clearTimeout(mostrarToast._timer);
  mostrarToast._timer = setTimeout(() => { toast.hidden = true; }, 3800);
}

async function api(caminho, opcoes) {
  opcoes = opcoes || {};
  const headers = Object.assign({}, opcoes.headers);
  const token = obterToken();
  if (token) headers["Authorization"] = "Bearer " + token;
  let corpo = opcoes.body;
  if (corpo !== undefined && corpo !== null) {
    headers["Content-Type"] = "application/json";
    corpo = JSON.stringify(corpo);
  }
  const resposta = await fetch(caminho, {
    method: opcoes.method || "GET",
    headers: headers,
    body: corpo,
  });
  if (resposta.status === 204) return null;
  let dados = null;
  try { dados = await resposta.json(); } catch (erroJson) { dados = null; }
  if (!resposta.ok) {
    let mensagem = "Erro inesperado (" + resposta.status + ")";
    if (dados && dados.detail) {
      mensagem = typeof dados.detail === "string" ? dados.detail : JSON.stringify(dados.detail);
    }
    const erro = new Error(mensagem);
    erro.status = resposta.status;
    throw erro;
  }
  return dados;
}

/* Decide pra qual tela mandar o usuario logado: se ele ja tem
   currículo, vai direto pro builder; senao, pra tela de criar. */
async function irParaTelaCorreta() {
  const lista = await api("/curriculos/");
  if (lista.length === 0) {
    window.location.href = "criar-curriculo.html";
  } else {
    window.location.href = "builder.html";
  }
}
