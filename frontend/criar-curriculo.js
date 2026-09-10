"use strict";

async function iniciarTelaCriarCurriculo() {
  if (!exigirAutenticacao()) return;
  try {
    const lista = await api("/curriculos/");
    if (lista.length > 0) {
      window.location.href = "builder.html";
    }
  } catch (erro) {
    if (erro.status === 401) {
      limparToken();
      window.location.href = "index.html";
    } else {
      mostrarToast("Não foi possível verificar seus dados agora. Recarregue a página.", true);
    }
  }
}

document.getElementById("form-criar-curriculo").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const payload = {
    titulo: document.getElementById("cc-titulo").value,
    nome_completo: document.getElementById("cc-nome").value,
    localizacao: document.getElementById("cc-localizacao").value,
    telefone: document.getElementById("cc-telefone").value,
    resumo_profissional: document.getElementById("cc-resumo").value,
  };
  try {
    await api("/curriculos/", { method: "POST", body: payload });
    window.location.href = "builder.html";
  } catch (erro) {
    mostrarToast(erro.message, true);
  }
});

document.getElementById("botao-sair").addEventListener("click", () => {
  sair();
});

iniciarTelaCriarCurriculo();
