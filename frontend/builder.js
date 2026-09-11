"use strict";


let usuarioEmail = null;
let curriculo = null;
let secoesAbertas = new Set(["dados-pessoais", "formacoes"]);
let estadoEdicao = {
  formacoes: null,
  experiencias: null,
  projetos: null,
  idiomas: null,
  certificados: null,
  habilidades: null,
};

const SITUACOES_FORMACAO = ["Concluído", "Em andamento", "Trancado", "Incompleto"];

const CATEGORIAS_HABILIDADE = [
  "Linguagens de Programação", "Frameworks & Bibliotecas", "Arquitetura de Software",
  "Banco de Dados", "Nuvem & DevOps", "Controle de Versão",
  "Segurança da Informação", "Redes & Infraestrutura",
  "Análise de Dados & BI", "Design & Criatividade", "Marketing & Vendas",
  "Gestão & Liderança", "Finanças & Contabilidade", "Atendimento ao Cliente",
  "Metodologias & Processos", "Ferramentas de Escritório", "Habilidades Interpessoais",
  "Saúde & Cuidados", "Educação & Ensino", "Jurídico & Compliance", "Outras",
];

const CONFIG_SECOES = {
  formacoes: {
    titulo: "Formação Acadêmica",
    campos: [
      { nome: "curso", label: "Curso", tipo: "text" },
      { nome: "instituicao", label: "Instituição", tipo: "text" },
      { nome: "ano_inicio", label: "Ano de início", tipo: "number" },
      { nome: "ano_conclusao", label: "Ano de conclusão", tipo: "number", opcional: true, ajuda: "Deixe vazio se ainda não concluiu", mostraSe: { valor: "Concluído" } },
      { nome: "situacao", label: "Situação", tipo: "select", opcoes: SITUACOES_FORMACAO, controlaCampo: "ano_conclusao" },
    ],
    linhaResumo: (item) => `<strong>${escapeHtml(item.curso)}</strong><span>${escapeHtml(item.instituicao)} · ${escapeHtml(item.situacao)}</span>`,
  },
  experiencias: {
    titulo: "Experiência Profissional",
    campos: [
      { nome: "cargo", label: "Cargo", tipo: "text" },
      { nome: "empresa", label: "Empresa", tipo: "text" },
      { nome: "data_inicio", label: "Data de início", tipo: "date" },
      { nome: "em_andamento", label: "Emprego atual (em andamento)", tipo: "checkbox", controlaCampo: "data_fim", virtual: true },
      { nome: "data_fim", label: "Data de fim", tipo: "date", opcional: true, ajuda: "Deixe vazio se for o emprego atual", mostraSe: { valor: false } },
      { nome: "descricao", label: "Descrição (uma linha por marcador)", tipo: "textarea" },
    ],
    linhaResumo: (item) => `<strong>${escapeHtml(item.cargo)}</strong><span>${escapeHtml(item.empresa)}</span>`,
    reescrever: { campo: "descricao" },
    valorVirtualInicial: (nomeVirtual, item) => nomeVirtual === "em_andamento" ? (item.data_fim === null || item.data_fim === undefined) : undefined,
    transformarPayload: (payload) => {
      const emAndamento = payload.em_andamento;
      const { em_andamento, ...resto } = payload;
      if (emAndamento) resto.data_fim = null;
      return resto;
    },
  },
  projetos: {
    titulo: "Projetos",
    campos: [
      { nome: "nome", label: "Nome do projeto", tipo: "text" },
      { nome: "contexto", label: "Contexto", tipo: "text", ajuda: "Ex: Projeto pessoal de portfólio" },
      { nome: "tecnologias", label: "Tecnologias", tipo: "text" },
      { nome: "descricao", label: "Descrição (uma linha por marcador)", tipo: "textarea" },
      { nome: "link", label: "Link", tipo: "text", opcional: true },
    ],
    linhaResumo: (item) => `<strong>${escapeHtml(item.nome)}</strong><span>${escapeHtml(item.tecnologias)}</span>`,
    reescrever: { campo: "descricao" },
  },
  idiomas: {
    titulo: "Idiomas",
    campos: [
      { nome: "nome", label: "Idioma", tipo: "text" },
      { nome: "nivel", label: "Nível", tipo: "text", ajuda: "Ex: Básico, Intermediário, Avançado, Fluente" },
    ],
    linhaResumo: (item) => `<strong>${escapeHtml(item.nome)}</strong><span>${escapeHtml(item.nivel)}</span>`,
  },
  certificados: {
    titulo: "Certificados e Cursos",
    campos: [
      { nome: "nome", label: "Nome do curso/certificado", tipo: "text" },
      { nome: "instituicao", label: "Instituição", tipo: "text" },
      { nome: "carga_horaria", label: "Carga horária (em horas)", tipo: "number", opcional: true },
      { nome: "periodo", label: "Período", tipo: "text", ajuda: "Ex: 2025" },
      { nome: "em_andamento", label: "Em andamento (ainda não concluí)", tipo: "checkbox", virtual: true },
    ],
    linhaResumo: (item) => `<strong>${escapeHtml(item.nome)}</strong><span>${escapeHtml(item.instituicao)} · ${escapeHtml(item.situacao)}</span>`,
    valorVirtualInicial: (nomeVirtual, item) => nomeVirtual === "em_andamento" ? item.situacao === "Em andamento" : undefined,
    transformarPayload: (payload) => {
      const emAndamento = payload.em_andamento;
      const { em_andamento, ...resto } = payload;
      resto.situacao = emAndamento ? "Em andamento" : "Concluído";
      return resto;
    },
  },
};


