# 06: Dashboard Financeiro, Relatórios Analíticos e Integração DevHub

**What to build:**  
A camada analítica financeira e a orquestração completa no ecossistema local. O usuário acessa a aba "Relatórios & Custos" e visualiza cards com os gastos totais consolidados por veículo, o custo médio por quilômetro rodado (R$/km), a divisão exata entre Peças versus Serviços/Mão de Obra em gráfico de rosca, e o histórico de despesas mês a mês em gráfico de barras interativo. Além disso, o projeto é integrado formalmente ao DevHub em `C:\projetos\dev-hub\projects.json` na porta `:8015`, permitindo que o usuário visualize status online/offline, monitore consumo de recursos e dê start/stop diretamente pela interface web do DevHub (`http://localhost:9999`) ou via scripts locais.

**Blocked by:** 04: Conclusão de Revisão com Despesas Itemizadas e Manutenção Corretiva Avulsa

**Status:** ready-for-agent

- [ ] Endpoint `/api/relatorios/dashboard` que agrega:
  - Total gasto acumulado por veículo.
  - Proporção percentual e monetária de `total_pecas` versus `total_servicos`.
  - Agrupamento temporal de despesas mês a mês (formato `YYYY-MM`).
  - Estimativa de custo por quilômetro ($R\$/\text{km}$) baseado na quilometragem percorrida entre manutenções registradas.
- [ ] Interface Vue 3 exibindo cards analíticos de KPI, gráfico de barras mensal e gráfico de rosca Peças vs. Serviços (sem dependências pesadas, utilizando SVG ou Chart.js leve).
- [ ] Registro do serviço `vehicle_maintenance` em `C:\projetos\dev-hub\projects.json` com porta `8015`, comando de inicialização, comando de parada e metadados.
- [ ] Verificação da inicialização limpa via painel web do DevHub (`http://localhost:9999`) e via terminal.
- [ ] Teste automatizado validando a consistência dos cálculos matemáticos de agregação e métricas do dashboard.
