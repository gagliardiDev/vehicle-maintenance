# 0001. Sistema de Controle de Manutenção Veicular e Gestão de Custos

> **Status:** `ready-for-agent`  
> **Data:** 09/11/2026  
> **Contexto:** [CONTEXT.md](../../CONTEXT.md)  
> **ADRs Relacionadas:** [0001-stack-fastapi-sqlite-vue3.md](../adr/0001-stack-fastapi-sqlite-vue3.md), [0002-ciclo-revisao-duas-fases-e-custos-itemizados.md](../adr/0002-ciclo-revisao-duas-fases-e-custos-itemizados.md)

---

## Problem Statement

O proprietário possui atualmente dois veículos de naturezas mecânicas distintas: um automóvel de tração integral (**Suzuki SX4 2.0 16V 4WD**, atualmente com 101.000 km) e uma motocicleta de uso urbano (**Honda Biz 125 2011**, com motor recém-retificado por completo).

Atualmente, o controle de intervenções mecânicas, periodicidades de troca e despesas enfrenta fricções severas:
1. **Dispersão e Perda de Histórico**: Registros antigos (como as revisões dos 87.000 km e 92.000 km do SX4) ficam soltos em conversas de chat, cadernos ou memória, dificultando saber com exatidão a vida útil restante de fluidos nobres (óleo de câmbio, velas iridium, fluido de freio DOT 4, óleo de diferencial GL-5).
2. **Falta de Projeção Preventiva Híbrida**: Certos componentes vencem estritamente por quilometragem (ex: óleo da Biz a cada 1.500 km ou velas do SX4), enquanto outros degradam por tempo decorrido mesmo com o veículo parado (óleo de motor aos 6 meses, fluido de freio aos 24 meses). Não há ferramenta visual unificada que aponte o vencimento iminente pelo critério mais restritivo.
3. **Falta de Apoio ao Fluxo Pré-Oficina ("Levar no Porta-Malas")**: No modelo de manutenção adotado pelo proprietário, peças de reposição de alta qualidade (filtros Wega/Tecfil/Mahle, lubrificantes de especificação API GL-5) são cotadas e compradas antecipadamente na internet para fornecimento direto ao mecânico, enquanto mão de obra e insumos padrão são fornecidos pela oficina. A ausência de um checklist dinâmico de compras com status de conferência gera esquecimentos e compras duplicadas.
4. **Opacidade Financeira de Custos**: Notas de oficinas misturam mão de obra com peças superfaturadas, impossibilitando auditar quanto do custo de manutenção é composto por peças sobressalentes versus serviços mecânicos, bem como calcular o custo real de manutenção por quilômetro rodado (R$/km).
5. **Dificuldade de Acesso no Local de Manutenção**: O proprietário necessita consultar o checklist e inspecionar códigos de peças diretamente pelo celular na garagem ou dentro da oficina via rede Wi-Fi local, sem depender de internet externa ou planilhas pesadas.

---

## Solution

Desenvolvimento do **Sistema de Controle de Manutenção Veicular**, uma aplicação web local de alto desempenho integrada ao ecossistema **DevHub** (`http://localhost:9999`) rodando na porta dedicada `:8015`.

A solução entrega:
- **Catálogo de Veículos e Odometria Dinâmica**: Cadastro individualizado para o Suzuki SX4 e a Honda Biz 125, com campo de **Odômetro de Referência** e botão de **Atualização Rápida de Odômetro** na interface para sincronização imediata em abastecimentos.
- **Motor de Gatilho Híbrido**: Cálculo automático do **Status de Vencimento** (`EM_DIA`, `PROXIMO`, `VENCIDO`) para cada **Item Monitorado**, considerando quilometragem restante versus dias restantes (o que vencer primeiro).
- **Ciclo de Revisões em Duas Fases**:
  - *Fase 1 (Revisão Planejada)*: Checklist interativo preparatório dividindo peças a adquirir antecipadamente (com marca, part number, loja e checkbox "no porta-malas") e serviços a executar na oficina.
  - *Fase 2 (Conclusão Flexível & Histórico)*: No ato da execução mecânica, o operador valida os itens, insere custos reais, registra eventuais imprevistos ou manutenções corretivas surgidas na inspeção de elevador e conclui a revisão, convertendo-a em um **Registro de Manutenção** imutável.