function containerIdLista(chave) { return "lista-" + chave; }

function formIdCampo(chave, nomeCampo, modo, itemId) {
  return modo === "novo" ? `novo-${chave}-${nomeCampo}` : `editar-${chave}-${itemId}-${nomeCampo}`;
}


async function iniciarBuilder() {
  if (!exigirAutenticacao()) return;
  try {
    const meusDados = await api("/usuarios/me");
    usuarioEmail = meusDados.email;
    document.getElementById("topo-email").textContent = usuarioEmail;

    const lista = await api("/curriculos/");
    if (lista.length === 0) {
      window.location.href = "criar-curriculo.html";
      return;
    }
    curriculo = await api(`/curriculos/${lista[0].id}`);
    renderEditor();
    renderPreview();
  } catch (erro) {
    if (erro.status === 401) {
      limparToken();
      window.location.href = "index.html";
    } else {
      mostrarToast("Não foi possível carregar seus dados agora. Recarregue a página.", true);
    }
  }
}


function renderEditor() {
  const raiz = document.getElementById("coluna-editor");
  let html = renderizarSecaoDadosPessoais();
  html += renderizarShellSecao("formacoes");
  html += renderizarShellSecao("experiencias");
  html += renderizarShellSecao("projetos");
  html += renderizarShellHabilidades();
  html += renderizarShellSecao("idiomas");
  html += renderizarShellSecao("certificados");
  raiz.innerHTML = html;

  preencherCamposPessoais();

  for (const chave of ["formacoes", "experiencias", "projetos", "idiomas", "certificados"]) {
    document.getElementById(`novo-${chave}`).innerHTML = renderizarFormNovoItem(chave, CONFIG_SECOES[chave]);
    ativarCamposCondicionais(chave, CONFIG_SECOES[chave], "novo");
    renderizarListaSecao(chave);
  }
  renderizarListaHabilidades();
}

function renderizarSecaoDadosPessoais() {
  const aberta = secoesAbertas.has("dados-pessoais") ? "aberta" : "";
  return `
    <div class="secao ${aberta}" data-secao-id="dados-pessoais">
      <div class="secao-cabecalho" data-acao="toggle-secao" data-secao="dados-pessoais">
        <span class="secao-titulo">Dados Pessoais</span>
        <span class="secao-seta">▸</span>
      </div>
      <div class="secao-corpo">
        <label>Título do currículo
          <input type="text" id="dp-titulo">
        </label>
        <label>Nome completo
          <input type="text" id="dp-nome">
        </label>
        <label>Localização
          <input type="text" id="dp-localizacao">
        </label>
        <label>Telefone
          <input type="text" id="dp-telefone">
        </label>
        <label>Link 1 (opcional)
          <input type="text" id="dp-url1" placeholder="https://github.com/seu-usuario">
        </label>
        <label>Link 2 (opcional)
          <input type="text" id="dp-url2" placeholder="https://linkedin.com/in/seu-usuario">
        </label>
        <label>Resumo profissional
          <textarea id="dp-resumo" rows="5"></textarea>
        </label>
        <div class="linha-acoes">
          <button type="button" class="botao-ia" data-acao="reescrever-generico" data-alvo="dp-resumo">Reescrever com IA</button>
          <button type="button" data-acao="salvar-dados-pessoais">Salvar dados pessoais</button>
        </div>
      </div>
    </div>`;
}

