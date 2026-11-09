# 🚗 AutoCare — Sistema de Controle de Manutenção Veicular

Sistema web local de alto desempenho dedicado ao controle de ciclo de vida mecânico, manutenções preventivas e corretivas, monitoramento de odômetro e gestão discriminada de custos para a frota pessoal (**Suzuki SX4 2.0 16V 4WD** e **Honda Biz 125 2011**).

Desenvolvido com **FastAPI + SQLite WAL** no backend e **Vue 3 + Vite + Tailwind CSS** no frontend, totalmente integrado ao **DevHub** (`http://localhost:9999`) na porta `:8015`.

---

## 🚀 Como Executar

### 1. Pelo DevHub (Recomendado)
Abra o painel do DevHub em `http://localhost:9999` e inicie o card **"AutoCare (Manutenção Veicular)"**, ou via terminal:
```cmd
hub start vehicle_maintenance
```

### 2. Por Script Local
Dê um duplo clique ou execute no terminal:
```cmd
iniciar_servidor.bat
```
- **Acesso no Computador:** [http://localhost:8015](http://localhost:8015)
- **Acesso no Celular (Wi-Fi):** `http://<SEU_IP_LOCAL>:8015`
- **Documentação Swagger (APIs REST):** [http://localhost:8015/docs](http://localhost:8015/docs)

Para encerrar o servidor liberando a porta:
```cmd
parar.bat
```

---

## 🛠️ Principais Recursos Implementados

1. **Catálogo de Veículos & Odometria Dinâmica**:
   - **Suzuki SX4 2.0 16V 4WD**: Inicializado com 101.000 km, histórico real das revisões de 87k e 92k km importado, e plano preventivo completo.
   - **Honda Biz 125 2011**: Inicializada com motor renovado (marco zero) e plano preventivo específico de motocicleta.
   - **Atualização Rápida de Odômetro**: Botão de 1 clique na home para atualizar o odômetro de referência a qualquer momento após abastecimentos.

2. **Gatilho Híbrido Preventivo**:
   - Projeção de vencimento por quilometragem restante versus tempo decorrido em meses (o critério mais restritivo prevalece).
   - Classificação visual automática: 🟢 *Em dia*, 🟡 *Próximo* (< 1.000 km ou < 30 dias) e 🔴 *Vencido*.

3. **Ciclo de Revisões em Duas Fases**:
   - **Revisão Planejada**: Checklist interativo para compras antecipadas (*"Peças para levar no porta-malas"*, marcas/códigos e status de compra) e lista de serviços contratados na oficina.
   - **Revisão dos 101.000 km do SX4**: Pré-configurada com filtros Wega/Tecfil, óleo GL-5 no porta-malas, óleo 5W-30 sintético e limpezas MAF/TBI na oficina.
   - **Conclusão Flexível na Oficina**: Permite revisar valores reais pagos e adicionar peças ou serviços imprevistos identificados no elevador antes de concluir.
   - Ao concluir, o odômetro é atualizado e os ciclos dos itens preventivos executados são reiniciados automaticamente.

4. **Manutenções Corretivas Avulsas**:
   - Botão direto para registrar consertos emergenciais imediatos (ex: pneu furado, bateria arriada) com suas despesas.

5. **Despesas Itemizadas & Auditoria de Custos**:
   - Lançamento obrigatório segregado em `PECA` versus `SERVICO` com part numbers e lojas.
   - **Dashboard Financeiro**: Gráficos mensais, proporção monetária Peças vs. Serviços e custo médio por quilômetro (R$/km).

6. **Comprovantes Anexos Locais**:
   - Suporte a upload e download de fotos e PDFs de notas fiscais, cupons e etiquetas de troca de óleo salvas em `data/uploads/`.

---

## 🧪 Testes Automatizados

A suite de testes cobre de ponta a ponta todas as regras de negócio via FastAPI TestClient em banco SQLite temporário:
```cmd
python -m pytest tests -v
```

---

## 📁 Estrutura de Documentação do Projeto

- [`CONTEXT.md`](./CONTEXT.md): Vocabulário canônico do domínio de manutenção automotiva.
- [`docs/adr/0001-stack-fastapi-sqlite-vue3.md`](./docs/adr/0001-stack-fastapi-sqlite-vue3.md): Decisão da arquitetura FastAPI + SQLite + Vue 3 na porta 8015.
- [`docs/adr/0002-ciclo-revisao-duas-fases-e-custos-itemizados.md`](./docs/adr/0002-ciclo-revisao-duas-fases-e-custos-itemizados.md): Decisão do ciclo em duas fases e despesas itemizadas.
- [`docs/specs/0001-sistema-controle-manutencao-veicular.md`](./docs/specs/0001-sistema-controle-manutencao-veicular.md): Especificação técnica com 25 user stories e critérios de aceitação.
- [`.scratch/sistema-controle-manutencao-veicular/issues/`](./.scratch/sistema-controle-manutencao-veicular/issues/): Fatias verticais (*tracer bullets*) do projeto.