- **Suporte a Manutenções Corretivas Avulsas**: Registro direto de reparos emergenciais (ex: pneu furado, bateria) sem necessidade de agendamento prévio.
- **Gestão Discriminada de Custos e Anexos**: Armazenamento estrito de **Despesas Itemizadas** segregadas em `PECA` e `SERVICO`, acompanhadas de upload opcional de **Comprovantes Anexos** (fotos de notas fiscais, cupons, etiquetas de troca de óleo).
- **Dashboard e Relatórios Analíticos**: Visão consolidada da saúde da frota, linha do tempo de manutenções, gráficos de despesas mensais, proporção monetária entre Peças e Mão de Obra e custo médio por quilômetro.

---

## User Stories

1. Como proprietário de veículos, quero acessar um painel principal consolidado, para visualizar instantaneamente o status geral do Suzuki SX4 e da Honda Biz 125.
2. Como proprietário, quero ver o odômetro de referência atual exibido com destaque no card de cada veículo, para conferir a quilometragem sem navegar por menus.
3. Como proprietário, quero atualizar o odômetro de um veículo com um clique através do modal de "Atualização Rápida de Odômetro", para manter os alertas precisos logo após um abastecimento.
4. Como operador mecânico, quero que cada veículo possua sua própria lista de Itens Monitorados com intervalos de KM e/ou Meses personalizados, para refletir as especificidades técnicas de um carro 4x4 versus uma motocicleta.
5. Como operador, quero que o sistema calcule dinamicamente se cada item está `EM_DIA`, `PROXIMO` (< 1.000 km ou < 30 dias) ou `VENCIDO`, para que eu priorize as manutenções antes de ocorrerem quebras mecânicas.
6. Como proprietário do Suzuki SX4, quero ter pré-carregados no sistema o histórico das revisões de 87.000 km e 92.000 km, para manter o registro contínuo da vida útil do óleo de câmbio, correia poly-V, velas iridium e suspensão.
7. Como proprietário do Suzuki SX4, quero ter a revisão atual dos 101.000 km pré-configurada como uma "Revisão Planejada", para controlar as peças já compradas e os serviços que serão executados na oficina.
8. Como comprador de peças online, quero listar no checklist da revisão planejada o part number exato e marcas recomendadas (ex: filtros Wega JFA 0885 / Tecfil ACP 709, óleo GL-5 80W-90), para não errar a especificação na hora da compra.
9. Como proprietário, quero marcar um checkbox "Já no porta-malas" para cada peça comprada com antecedência, para saber exatamente quais itens já estão físicos no carro antes de ir ao mecânico.
10. Como proprietário na oficina, quero acessar o sistema pelo celular conectado ao Wi-Fi residencial/oficina na porta 8015, para ditar ao mecânico os procedimentos exatos da revisão (ex: limpeza de MAF com limpa-contatos e teste de tampa do radiador).
11. Como operador, quero poder adicionar novos itens ou serviços de última hora diretamente na tela de conclusão da revisão planejada, para contabilizar peças imprevistas detectadas pelo mecânico no elevador.
12. Como operador, quero concluir uma revisão planejada informando a data real e o odômetro final da execução, para que o sistema atualize automaticamente o odômetro do veículo e recalcule os próximos ciclos preventivos.
13. Como operador, quero registrar manutenções corretivas avulsas de emergência com um clique, para arquivar consertos imediatos que não passaram por planejamento prévio.
14. Como gestor financeiro, quero que cada gasto de uma manutenção seja itemizado obrigatoriamente como `PECA` ou `SERVICO`, para auditar a relação entre custo de autopeças e mão de obra cobrada.
15. Como gestor financeiro, quero registrar para cada peça o fornecedor (ex: Mercado Livre, Autopeças X), quantidade e valor unitário, para guardar referência de preço para compras futuras.
16. Como usuário, quero anexar fotos ou PDFs de comprovantes (notas fiscais, etiquetas de lubrificante ou fotos de peças desgastadas) a qualquer manutenção, para comprovar o histórico do veículo em caso de venda futura.
17. Como usuário, quero visualizar os comprovantes anexados diretamente na linha do tempo da manutenção, sem precisar procurar em pastas do sistema operacional.
18. Como proprietário da Honda Biz 125, quero que ela seja inicializada com plano preventivo específico de moto (trocas de óleo a cada 1.500 km, regulagem de corrente a cada 500 km, kit relação aos 15.000 km e lonas de freio), facilitando a gestão pós-reforma do motor.
19. Como proprietário da Biz, quero que o odômetro inicial dela seja facilmente ajustável via Atualização Rápida assim que eu checar o velocímetro físico da moto, sem bloquear o funcionamento do sistema.
20. Como operador, quero visualizar um gráfico de barras mensal com os gastos acumulados, para identificar os meses de maior impacto financeiro na frota.
21. Como operador, quero visualizar um gráfico de pizza/rosca comparando o total investido em Peças versus Serviços/Mão de Obra, para saber onde está concentrado o custo de propriedade dos veículos.
22. Como operador, quero visualizar o custo total por veículo e o custo médio estimado por quilômetro rodado (R$/km), para comparar a eficiência econômica entre o carro e a moto.
23. Como usuário do ecossistema local, quero iniciar o serviço com um clique pelo DevHub (`http://localhost:9999`) ou via script `iniciar_servidor.bat`, para ter inicialização padronizada idêntica aos outros projetos da máquina.
24. Como usuário do ecossistema local, quero encerrar o serviço de forma limpa via script `parar.bat`, para liberar a porta 8015 sem deixar processos órfãos em background.
25. Como operador em dispositivo móvel, quero uma interface responsiva com botões touch-friendly, contrastes adequados e badges coloridas, para operar com conforto mesmo com a tela do celular na vertical.

