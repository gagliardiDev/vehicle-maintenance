# 0002. Ciclo de Revisões em Duas Fases e Despesas Itemizadas

A gestão prática de veículos envolve a compra prévia de peças na internet para fornecimento na oficina ("levar no porta-malas"), seguida da execução de serviços e eventuais imprevistos identificados durante a inspeção no elevador.

Decidiu-se separar o fluxo em duas fases: `Revisão Planejada` (checklist interativo de peças a adquirir e serviços previstos com status de compra) e `Registro de Manutenção` (registro histórico imutável consolidado após a execução). No momento da conclusão na oficina, a revisão planejada permite a inclusão flexível de despesas corretivas de última hora, calcula os totais divididos categoricamente em `PECA` e `SERVICO`, atualiza os odômetros dos itens monitorados vinculados e aceita uploads opcionais de comprovantes locais. Manutenções emergenciais também podem ser lançadas diretamente como `Manutenção Corretiva Avulsa`.
