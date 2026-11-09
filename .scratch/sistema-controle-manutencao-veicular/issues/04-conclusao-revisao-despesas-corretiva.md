# 04: Conclusão de Revisão com Despesas Itemizadas e Manutenção Corretiva Avulsa

**What to build:**  
A transição atômica da fase de planejamento para o histórico consolidado de manutenções, bem como o suporte a reparos emergenciais não programados. Ao concluir uma revisão planejada na oficina, o usuário clica em "Concluir Revisão", insere a data real e o odômetro final, revisa os valores reais pagos e pode adicionar novas peças ou serviços imprevistos (ex: troca de coifa rasgada ou pastilhas traseiras identificadas no elevador). Ao confirmar, a revisão é fechada, um `Registro de Manutenção` imutável é gravado com todas as `Despesas Itemizadas` discriminadas estritamente em `PECA` e `SERVICO`, o odômetro do veículo é atualizado caso seja superior ao atual e os itens preventivos vinculados têm seus ciclos reiniciados. O sistema também oferece um botão para registrar uma `Manutenção Corretiva Avulsa` direta, e carrega o histórico real das revisões passadas do SX4 (87.000 km e 92.000 km) na Linha do Tempo.

**Blocked by:** 03: Revisões Planejadas e Checklist Pré-Oficina ("Levar no Porta-Malas")

**Status:** done

- [x] Tabelas `registros_manutencao` e `despesas_itemizadas` criadas no SQLite.
- [x] Endpoint `/api/revisoes/{id}/concluir` que executa a transação atômica:
  - Cria o `Registro de Manutenção` com campos `total_pecas`, `total_servicos` e `total_geral`.
  - Persiste as despesas itemizadas associadas.
  - Atualiza o status da revisão planejada para `CONCLUIDA`.
  - Atualiza o `odometro_referencia` do veículo e insere no histórico de odometria.
  - Atualiza `ultimo_odometro` e `ultima_data` dos itens monitorados executados.
- [x] Endpoint `/api/manutencoes/corretiva` para cadastro direto de intervenção de emergência com suas respectivas despesas.
- [x] Carga inicial do histórico real do Suzuki SX4:
  - Revisão dos 87.000 km (óleo motor, filtros ar/óleo/cabine, velas iridium, óleo câmbio, correia poly-V, fluido freio, kit amortecedor LE, coifa LE).
  - Revisão dos 92.000 km (óleo motor e filtro óleo, pastilhas dianteiras, bateria 60Ah, geometria e balanceamento).
- [x] Interface Vue 3 com modal interativo de conclusão de revisão, tela de cadastro de corretiva avulsa e Linha do Tempo visual com detalhamento expansível de custos.
- [x] Teste automatizado validando a consistência dos totais de peças e serviços e o recálculo dos prazos preventivos.