---

## Implementation Decisions

### 1. Modelo de Domínio e Tipagem Canônica

O subsistema de domínio adota tipos imutáveis e schemas estritos em Python/Pydantic no backend e TypeScript/Vue no frontend:

```python
# Prototype decision snippet (Domain Schema)
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class TipoVeiculo(str, Enum):
    CARRO = "CARRO"
    MOTO = "MOTO"

class StatusVencimento(str, Enum):
    EM_DIA = "EM_DIA"
    PROXIMO = "PROXIMO"
    VENCIDO = "VENCIDO"

class StatusRevisao(str, Enum):
    PLANEJADA = "PLANEJADA"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"

class TipoDespesa(str, Enum):
    PECA = "PECA"
    SERVICO = "SERVICO"

class TipoIntervencao(str, Enum):
    PREVENTIVA = "PREVENTIVA"
    CORRETIVA = "CORRETIVA"
    INSPECAO = "INSPECAO"
```

### 2. Módulos do Backend (FastAPI + SQLite WAL)

- **`core/db.py`**: Gerenciador de conexão SQLite nativa configurada com `PRAGMA journal_mode=WAL`, `PRAGMA foreign_keys=ON` e `PRAGMA synchronous=NORMAL`. Criação automática do schema no diretório `data/maintenance.db`.
- **`repositories/`**: Camada de persistência desacoplada da camada HTTP para veículos, itens monitorados, revisões e despesas.
- **`services/maintenance_service.py`**:
  - Implementação do algoritmo do **Gatilho Híbrido**:
    $$\Delta\text{km} = (\text{último\_odômetro} + \text{intervalo\_km}) - \text{odômetro\_referência}$$
    $$\Delta\text{dias} = (\text{última\_data} + \text{intervalo\_meses} \times 30.4375) - \text{hoje}$$
    Classificação: se $\Delta\text{km} \le 0$ ou $\Delta\text{dias} \le 0 \implies \text{VENCIDO}$; se $\Delta\text{km} \le 1.000$ ou $\Delta\text{dias} \le 30 \implies \text{PROXIMO}$; senão $\implies \text{EM\_DIA}$.
  - Conclusão atômica de Revisões Planejadas: persiste o registro histórico, computa totais de despesas, atualiza odômetro do veículo se aplicável e sincroniza os odômetros/datas dos itens monitorados correspondentes em uma única transação SQLite.
- **`api/`**:
  - `/api/veiculos`: CRUD e listagem com contadores de itens vencidos/próximos.
  - `/api/veiculos/{id}/odometro`: Atualização Rápida de Odômetro.
  - `/api/veiculos/{id}/itens`: Gestão de Itens Monitorados e projeções calculadas.
  - `/api/revisoes`: Gestão de Revisões Planejadas (itens, peças no porta-malas e conclusão).
  - `/api/manutencoes`: Histórico cronológico, cadastro de corretivas avulsas e upload de comprovantes.
  - `/api/relatorios/dashboard`: Métricas financeiras consolidadas (gastos por mês, veículo, peças vs serviços e R$/km).
- **`data/seed.py`**: População inicial idempotente:
  - Veículo 1: Suzuki SX4 2.0 16V (101.000 km), com histórico de 87k e 92k km, plano preventivo de 10 itens e Revisão Planejada dos 101.000 km preenchida com as peças do porta-malas e serviços da oficina.
  - Veículo 2: Honda Biz 125 2011 (odômetro inicial provisório 0 km), com plano preventivo de 6 itens para motocicleta.

### 3. Módulos do Frontend (Vue 3 + Vite + Tailwind CSS)

