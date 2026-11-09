# 03: Revisões Planejadas e Checklist Pré-Oficina ("Levar no Porta-Malas")

**What to build:**  
O fluxo preparatório de revisões que apoia a cotação e compra antecipada de peças na internet antes da ida à oficina. O usuário pode abrir uma nova "Revisão Planejada" para um veículo, informando a quilometragem prevista e inserindo a lista de peças a adquirir e serviços a executar. Para cada peça, registra-se part number, marca recomendada, loja/fornecedor, quantidade e custo estimado. Na interface do celular ou desktop, o usuário dispõe de um checklist interativo onde pode marcar o checkbox "No porta-malas" para cada item já entregue e guardado no carro. A revisão atual dos 101.000 km do Suzuki SX4 já nasce pré-carregada no sistema com todas as peças e serviços detalhados no plano original.

**Blocked by:** 02: Plano Preventivo, Gatilho Híbrido e Projeção de Vencimento

**Status:** done

- [x] Tabelas `revisoes_planejadas` e `revisao_itens` persistidas no SQLite.
- [x] Rota da API REST para CRUD de revisões planejadas e toggle do status `comprado_porta_malas`.
- [x] População inicial da Revisão de 101.000 km do Suzuki SX4:
  - Peças a comprar por fora: Filtro de Ar (Wega JFA 0885/Tecfil ARL 7714), Filtro de Cabine (Tecfil ACP 709/Wega AKX 1965), Óleo do Diferencial/Transferência (2L API GL-5 80W-90).
  - Serviços de oficina: Troca de óleo 5W-30 (4,5L) + filtro de óleo M14, instalação dos filtros do porta-malas, troca do óleo GL-5, limpezas MAF/TBI/PCV, rodízio/alinhamento e inspeção de elevador.
- [x] Interface Vue 3 mobile-first exibindo o checklist com visual estilo prancheta de oficina, contadores de itens no porta-malas vs. a comprar e alertas visuais.
- [x] Botão para adicionar itens rápidos à lista de compras ou à lista de serviços da oficina.
- [x] Teste automatizado validando a persistência da revisão planejada e o toggle do estado do checklist.