function preencherCamposPessoais() {
  document.getElementById("dp-titulo").value = curriculo.titulo || "";
  document.getElementById("dp-nome").value = curriculo.nome_completo || "";
  document.getElementById("dp-localizacao").value = curriculo.localizacao || "";
  document.getElementById("dp-telefone").value = curriculo.telefone || "";
  document.getElementById("dp-url1").value = curriculo.url_1 || "";
  document.getElementById("dp-url2").value = curriculo.url_2 || "";
  document.getElementById("dp-resumo").value = curriculo.resumo_profissional || "";

  const mapaCampos = {
    "dp-titulo": "titulo",
    "dp-nome": "nome_completo",
    "dp-localizacao": "localizacao",
    "dp-telefone": "telefone",
    "dp-url1": "url_1",
    "dp-url2": "url_2",
    "dp-resumo": "resumo_profissional",
  };
  for (const [idCampo, nomeAtributo] of Object.entries(mapaCampos)) {
    document.getElementById(idCampo).addEventListener("input", (ev) => {
      curriculo[nomeAtributo] = ev.target.value;
      renderPreview();
    });
  }
}

async function salvarDadosPessoais() {
  const payload = {
    titulo: curriculo.titulo,
    nome_completo: curriculo.nome_completo,
    localizacao: curriculo.localizacao,
    telefone: curriculo.telefone,
    url_1: curriculo.url_1 || null,
    url_2: curriculo.url_2 || null,
    resumo_profissional: curriculo.resumo_profissional,
  };
  const atualizado = await api(`/curriculos/${curriculo.id}`, { method: "PATCH", body: payload });
  Object.assign(curriculo, atualizado);
  mostrarToast("Dados pessoais salvos.");
}


function renderizarShellSecao(chave) {
  const cfg = CONFIG_SECOES[chave];
  const contagem = (curriculo[chave] || []).length;
  const aberta = secoesAbertas.has(chave) ? "aberta" : "";
  return `
    <div class="secao ${aberta}" data-secao-id="${chave}">
      <div class="secao-cabecalho" data-acao="toggle-secao" data-secao="${chave}">
        <span class="secao-titulo">${escapeHtml(cfg.titulo)} <span class="secao-contagem" id="contagem-${chave}">${contagem}</span></span>
        <span class="secao-seta">▸</span>
      </div>
      <div class="secao-corpo">
        <div id="${containerIdLista(chave)}"></div>
        <div id="novo-${chave}"></div>
      </div>
    </div>`;
}

function renderizarCampoHtml(chave, campo, valorAtual, modo, itemId) {
  const id = formIdCampo(chave, campo.nome, modo, itemId);
  if (campo.tipo === "checkbox") {
    return `<label id="rotulo-${id}" class="campo-checkbox"><input type="checkbox" id="${id}" ${valorAtual ? "checked" : ""}> ${escapeHtml(campo.label)}</label>`;
  }
  const valor = valorAtual === undefined || valorAtual === null ? "" : valorAtual;
  const ajuda = campo.ajuda ? `<div class="campo-ajuda">${escapeHtml(campo.ajuda)}</div>` : "";
  let controle;
  if (campo.tipo === "textarea") {
    controle = `<textarea id="${id}" rows="3">${escapeHtml(valor)}</textarea>`;
  } else if (campo.tipo === "select") {
    const opcoesHtml = campo.opcoes.map(op =>
      `<option value="${escapeHtml(op)}" ${op === valor ? "selected" : ""}>${escapeHtml(op)}</option>`
    ).join("");
    controle = `<select id="${id}">${opcoesHtml}</select>`;
  } else {
    controle = `<input type="${campo.tipo}" id="${id}" value="${escapeHtml(valor)}">`;
  }
  return `<label id="rotulo-${id}">${escapeHtml(campo.label)}${controle}${ajuda}</label>`;
}

function valorInicialCampo(cfg, campo, item) {
  if (campo.tipo === "checkbox" && cfg.valorVirtualInicial && item) {
    const valor = cfg.valorVirtualInicial(campo.nome, item);
    if (valor !== undefined) return valor;
  }
  return item ? item[campo.nome] : "";
}

function ativarCamposCondicionais(chave, cfg, modo, itemId) {
  for (const campoControlador of cfg.campos) {
    if (!campoControlador.controlaCampo) continue;
    const campoAlvo = cfg.campos.find(c => c.nome === campoControlador.controlaCampo);
    if (!campoAlvo || !campoAlvo.mostraSe) continue;
    const elControlador = document.getElementById(formIdCampo(chave, campoControlador.nome, modo, itemId));
    const idAlvo = formIdCampo(chave, campoAlvo.nome, modo, itemId);
    const rotuloAlvo = document.getElementById(`rotulo-${idAlvo}`);
    if (!elControlador || !rotuloAlvo) continue;
    const aplicar = () => {
      const valorControlador = campoControlador.tipo === "checkbox" ? elControlador.checked : elControlador.value;
      const mostrar = valorControlador === campoAlvo.mostraSe.valor;
      rotuloAlvo.style.display = mostrar ? "" : "none";
      if (!mostrar) {
        const elAlvo = document.getElementById(idAlvo);
        if (elAlvo) elAlvo.value = "";
      }
    };
    aplicar();
    elControlador.addEventListener("change", aplicar);
  }
}

