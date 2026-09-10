"use strict";


const CHAVE_TOKEN = "cvauto_token";
const CHAVE_TEMA = "cvauto_tema";

function aplicarTemaSalvo() {
  const tema = localStorage.getItem(CHAVE_TEMA) || "escuro";
  document.documentElement.setAttribute("data-tema", tema);
}

function tituloBotaoTema(tema) {
  return tema === "escuro" ? "Mudar pra modo claro" : "Mudar pra modo escuro";
}

function atualizarBotaoTema() {
  const botao = document.getElementById("botao-tema");
  if (!botao) return;
  const tema = document.documentElement.getAttribute("data-tema") || "escuro";
  botao.title = tituloBotaoTema(tema);
  botao.setAttribute("aria-label", tituloBotaoTema(tema));
}

function alternarTema() {
  const atual = document.documentElement.getAttribute("data-tema") || "escuro";
  const novo = atual === "escuro" ? "claro" : "escuro";
  document.documentElement.setAttribute("data-tema", novo);
  localStorage.setItem(CHAVE_TEMA, novo);
  atualizarBotaoTema();
}

function inicializarBotaoTema() {
  const botao = document.getElementById("botao-tema");
  if (!botao) return;
  atualizarBotaoTema();
  botao.addEventListener("click", alternarTema);
}

aplicarTemaSalvo();
document.addEventListener("DOMContentLoaded", inicializarBotaoTema);

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

async function irParaTelaCorreta() {
  const lista = await api("/curriculos/");
  if (lista.length === 0) {
    window.location.href = "criar-curriculo.html";
  } else {
    window.location.href = "builder.html";
  }
}