- **SPA Integrada com Single-Origin**:
  - Desenvolvido no diretório `frontend/` com Vue 3 (Composition API `<script setup>`), Vite e Tailwind CSS.
  - Build empacotado em `frontend/dist/` servido estaticamente pelo FastAPI na raiz `/`, eliminando a necessidade de servidores Node em produção local.
- **Componentes Principais**:
  - `FleetOverview.vue`: Cards dos veículos com badges visuais, alerta de vencimentos e botão de odômetro rápido.
  - `MonitoredItemsList.vue`: Listagem de peças preventivas com barra visual de progresso (KM restante e tempo restante).
  - `PlannedRevisionView.vue`: Checklist de preparação para oficina com badges "Porta-malas", marcas/códigos e botão de conclusão com modal de despesas.
  - `MaintenanceTimeline.vue`: Linha do tempo de manutenções com filtro por veículo, discriminação Peças vs Mão de Obra e galeria de comprovantes anexos.
  - `FinancialDashboard.vue`: Indicadores de custo, gráfico de barras mensal e proporção Peças vs Serviços.
  - `AttachmentUploader.vue`: Componente drag-and-drop para fotos de notas fiscais com visualização inline.

### 4. Integração Operacional com o DevHub

- **Porta**: `8015`, com host binding `0.0.0.0` para permitir acesso de outros dispositivos na mesma rede Wi-Fi.
- **Scripts**:
  - `iniciar_servidor.bat`: Ativa o ambiente e inicia o Uvicorn na porta 8015 em modo single-process.
  - `parar.bat`: Identifica o PID em escuta na porta 8015 e executa `taskkill /F /PID` garantindo liberação imediata da porta.
- **Registro no DevHub**: Inserção no arquivo `C:\projetos\dev-hub\projects.json` sob a chave `vehicle_maintenance`.

---

## Testing Decisions

### Princípios de Testabilidade (Seam Mais Alto Possível)

Os testes automatizados devem validar o comportamento externo do sistema e a integridade das regras de negócio automotivas, sem se acoplar a detalhes internos de implementação.

A costura primária (*primary seam*) de teste é a **API REST via FastAPI TestClient** operando sobre uma base SQLite temporária em memória:
1. **Gatilho Híbrido**:
   - Testar item com intervalo de 10.000 km e 6 meses.
   - Avançar o odômetro além do limite $\implies$ deve retornar status `VENCIDO`.
   - Manter odômetro baixo mas simular data de última troca há 7 meses $\implies$ deve retornar status `VENCIDO`.
   - Simular aproximação (< 1.000 km restantes ou < 30 dias restantes) $\implies$ deve retornar status `PROXIMO`.
2. **Ciclo de Revisão e Despesas Itemizadas**:
   - Cadastrar revisão planejada com 2 peças no porta-malas e 1 serviço.
   - Concluir a revisão incluindo uma peça extra de última hora.
   - Validar se a revisão passa para status `CONCLUIDA`, se um novo `Registro de Manutenção` foi gerado e se os totais `total_pecas`, `total_servicos` e `total_geral` foram calculados com precisão exata.
   - Validar se o item monitorado correspondente teve sua última data e último odômetro atualizados para o odômetro da revisão.
3. **Atualização Rápida de Odômetro**:
   - Enviar requisição com novo odômetro $\implies$ validar se o odômetro do veículo é atualizado e se um registro histórico de odômetro é gravado.
4. **Upload de Comprovantes**:
   - Submeter arquivo de imagem/PDF via multipart $\implies$ validar persistência em disco em `data/uploads/` e vínculo com o registro de manutenção.

---

## Out of Scope

- Integração telemática automática via OBD-II (Bluetooth/Wi-Fi no carro): a leitura do odômetro continuará sendo informada pelo operador.
- Emissão de notas fiscais ou integração com SEFAZ/sistemas tributários: o sistema é estritamente pessoal e gerencial.
- Controle de abastecimentos diários e cálculo de consumo médio de combustível (km/l): o foco é exclusivamente manutenção preventiva/corretiva e seus custos.
- Múltiplos usuários ou controle de permissões por login: o sistema é monousuário, voltado para o proprietário da máquina.

---

## Further Notes

- O banco de dados SQLite deve ser mantido em arquivo único no caminho relativo `data/maintenance.db`, permitindo que um simples backup da pasta preserve 100% dos dados da frota.
- A pasta `data/uploads/` deve conter um `.gitignore` preservando a estrutura de diretórios e evitando versionar arquivos pesados ou fotos pessoais.