function renderizarLinhaItem(chave, cfg, item) {
  return `
    <div class="item-lista">
      <div class="item-lista-topo">
        <div class="item-lista-resumo">${cfg.linhaResumo(item)}</div>
        <div class="item-lista-acoes">
          <button type="button" class="botao-secundario" data-acao="editar" data-secao="${chave}" data-id="${item.id}">Editar</button>
          <button type="button" class="botao-perigo" data-acao="excluir" data-secao="${chave}" data-id="${item.id}">Excluir</button>
        </div>
      </div>
    </div>`;
}

function renderizarFormItem(chave, cfg, item) {
  const camposHtml = cfg.campos.map(c => renderizarCampoHtml(chave, c, valorInicialCampo(cfg, c, item), "editar", item.id)).join("");
  let reescreverHtml = "";
  if (cfg.reescrever) {
    const idCampo = formIdCampo(chave, cfg.reescrever.campo, "editar", item.id);
    reescreverHtml = `<button type="button" class="botao-ia" data-acao="reescrever-generico" data-alvo="${idCampo}">Reescrever com IA</button>`;
  }
  return `
    <div class="item-lista">
      <div class="item-lista-form">
        ${camposHtml}
        ${reescreverHtml}
        <div class="linha-acoes">
          <button type="button" data-acao="salvar-edicao" data-secao="${chave}" data-id="${item.id}">Salvar</button>
          <button type="button" class="botao-secundario" data-acao="cancelar-edicao" data-secao="${chave}" data-id="${item.id}">Cancelar</button>
        </div>
      </div>
    </div>`;
}

function renderizarFormNovoItem(chave, cfg) {
  const camposHtml = cfg.campos.map(c => renderizarCampoHtml(chave, c, "", "novo")).join("");
  let reescreverHtml = "";
  if (cfg.reescrever) {
    const idCampo = formIdCampo(chave, cfg.reescrever.campo, "novo");
    reescreverHtml = `<button type="button" class="botao-ia" data-acao="reescrever-generico" data-alvo="${idCampo}">Reescrever com IA</button>`;
  }
  return `
    <div class="form-novo-item">
      <div class="secao-titulo" style="margin-bottom:10px;">Adicionar</div>
      ${camposHtml}
      ${reescreverHtml}
      <button type="button" data-acao="adicionar" data-secao="${chave}">Adicionar</button>
    </div>`;
}

function renderizarListaSecao(chave) {
  const cfg = CONFIG_SECOES[chave];
  const container = document.getElementById(containerIdLista(chave));
  const itens = curriculo[chave] || [];
  if (itens.length === 0) {
    container.innerHTML = `<p class="preview-vazio">Nada cadastrado ainda.</p>`;
    return;
  }
  container.innerHTML = itens.map(item => {
    return estadoEdicao[chave] === item.id
      ? renderizarFormItem(chave, cfg, item)
      : renderizarLinhaItem(chave, cfg, item);
  }).join("");
  if (estadoEdicao[chave] != null) {
    ativarCamposCondicionais(chave, cfg, "editar", estadoEdicao[chave]);
  }
}

function atualizarContagemSecao(chave) {
  const el = document.getElementById(`contagem-${chave}`);
  if (el) el.textContent = String((curriculo[chave] || []).length);
}

function valorDoCampo(chave, campo, modo, itemId) {
  const el = document.getElementById(formIdCampo(chave, campo.nome, modo, itemId));
  if (campo.tipo === "checkbox") {
    return el.checked;
  }
  let valor = el.value;
  if (campo.tipo === "number") {
    return valor === "" ? null : Number(valor);
  }
  if (campo.opcional && valor === "") {
    return null;
  }
  return valor;
}

function validarCamposObrigatorios(cfg, chave, modo, itemId) {
  for (const campo of cfg.campos) {
    if (campo.opcional || campo.tipo === "checkbox") continue;
    const el = document.getElementById(formIdCampo(chave, campo.nome, modo, itemId));
    if (String(el.value).trim() === "") {
      mostrarToast(`Preencha o campo "${campo.label}".`, true);
      return false;
    }
  }
  return true;
}

