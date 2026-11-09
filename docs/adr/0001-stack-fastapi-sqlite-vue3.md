# 0001. Arquitetura FastAPI, SQLite e Vue 3 Integrada ao DevHub

O sistema de controle de manutenção requer baixo consumo de recursos, execução em máquina local (Windows) gerenciada pelo DevHub, facilidade de backup e interface responsiva acessível tanto no desktop quanto no celular na oficina via Wi-Fi.

Optou-se por backend em Python com FastAPI e SQLite em modo WAL, pareado com frontend em Vue 3 (Vite + Tailwind CSS), servido na porta `8015` com binding em `0.0.0.0`. O FastAPI expõe a API REST e serve os estáticos compilados do Vue 3 para manter processo único em produção local, enquanto o Vite dev server pode ser usado durante desenvolvimento ativo. A integração com o DevHub ocorre via scripts `.bat` padronizados na pasta raiz.
