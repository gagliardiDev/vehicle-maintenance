# 05: Anexos e Comprovantes Locais (Fotos de Notas, Etiquetas e Peças)

**What to build:**  
O subsistema de upload e visualização de comprovantes digitais (fotos de notas fiscais da oficina, cupons de autopeças, fotos da etiqueta de óleo no parabrisa ou de peças substituídas) atrelados a qualquer registro de manutenção histórico. O usuário pode arrastar ou selecionar fotos/PDFs diretamente do computador ou da câmera/galeria do celular. Os arquivos são salvos localmente em `data/uploads/` com nomes sanitizados e metadados no SQLite. Na interface, cada manutenção exibe sua galeria de miniaturas com clique para zoom e download.

**Blocked by:** 04: Conclusão de Revisão com Despesas Itemizadas e Manutenção Corretiva Avulsa

**Status:** ready-for-agent

- [ ] Tabela `comprovantes` criada no SQLite armazenando `manutencao_id`, `filename`, `original_name`, `filepath`, `mimetype`, `tamanho_bytes` e timestamp.
- [ ] Diretório `data/uploads/` gerenciado automaticamente com `.gitignore` para preservar privacidade e evitar versionar binários pesados.
- [ ] Endpoints de upload (`POST /api/manutencoes/{id}/anexos`), download e deleção de comprovantes com validação de tipos de arquivo permitidos (JPEG, PNG, WEBP, PDF) e limite de tamanho (15 MB).
- [ ] Componente Vue 3 de upload drag-and-drop integrado ao modal de detalhes da manutenção e na tela de conclusão.
- [ ] Galeria com visualizador lightbox integrado na linha do tempo para inspeção de recibos pelo celular na oficina.
- [ ] Teste automatizado validando o upload de arquivo multipart, integridade no disco e associação correta com o registro de manutenção.