async function adicionarItem(chave) {
  const cfg = CONFIG_SECOES[chave];
  if (!validarCamposObrigatorios(cfg, chave, "novo")) return;
  let payload = {};
  for (const campo of cfg.campos) {
    payload[campo.nome] = valorDoCampo(chave, campo, "novo");
  }
  if (cfg.transformarPayload) payload = cfg.transformarPayload(payload);
  const criado = await api(`/curriculos/${curriculo.id}/${chave}/`, { method: "POST", body: payload });
  curriculo[chave].push(criado);
  renderizarListaSecao(chave);
  atualizarContagemSecao(chave);
  renderPreview();
  document.getElementById(`novo-${chave}`).innerHTML = renderizarFormNovoItem(chave, cfg);
  ativarCamposCondicionais(chave, cfg, "novo");
  mostrarToast("Adicionado.");
}

async function salvarEdicaoItem(chave, itemId) {
  const cfg = CONFIG_SECOES[chave];
  if (!validarCamposObrigatorios(cfg, chave, "editar", itemId)) return;
  let payload = {};
  for (const campo of cfg.campos) {
    payload[campo.nome] = valorDoCampo(chave, campo, "editar", itemId);
  }
  if (cfg.transformarPayload) payload = cfg.transformarPayload(payload);
  const atualizado = await api(`/curriculos/${curriculo.id}/${chave}/${itemId}`, { method: "PATCH", body: payload });
  const lista = curriculo[chave];
  const indice = lista.findIndex(i => i.id === itemId);
  if (indice >= 0) lista[indice] = atualizado;
  estadoEdicao[chave] = null;
  renderizarListaSecao(chave);
  renderPreview();
  mostrarToast("Alterações salvas.");
}

async function excluirItem(chave, itemId) {
  if (!window.confirm("Tem certeza que quer excluir este item?")) return;
  await api(`/curriculos/${curriculo.id}/${chave}/${itemId}`, { method: "DELETE" });
  curriculo[chave] = curriculo[chave].filter(i => i.id !== itemId);
  if (chave === "habilidades") {
    renderizarListaHabilidades();
  } else {
    renderizarListaSecao(chave);
  }
  atualizarContagemSecao(chave);
  renderPreview();
  mostrarToast("Excluído.");
}


async function reescreverTextoGenerico(elementoId, botao) {
  const campo = document.getElementById(elementoId);
  if (!campo) return;
  const textoOriginal = campo.value.trim();
  if (!textoOriginal) {
    mostrarToast("Escreva algo antes de pedir pra IA reescrever.", true);
    return;
  }
  const rotuloOriginal = botao.textContent;
  botao.disabled = true;
  botao.textContent = "Consultando IA...";
  try {
    const resposta = await api("/ia/reescrever", { method: "POST", body: { texto: textoOriginal } });
    campo.value = resposta.texto_sugerido;
    campo.dispatchEvent(new Event("input", { bubbles: true }));
    mostrarToast("Texto reescrito pela IA. Revise antes de salvar.");
  } catch (erro) {
    mostrarToast("Não foi possível consultar a IA agora: " + erro.message, true);
  } finally {
    botao.disabled = false;
    botao.textContent = rotuloOriginal;
  }
}


function renderizarShellHabilidades() {
  const aberta = secoesAbertas.has("habilidades") ? "aberta" : "";
  const contagem = (curriculo.habilidades || []).length;
  return `
    <div class="secao ${aberta}" data-secao-id="habilidades">
      <div class="secao-cabecalho" data-acao="toggle-secao" data-secao="habilidades">
        <span class="secao-titulo">Habilidades <span class="secao-contagem" id="contagem-habilidades">${contagem}</span></span>
        <span class="secao-seta">▸</span>
      </div>
      <div class="secao-corpo">
        <div class="linha-acoes" style="margin-bottom:10px;">
          <button type="button" class="botao-ia" data-acao="categorizar-habilidades">Categorizar com IA</button>
        </div>
        <div id="lista-habilidades"></div>
        <div id="sugestoes-categoria" class="lista-sugestoes-categoria"></div>
        <div class="form-novo-item">
          <label>Nova habilidade
            <input type="text" id="novo-habilidade-nome" placeholder="Ex: Python">
          </label>
          <button type="button" data-acao="adicionar-habilidade">Adicionar</button>
        </div>
      </div>
    </div>`;
}

