# Vehicle Maintenance

Contexto dedicado ao controle de ciclo de vida, manutenções preventivas e corretivas, monitoramento de odômetro e gestão discriminada de custos para a frota pessoal de veículos (Suzuki SX4 e Honda Biz 125).

## Language

### Veículos e Odometria

**Veículo**:
Unidade automotiva registrada no sistema (carro ou motocicleta) possuindo identificador, modelo, ano, placa e odômetro de referência.
_Avoid_: Automóvel, máquina, transporte

**Odômetro de Referência**:
Quilometragem acumulada mais recente informada pelo proprietário para um veículo, utilizada como base para o cálculo dinâmico de vencimento das manutenções.
_Avoid_: KM atual, quilometragem marcada

### Manutenção Preventiva e Monitoramento

**Item Monitorado**:
Componente, fluido ou serviço com periodicidade controlada vinculado a um veículo específico, possuindo limites configuráveis de quilometragem e/ou tempo em meses.
_Avoid_: Peça preventiva, tarefa, agendamento

**Gatilho Híbrido**:
Regra de cálculo de vencimento que projeta a próxima intervenção no cenário mais restritivo: quilometragem acumulada versus tempo decorrido desde a última execução (o que vencer primeiro).
_Avoid_: Alerta fixo, prazo simples

**Status de Vencimento**:
Classificação calculada da situação de um item monitorado: `EM_DIA` (longe dos limites), `PROXIMO` (a menos de 1.000 km ou menos de 30 dias do limite) ou `VENCIDO` (limite de odômetro ou tempo ultrapassado).
_Avoid_: Situação, estado da peça

### Histórico e Custos

**Revisão Planejada**:
Estado preparatório de uma intervenção futura com checklist de peças a adquirir ("levar no porta-malas") e serviços a executar, que é convertida em um Registro de Manutenção ao ser concluída na oficina.
_Avoid_: Orçamento, cotação, rascunho de serviço

**Registro de Manutenção**:
Evento histórico consolidado representando uma intervenção ou revisão realizada em determinada data e odômetro para um veículo (tanto planejada quanto corretiva avulsa).
_Avoid_: Ordem de serviço, conserto, visita à oficina

**Manutenção Corretiva Avulsa**:
Intervenção não programada motivada por falha, quebra ou desgaste inesperado (ex: pneu furado, bateria esgotada), registrada diretamente sem passar por fase de planejamento.
_Avoid_: Conserto de emergência, reparo isolado

**Despesa Itemizada**:
Linha de custo associada a um Registro de Manutenção classificada estritamente em `PECA` ou `SERVICO`, contendo descrição, código/part-number (quando peça), fornecedor/estabelecimento, quantidade e valor monetário.
_Avoid_: Gasto geral, nota fiscal, despesa avulsa

**Comprovante Anexo**:
Arquivo digital opcional (foto ou PDF de nota fiscal, cupom, etiqueta de óleo ou peça trocada) associado a um Registro de Manutenção e armazenado localmente no servidor.
_Avoid_: Recibo avulso, foto solta

**Atualização Rápida de Odômetro**:
Registro pontual de quilometragem acumulada que recalcula os vencimentos dos Itens Monitorados sem exigir vínculo com uma intervenção de manutenção.
_Avoid_: Marcação de km, ajuste manual de hodômetro

