<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <span class="text-xs font-bold uppercase tracking-wider text-emerald-400">Inteligência Financeira</span>
        <h1 class="text-2xl font-black text-white mt-0.5">Auditoria de Custos & Indicadores</h1>
        <p class="text-xs text-slate-400 mt-1 max-w-xl">
          Consolidação de despesas entre autopeças adquiridas e mão de obra de oficina, histórico mensal e custo por quilômetro rodado.
        </p>
      </div>

      <button 
        @click="fetchMetrics" 
        class="px-3.5 py-2 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors flex items-center gap-1.5 self-start md:self-auto"
      >
        <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Atualizar Métricas
      </button>
    </div>

    <!-- KPI Summary Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Total Investido -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
        <span class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Gasto Total Acumulado</span>
        <div class="text-2xl font-mono font-black text-white">
          R$ {{ formatMoeda(metrics?.total_geral_gasto) }}
        </div>
        <p class="text-[11px] text-slate-500 mt-1">{{ metrics?.total_manutencoes_feitas }} manutenções registradas</p>
      </div>

      <!-- Peças -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
        <div class="flex items-center justify-between mb-1">
          <span class="text-[10px] uppercase font-bold text-blue-400">Autopeças & Insumos</span>
          <span class="text-xs font-bold text-blue-400 font-mono">{{ metrics?.proporcao?.percentual_pecas }}%</span>
        </div>
        <div class="text-2xl font-mono font-black text-blue-300">
          R$ {{ formatMoeda(metrics?.proporcao?.total_pecas) }}
        </div>
        <p class="text-[11px] text-slate-500 mt-1">Filtros, óleos, baterias e velas</p>
      </div>

      <!-- Serviços -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
        <div class="flex items-center justify-between mb-1">
          <span class="text-[10px] uppercase font-bold text-purple-400">Mão de Obra & Oficinas</span>
          <span class="text-xs font-bold text-purple-400 font-mono">{{ metrics?.proporcao?.percentual_servicos }}%</span>
        </div>
        <div class="text-2xl font-mono font-black text-purple-300">
          R$ {{ formatMoeda(metrics?.proporcao?.total_servicos) }}
        </div>
        <p class="text-[11px] text-slate-500 mt-1">Alinhamento, trocas e limpezas</p>
      </div>

      <!-- Revisões Planejadas -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
        <span class="text-[10px] uppercase font-bold text-amber-400 block mb-1">Revisões no Radar</span>
        <div class="text-2xl font-mono font-black text-amber-300">
          {{ metrics?.total_revisoes_planejadas }}
        </div>
        <p class="text-[11px] text-slate-500 mt-1">Próximas intervenções com checklist</p>
      </div>
    </div>

    <!-- Peças vs Serviços Split Bar -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
      <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">Distribuição do Custo de Propriedade</h3>
      <div class="w-full bg-slate-950 h-4 rounded-full overflow-hidden flex border border-slate-800 p-0.5">
        <div 
          class="bg-blue-500 h-full rounded-l-full transition-all duration-700" 
          :style="{ width: `${metrics?.proporcao?.percentual_pecas || 50}%` }"
          :title="`Peças: ${metrics?.proporcao?.percentual_pecas}%`"
        ></div>
        <div 
          class="bg-purple-500 h-full rounded-r-full transition-all duration-700" 
          :style="{ width: `${metrics?.proporcao?.percentual_servicos || 50}%` }"
          :title="`Serviços: ${metrics?.proporcao?.percentual_servicos}%`"
        ></div>
      </div>
      <div class="flex items-center justify-between text-xs font-semibold mt-2 px-1">
        <span class="text-blue-400 flex items-center gap-1.5">
          <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
          Peças Compradas: {{ metrics?.proporcao?.percentual_pecas }}% (R$ {{ formatMoeda(metrics?.proporcao?.total_pecas) }})
        </span>
        <span class="text-purple-400 flex items-center gap-1.5">
          <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
          Serviços de Oficina: {{ metrics?.proporcao?.percentual_servicos }}% (R$ {{ formatMoeda(metrics?.proporcao?.total_servicos) }})
        </span>
      </div>
    </div>

    <!-- Monthly Expenses Chart & Vehicle Comparison Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Monthly Bar Chart -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
        <div>
          <h3 class="text-sm font-bold text-white mb-1">Histórico Mensal de Despesas</h3>
          <p class="text-xs text-slate-400 mb-6">Investimento mês a mês na manutenção da frota.</p>
        </div>

        <div v-if="(metrics?.gastos_mensais || []).length === 0" class="text-center py-12 text-slate-500 text-xs">
          Nenhum dado mensal para exibir.
        </div>

        <div v-else class="space-y-4">
          <!-- SVG Bar Chart -->
          <div class="h-48 flex items-end gap-3 pt-6 pb-2 px-2 border-b border-slate-800">
            <div 
              v-for="gm in metrics.gastos_mensais" 
              :key="gm.mes"
              class="flex-1 flex flex-col items-center gap-1.5 h-full justify-end group relative"
            >
              <!-- Tooltip on Hover -->
              <div class="opacity-0 group-hover:opacity-100 transition-opacity absolute -top-10 bg-slate-950 border border-slate-700 text-[10px] font-mono text-white px-2 py-1 rounded shadow-lg pointer-events-none whitespace-nowrap z-10">
                R$ {{ formatMoeda(gm.total) }} (Peças: R${{ formatMoeda(gm.total_pecas) }})
              </div>

              <!-- Bar -->
              <div 
                class="w-full bg-gradient-to-t from-blue-600 to-emerald-400 rounded-t-md transition-all duration-500 group-hover:brightness-125"
                :style="{ height: `${getBarHeight(gm.total)}%` }"
              ></div>
              <span class="text-[10px] font-mono text-slate-400 truncate max-w-full block">
                {{ formatMes(gm.mes) }}
              </span>
            </div>
          </div>
          <div class="flex items-center justify-between text-[11px] text-slate-500">
            <span>Mais antigo</span>
            <span>Mês mais recente</span>
          </div>
        </div>
      </div>

      <!-- Vehicle Comparison Card -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <h3 class="text-sm font-bold text-white mb-1">Custos por Veículo</h3>
        <p class="text-xs text-slate-400 mb-4">Total investido e eficiência econômica por modelo.</p>

        <div class="space-y-3">
          <div 
            v-for="gv in metrics?.gastos_por_veiculo || []" 
            :key="gv.veiculo_id"
            class="bg-slate-950 p-4 rounded-xl border border-slate-800/80 space-y-2"
          >
            <div class="flex items-center justify-between">
              <span class="font-bold text-sm text-white">{{ gv.veiculo_nome }}</span>
              <span class="font-mono font-black text-sm text-emerald-400">
                R$ {{ formatMoeda(gv.total_gasto) }}
              </span>
            </div>

            <div class="flex items-center justify-between text-xs text-slate-400 font-mono">
              <span>Peças: R$ {{ formatMoeda(gv.total_pecas) }}</span>
              <span>Serviços: R$ {{ formatMoeda(gv.total_servicos) }}</span>
            </div>

            <div class="pt-2 border-t border-slate-900 flex items-center justify-between text-xs">
              <span class="text-slate-500">{{ gv.total_manutencoes }} manutenções registradas</span>
              <span v-if="gv.custo_por_km" class="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono font-bold">
                R$ {{ gv.custo_por_km }} / km
              </span>
              <span v-else class="text-slate-600 text-[11px] italic">
                Aguardando odômetro da próxima revisão
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const metrics = ref(null)

const fetchMetrics = async () => {
  try {
    const res = await fetch('/api/relatorios/dashboard')
    if (res.ok) {
      metrics.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  fetchMetrics()
})

const getBarHeight = (total) => {
  const max = Math.max(...(metrics.value?.gastos_mensais || []).map(g => g.total), 1)
  return Math.max(10, Math.round((total / max) * 100))
}

const formatMes = (mesStr) => {
  if (!mesStr) return ''
  const parts = mesStr.split('-')
  if (parts.length < 2) return mesStr
  return `${parts[1]}/${parts[0].substring(2)}`
}

const formatMoeda = (val) => {
  if (val === undefined || val === null) return '0,00'
  return Number(val).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

defineExpose({ fetchMetrics })
</script>