function renderizarFormEdicaoHabilidade(item) {
  const opcoesHtml = CATEGORIAS_HABILIDADE.map(c =>
    `<option value="${escapeHtml(c)}" ${c === item.categoria ? "selected" : ""}>${escapeHtml(c)}</option>`
  ).join("");
  return `
    <div class="item-lista">
      <div class="item-lista-form">
        <label>Nome
          <input type="text" id="editar-habilidade-${item.id}-nome" value="${escapeHtml(item.nome)}">
        </label>
        <label>Categoria
          <select id="editar-habilidade-${item.id}-categoria">
            <option value="">Sem categoria</option>
            ${opcoesHtml}
          </select>
        </label>
        <div class="linha-acoes">
          <button type="button" data-acao="salvar-edicao-habilidade" data-id="${item.id}">Salvar</button>
          <button type="button" class="botao-secundario" data-acao="cancelar-edicao" data-secao="habilidades" data-id="${item.id}">Cancelar</button>
        </div>
      </div>
    </div>`;
}

function renderizarListaHabilidades() {
  const container = document.getElementById("lista-habilidades");
  const itens = curriculo.habilidades || [];
  if (itens.length === 0) {
    container.innerHTML = `<p class="preview-vazio">Nenhuma habilidade cadastrada ainda.</p>`;
    return;
  }
  container.innerHTML = itens.map(h => {
    if (estadoEdicao.habilidades === h.id) return renderizarFormEdicaoHabilidade(h);
    const chip = h.categoria
      ? `<span class="chip-categoria">${escapeHtml(h.categoria)}</span>`
      : `<span class="chip-sem-categoria">sem categoria</span>`;
    return `
      <div class="item-lista">
        <div class="item-lista-topo">
          <div class="item-lista-resumo"><strong>${escapeHtml(h.nome)}</strong>${chip}</div>
          <div class="item-lista-acoes">
            <button type="button" class="botao-secundario" data-acao="editar-habilidade" data-id="${h.id}">Editar</button>
            <button type="button" class="botao-perigo" data-acao="excluir" data-secao="habilidades" data-id="${h.id}">Excluir</button>
          </div>
        </div>
      </div>`;
  }).join("");
}

async function adicionarHabilidade() {
  const el = document.getElementById("novo-habilidade-nome");
  const nome = el.value.trim();
  if (!nome) {
    mostrarToast("Digite o nome da habilidade.", true);
    return;
  }
  const criado = await api(`/curriculos/${curriculo.id}/habilidades/`, { method: "POST", body: { nome } });
  curriculo.habilidades.push(criado);
  renderizarListaHabilidades();
  atualizarContagemSecao("habilidades");
  renderPreview();
  el.value = "";
  mostrarToast("Habilidade adicionada.");
}

async function salvarEdicaoHabilidade(itemId) {
  const nome = document.getElementById(`editar-habilidade-${itemId}-nome`).value;
  const categoria = document.getElementById(`editar-habilidade-${itemId}-categoria`).value || null;
  if (!nome.trim()) {
    mostrarToast("O nome da habilidade nao pode ficar vazio.", true);
    return;
  }
  const atualizado = await api(`/curriculos/${curriculo.id}/habilidades/${itemId}`, {
    method: "PATCH",
    body: { nome, categoria },
  });
  const indice = curriculo.habilidades.findIndex(h => h.id === itemId);
  if (indice >= 0) curriculo.habilidades[indice] = atualizado;
  estadoEdicao.habilidades = null;
  renderizarListaHabilidades();
  renderPreview();
  mostrarToast("Habilidade atualizada.");
}

async function categorizarHabilidades() {
  const caixa = document.getElementById("sugestoes-categoria");
  try {
    const sugestoes = await api(`/curriculos/${curriculo.id}/habilidades/categorizar`, { method: "POST" });
    if (!sugestoes || sugestoes.length === 0) {
      mostrarToast("Todas as habilidades já têm categoria.");
      caixa.innerHTML = "";
      return;
    }
    caixa.innerHTML = sugestoes.map(s => {
      const habilidade = curriculo.habilidades.find(h => h.id === s.id);
      const nome = habilidade ? habilidade.nome : ("#" + s.id);
      return `
        <div class="sugestao-categoria-linha" data-linha-id="${s.id}">
          <span><strong>${escapeHtml(nome)}</strong> → ${escapeHtml(s.categoria)}</span>
          <span>
            <button type="button" class="botao-texto" data-acao="aplicar-categoria-sugerida" data-id="${s.id}" data-categoria="${escapeHtml(s.categoria)}">Aplicar</button>
            <button type="button" class="botao-texto" data-acao="descartar-categoria-sugerida" data-id="${s.id}">Descartar</button>
          </span>
        </div>`;
    }).join("");
  } catch (erro) {
    mostrarToast("Não foi possível consultar a IA agora: " + erro.message, true);
  }
}

