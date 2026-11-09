# 01: Infraestrutura Básica, Catálogo de Veículos e Atualização Rápida de Odômetro

**What to build:**  
Uma aplicação funcional com backend FastAPI e interface Vue 3 servida localmente na porta 8015 em `0.0.0.0`, integrada com SQLite em modo WAL. O usuário acessa a tela inicial e visualiza os cards dos dois veículos da frota (**Suzuki SX4 2.0 16V 4WD** com odômetro em 101.000 km e **Honda Biz 125 2011** com odômetro provisório), com badges de identificação (Carro vs. Moto). Cada card disponibiliza um botão de "Atualização Rápida de Odômetro", abrindo um modal responsivo onde o usuário digita a nova quilometragem; ao salvar, o novo valor é gravado no banco, registrado no histórico de odometria e refletido imediatamente na interface sem recarregar a página. A aplicação é acompanhada por scripts operacionais `iniciar_servidor.bat` e `parar.bat`.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] O banco SQLite é inicializado em `data/maintenance.db` com tabela de veículos e histórico de odômetro em modo WAL.
- [ ] Os veículos Suzuki SX4 (101.000 km) e Honda Biz 125 2011 são cadastrados automaticamente via seed idempotente.
- [ ] A API REST expõe rotas `/api/veiculos` e `/api/veiculos/{id}/odometro`.
- [ ] A interface Vue 3 (Tailwind CSS) exibe a listagem dos veículos em cards limpos e responsivos para celular e desktop.
- [ ] O modal de "Atualização Rápida de Odômetro" valida entradas não numéricas e impede valores decrescentes no odômetro de referência.
- [ ] O histórico de alterações de odômetro armazena a data/hora e o valor informado.
- [ ] Os scripts `iniciar_servidor.bat` e `parar.bat` inicializam e finalizam o processo na porta 8015 de forma limpa.
- [ ] Teste automatizado via TestClient valida o CRUD de veículos e o recálculo do odômetro.
