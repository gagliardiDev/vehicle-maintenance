# 02: Plano Preventivo, Gatilho Híbrido e Projeção de Vencimento

**What to build:**  
O motor preventivo de regras de manutenção baseado em Gatilho Híbrido (quilometragem versus tempo decorrido, o que vencer primeiro). Ao acessar os detalhes de um veículo, o usuário visualiza todos os seus Itens Monitorados divididos por categorias mecânicas (Motor, Transmissão, Freios, Suspensão, etc.). Cada item exibe barras de progresso informando a quilometragem e o tempo restantes até a próxima intervenção, com classificação visual imediata em 🟢 `EM_DIA`, 🟡 `PROXIMO` (< 1.000 km ou < 30 dias) ou 🔴 `VENCIDO`. O usuário pode adicionar novos itens ou editar limites existentes. O Suzuki SX4 e a Honda Biz 125 já são inicializados com seus respectivos planos preventivos padrão populados.

**Blocked by:** 01: Infraestrutura Básica, Catálogo de Veículos e Atualização Rápida de Odômetro

**Status:** ready-for-agent

- [ ] Tabela de `itens_monitorados` persistida no SQLite vinculada a cada veículo.
- [ ] Implementação da fórmula de Gatilho Híbrido calculando `km_restante` e `dias_restantes` dinamicamente com base no `odometro_referencia` do veículo e na data atual.
- [ ] Classificação estrita de status: `VENCIDO` se KM ou dias $\le 0$; `PROXIMO` se KM $\le 1.000$ ou dias $\le 30$; senão `EM_DIA`.
- [ ] Carga inicial dos 10 itens preventivos do Suzuki SX4 (óleo de motor 5W-30, óleo de câmbio, óleo diferencial/transferência GL-5, velas iridium, correia poly-V, fluido de freio, filtros ar/óleo/cabine).
- [ ] Carga inicial dos 6 itens preventivos da Honda Biz 125 (óleo 10W-30 a cada 1.500 km, regulagem de corrente a cada 500 km, kit relação aos 15.000 km, vela, filtro de ar e lonas).
- [ ] Interface Vue 3 exibindo a listagem de itens preventivos com barras de progresso, filtro por status e modal para criação/edição de itens.
- [ ] Contadores de itens vencidos e próximos exibidos como badges no card do veículo na página principal.
- [ ] Teste automatizado via TestClient validando a transição de status por odômetro e por tempo decorrido.