async function aplicarCategoriaSugerida(itemId, categoria) {
  const atualizado = await api(`/curriculos/${curriculo.id}/habilidades/${itemId}`, {
    method: "PATCH",
    body: { categoria },
  });
  const indice = curriculo.habilidades.findIndex(h => h.id === itemId);
  if (indice >= 0) curriculo.habilidades[indice] = atualizado;
  renderizarListaHabilidades();
  renderPreview();
  const linha = document.querySelector(`.sugestao-categoria-linha[data-linha-id="${itemId}"]`);
  if (linha) linha.remove();
  mostrarToast("Categoria aplicada.");
}


function alternarSecao(chave) {
  if (secoesAbertas.has(chave)) secoesAbertas.delete(chave); else secoesAbertas.add(chave);
  const el = document.querySelector(`.secao[data-secao-id="${chave}"]`);
  if (el) el.classList.toggle("aberta");
}


function formatarDataMesAno(dataIso) {
  if (!dataIso) return null;
  const partes = String(dataIso).split("-");
  if (partes.length < 2) return dataIso;
  return `${partes[1]}/${partes[0]}`;
}

function agruparHabilidades(habilidades) {
  const grupos = {};
  for (const h of habilidades) {
    const chave = h.categoria || "Outras";
    if (!grupos[chave]) grupos[chave] = [];
    grupos[chave].push(h.nome);
  }
  return grupos;
}

function dividirEmLinhas(texto) {
  const linhas = String(texto || "").split("\n").map(l => l.trim()).filter(Boolean);
  if (linhas.length) return linhas;
  return texto ? [texto] : [];
}

function renderPreview() {
  const raiz = document.getElementById("pagina-preview");
  if (!curriculo) { raiz.innerHTML = ""; return; }

  let html = "";
  html += `<h1 class="prev-nome">${escapeHtml(curriculo.nome_completo || "Seu nome")}</h1>`;

  const linhaContato = [curriculo.localizacao, curriculo.telefone, usuarioEmail]
    .filter(Boolean).map(escapeHtml).join(" | ");
  html += `<p class="prev-contato">${linhaContato}</p>`;

  if (curriculo.url_1 || curriculo.url_2) {
    const links = [];
    if (curriculo.url_1) links.push(`<a href="${escapeHtml(curriculo.url_1)}">${escapeHtml(curriculo.url_1)}</a>`);
    if (curriculo.url_2) links.push(`<a href="${escapeHtml(curriculo.url_2)}">${escapeHtml(curriculo.url_2)}</a>`);
    html += `<p class="prev-contato">${links.join(" | ")}</p>`;
  }
  html += `<hr>`;

  html += `<h2>RESUMO PROFISSIONAL</h2>`;
  html += `<p class="prev-paragrafo">${escapeHtml(curriculo.resumo_profissional || "")}</p>`;

  const formacoes = curriculo.formacoes || [];
  if (formacoes.length) {
    html += `<h2>FORMAÇÃO ACADÊMICA</h2>`;
    for (const f of formacoes) {
      const fim = f.ano_conclusao || "Atual";
      html += `<p class="prev-item-titulo">${escapeHtml(f.curso)}</p>`;
      html += `<p class="prev-item-subtitulo">${escapeHtml(f.instituicao)} | ${escapeHtml(f.ano_inicio)} – ${escapeHtml(fim)} (${escapeHtml(f.situacao)})</p>`;
    }
  }

  const experiencias = curriculo.experiencias || [];
  if (experiencias.length) {
    html += `<h2>EXPERIÊNCIA PROFISSIONAL</h2>`;
    for (const e of experiencias) {
      const fim = e.data_fim ? formatarDataMesAno(e.data_fim) : "Atual";
      html += `<p class="prev-item-titulo">${escapeHtml(e.cargo)}</p>`;
      html += `<p class="prev-item-subtitulo">${escapeHtml(e.empresa)} | ${formatarDataMesAno(e.data_inicio)} – ${fim}</p>`;
      const linhas = dividirEmLinhas(e.descricao);
      if (linhas.length) html += `<ul>` + linhas.map(l => `<li>${escapeHtml(l)}</li>`).join("") + `</ul>`;
    }
  }

  const projetos = curriculo.projetos || [];
  if (projetos.length) {
    html += `<h2>PROJETOS</h2>`;
    for (const p of projetos) {
      html += `<p class="prev-item-titulo">${escapeHtml(p.nome)}</p>`;
      let sub = `${escapeHtml(p.contexto)} | ${escapeHtml(p.tecnologias)}`;
      if (p.link) sub += ` | <a href="${escapeHtml(p.link)}">${escapeHtml(p.link)}</a>`;
      html += `<p class="prev-item-subtitulo">${sub}</p>`;
      const linhas = dividirEmLinhas(p.descricao);
      if (linhas.length) html += `<ul>` + linhas.map(l => `<li>${escapeHtml(l)}</li>`).join("") + `</ul>`;
    }
  }

  const habilidades = curriculo.habilidades || [];
  if (habilidades.length) {
    html += `<h2>HABILIDADES TÉCNICAS</h2>`;
    const grupos = agruparHabilidades(habilidades);
    for (const [categoria, nomes] of Object.entries(grupos)) {
      html += `<p class="prev-habilidade-linha"><b>${escapeHtml(categoria)}:</b> ${escapeHtml(nomes.join(", "))}</p>`;
    }
  }

  const certificados = curriculo.certificados || [];
  if (certificados.length) {
    html += `<h2>CERTIFICADOS E CURSOS</h2><ul>`;
    for (const c of certificados) {
      let linha = `<b>${escapeHtml(c.nome)}</b> — ${escapeHtml(c.instituicao)}`;
      if (c.carga_horaria) linha += ` | ${escapeHtml(c.carga_horaria)}h`;
      linha += ` | ${escapeHtml(c.situacao)}`;
      if (c.periodo) linha += ` em ${escapeHtml(c.periodo)}`;
      html += `<li>${linha}</li>`;
    }
    html += `</ul>`;
  }

  const idiomas = curriculo.idiomas || [];
  if (idiomas.length) {
    html += `<h2>IDIOMAS</h2>`;
    for (const i of idiomas) {
      html += `<p class="prev-habilidade-linha"><b>${escapeHtml(i.nome)}:</b> ${escapeHtml(i.nivel)}</p>`;
    }
  }

  raiz.innerHTML = html;
}


function slugificarNomeArquivo(texto) {
  const base = String(texto || "").trim().toLowerCase().replace(/\s+/g, "_");
  const limpo = base.replace(/[\\/:*?"<>|]/g, "");
  return limpo || "curriculo";
}


document.getElementById("botao-sair").addEventListener("click", () => {
  sair();
});

document.getElementById("botao-baixar-pdf").addEventListener("click", async () => {
  try {
    const resposta = await fetch(`/curriculos/${curriculo.id}/pdf`, {
      headers: { Authorization: "Bearer " + obterToken() },
    });
    if (!resposta.ok) throw new Error("Não foi possível gerar o PDF.");
    const blob = await resposta.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${slugificarNomeArquivo(curriculo.titulo)}.pdf`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  } catch (erro) {
    mostrarToast(erro.message, true);
  }
});


document.getElementById("coluna-editor").addEventListener("click", async (ev) => {
  const alvo = ev.target.closest("[data-acao]");
  if (!alvo) return;
  const acao = alvo.dataset.acao;
  const secao = alvo.dataset.secao;
  const id = alvo.dataset.id ? Number(alvo.dataset.id) : null;

  try {
    if (acao === "toggle-secao") {
      alternarSecao(secao);
    } else if (acao === "salvar-dados-pessoais") {
      await salvarDadosPessoais();
    } else if (acao === "reescrever-generico") {
      await reescreverTextoGenerico(alvo.dataset.alvo, alvo);
    } else if (acao === "adicionar") {
      await adicionarItem(secao);
    } else if (acao === "editar") {
      estadoEdicao[secao] = id;
      renderizarListaSecao(secao);
    } else if (acao === "cancelar-edicao") {
      estadoEdicao[secao] = null;
      if (secao === "habilidades") renderizarListaHabilidades(); else renderizarListaSecao(secao);
    } else if (acao === "salvar-edicao") {
      await salvarEdicaoItem(secao, id);
    } else if (acao === "excluir") {
      await excluirItem(secao, id);
    } else if (acao === "adicionar-habilidade") {
      await adicionarHabilidade();
    } else if (acao === "editar-habilidade") {
      estadoEdicao.habilidades = id;
      renderizarListaHabilidades();
    } else if (acao === "salvar-edicao-habilidade") {
      await salvarEdicaoHabilidade(id);
    } else if (acao === "categorizar-habilidades") {
      await categorizarHabilidades();
    } else if (acao === "aplicar-categoria-sugerida") {
      await aplicarCategoriaSugerida(id, alvo.dataset.categoria);
    } else if (acao === "descartar-categoria-sugerida") {
      const linha = alvo.closest(".sugestao-categoria-linha");
      if (linha) linha.remove();
    }
  } catch (erro) {
    mostrarToast(erro.message || "Ocorreu um erro.", true);
  }
});


iniciarBuilder();
