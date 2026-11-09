<template>
  <div class="space-y-6">
    <!-- Header with Selector -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <span class="text-xs font-bold uppercase tracking-wider text-amber-400">Preparação Pré-Oficina</span>
        <h1 class="text-2xl font-black text-white mt-0.5">Revisões Planejadas & Porta-Malas</h1>
        <p class="text-xs text-slate-400 mt-1 max-w-xl">
          Checklist interativo de peças adquiridas antecipadamente na internet e escopo de serviços contratados na oficina mecânica.
        </p>
      </div>

      <div class="flex items-center gap-2">
        <select 
          v-model="selectedVehicleId" 
          @change="fetchRevisoes"
          class="bg-slate-950 border border-slate-700 text-xs font-semibold text-slate-200 rounded-xl px-3 py-2 outline-none focus:border-blue-500"
        >
          <option :value="null">Todos os Veículos</option>
          <option v-for="v in allVehicles" :key="v.id" :value="v.id">{{ v.nome }}</option>
        </select>
        <button 
          @click="openNewRevisionModal"
          class="px-3.5 py-2 rounded-xl text-xs font-bold bg-amber-600 hover:bg-amber-500 text-white transition-colors flex items-center gap-1.5 shadow-md shadow-amber-600/20"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nova Revisão Planejada
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="revisoes.length === 0" class="text-center py-16 bg-slate-900/40 border border-slate-800/60 rounded-2xl p-6">
      <div class="w-16 h-16 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center mx-auto mb-3 text-2xl">
        📋
      </div>
      <h3 class="text-lg font-bold text-white mb-1">Nenhuma revisão planejada pendente</h3>
      <p class="text-xs text-slate-400 max-w-md mx-auto mb-4">
        Todas as revisões preventivas estão concluídas ou ainda não foram agendadas. Você pode planejar uma nova revisão com checklist a qualquer momento.
      </p>
      <button 
        @click="openNewRevisionModal"
        class="px-4 py-2 rounded-xl text-xs font-bold bg-amber-600 hover:bg-amber-500 text-white transition-colors"
      >
        Planejar Próxima Revisão
      </button>
    </div>

    <!-- Revisions List -->
    <div v-for="rev in revisoes" :key="rev.id" class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
      <!-- Revision Header Banner -->
      <div class="p-6 bg-gradient-to-r from-slate-900 via-slate-850 to-slate-900 border-b border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5">
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono">
              {{ getVehicleName(rev.veiculo_id) }}
            </span>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/20">
              Planejada para {{ formatKm(rev.odometro_previsto) }} km
            </span>
            <span v-if="rev.data_prevista" class="text-xs text-slate-400">
              Previsão: {{ formatDate(rev.data_prevista) }}
            </span>
          </div>
          <h2 class="text-xl font-black text-white">{{ rev.titulo }}</h2>
          <p v-if="rev.observacoes" class="text-xs text-slate-400 mt-1 max-w-2xl">
            {{ rev.observacoes }}
          </p>
        </div>

        <!-- Action / Trunk Meter -->
        <div class="flex items-center gap-3">
          <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-center">
            <span class="text-[10px] uppercase font-bold text-slate-400 block">Peças no Porta-Malas</span>
            <span class="text-base font-black text-amber-300 font-mono">
              {{ rev.total_porta_malas }} / {{ rev.total_itens_pecas }}
            </span>
          </div>

          <button 
            @click="$emit('concluir-revisao', rev)"
            class="px-4 py-3 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-all flex items-center gap-2 shadow-lg shadow-emerald-600/20 active:scale-95"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Concluir na Oficina
          </button>
        </div>
      </div>

      <!-- Revision Content: 2 Columns (Porta-Malas vs Oficina) -->
      <div class="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Section A: Peças para Comprar por Fora & Levar no Porta-Malas -->
        <div class="space-y-3">
          <div class="flex items-center justify-between pb-2 border-b border-slate-800">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 text-xs font-bold">
                A
              </span>
              <h3 class="font-bold text-white text-sm">Peças para Levar no Porta-Malas</h3>
            </div>
            <span class="text-xs text-amber-400 font-semibold font-mono">
              {{ getPecasPortaMalas(rev.itens).filter(i => i.comprado_porta_malas).length }} de {{ getPecasPortaMalas(rev.itens).length }} prontas
            </span>
          </div>

          <div class="space-y-2">
            <div 
              v-for="item in getPecasPortaMalas(rev.itens)" 
              :key="item.id"
              :class="item.comprado_porta_malas ? 'bg-emerald-950/20 border-emerald-500/30' : 'bg-slate-950/60 border-slate-800/80'"
              class="p-3.5 rounded-xl border transition-all flex items-start justify-between gap-3 group"
            >
              <div class="flex items-start gap-3">
                <input 
                  type="checkbox" 
                  :checked="item.comprado_porta_malas"
                  @change="toggleItemPortaMalas(item)"
                  class="mt-1 w-4 h-4 rounded bg-slate-900 border-slate-700 text-emerald-500 focus:ring-emerald-500 cursor-pointer"
                />
                <div>
                  <h4 
                    :class="item.comprado_porta_malas ? 'text-emerald-300 font-semibold line-through decoration-emerald-500/40' : 'text-white font-semibold'"
                    class="text-xs leading-snug"
                  >
                    {{ item.descricao }}
                  </h4>
                  <div class="flex flex-wrap items-center gap-2 text-[11px] text-slate-400 mt-1">
                    <span v-if="item.part_number" class="px-1.5 py-0.2 rounded bg-slate-800 font-mono text-slate-300">
                      {{ item.part_number }}
                    </span>
                    <span v-if="item.fornecedor" class="text-slate-500">
                      Loja: {{ item.fornecedor }}
                    </span>
                    <span>Qtd: {{ item.quantidade }}</span>
                  </div>
                </div>
              </div>

              <div class="text-right shrink-0">
                <span class="text-xs font-mono font-bold text-slate-300 block">
                  R$ {{ formatMoeda(item.quantidade * item.valor_estimado) }}
                </span>
                <span 
                  :class="item.comprado_porta_malas ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' : 'text-slate-400 bg-slate-800 border-slate-700'"
                  class="text-[9px] font-bold px-1.5 py-0.2 rounded-full border uppercase mt-1 inline-block"
                >
                  {{ item.comprado_porta_malas ? 'No porta-malas' : 'A comprar' }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Section B: Serviços e Insumos da Oficina -->
        <div class="space-y-3">
          <div class="flex items-center justify-between pb-2 border-b border-slate-800">
            <div class="flex items-center gap-2">
              <span class="w-6 h-6 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 text-xs font-bold">
                B
              </span>
              <h3 class="font-bold text-white text-sm">Serviços e Peças da Oficina</h3>
            </div>
            <span class="text-xs text-slate-400 font-semibold font-mono">
              {{ getServicosOficina(rev.itens).length }} itens
            </span>
          </div>

          <div class="space-y-2">
            <div 
              v-for="item in getServicosOficina(rev.itens)" 
              :key="item.id"
              class="bg-slate-950/60 border border-slate-800/80 p-3.5 rounded-xl flex items-start justify-between gap-3"
            >
              <div>
                <span 
                  :class="item.tipo === 'PECA' ? 'text-blue-400 bg-blue-500/10 border-blue-500/20' : 'text-purple-400 bg-purple-500/10 border-purple-500/20'"
                  class="text-[9px] font-extrabold uppercase px-1.5 py-0.2 rounded-full border mb-1 inline-block"
                >
                  {{ item.tipo === 'PECA' ? 'Peça Oficina' : 'Mão de Obra / Serviço' }}
                </span>
                <h4 class="text-xs font-semibold text-white leading-snug">{{ item.descricao }}</h4>
                <div v-if="item.part_number" class="text-[11px] text-slate-400 font-mono mt-0.5">
                  Ref: {{ item.part_number }}
                </div>
              </div>

              <div class="text-right shrink-0">
                <span class="text-xs font-mono font-bold text-slate-300 block">
                  R$ {{ formatMoeda(item.quantidade * item.valor_estimado) }}
                </span>
                <span class="text-[10px] text-slate-500">
                  {{ item.valor_estimado === 0 ? 'Incluso / Cortesia' : 'Estimado' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Nova Revisão Planejada -->
    <div v-if="showNewModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div class="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl">
        <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/50">
          <h3 class="font-bold text-white text-base">Nova Revisão Planejada</h3>
          <button @click="showNewModal = false" class="text-slate-400 hover:text-white p-1">✕</button>
        </div>

        <form @submit.prevent="createRevision" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Veículo</label>
            <select 
              v-model="newForm.veiculo_id"
              required
              class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3 py-2 rounded-lg outline-none focus:border-blue-500"
            >
              <option v-for="v in allVehicles" :key="v.id" :value="v.id">{{ v.nome }}</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Título da Revisão</label>
            <input 
              v-model="newForm.titulo" 
              type="text" 
              required
              placeholder="Ex: Revisão dos 110.000 km"
              class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-blue-500"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-slate-400 mb-1">Odômetro Previsto (KM)</label>
              <input 
                v-model.number="newForm.odometro_previsto" 
                type="number" 
                required
                class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-400 mb-1">Data Estimada</label>
              <input 
                v-model="newForm.data_prevista" 
                type="date"
                class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Observações de Planejamento</label>
            <textarea 
              v-model="newForm.observacoes" 
              rows="2"
              placeholder="Notas de cotação ou lembretes para a oficina..."
              class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-blue-500"
            ></textarea>
          </div>

          <div class="pt-4 border-t border-slate-800 flex items-center justify-end gap-2">
            <button 
              type="button" 
              @click="showNewModal = false"
              class="px-4 py-2 rounded-lg text-xs font-semibold text-slate-300 hover:bg-slate-800"
            >
              Cancelar
            </button>
            <button 
              type="submit" 
              :disabled="saving"
              class="px-5 py-2 rounded-lg text-xs font-bold bg-amber-600 hover:bg-amber-500 text-white transition-colors disabled:opacity-50"
            >
              {{ saving ? 'Criando...' : 'Criar Revisão' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  allVehicles: { type: Array, default: () => [] }
})
const emit = defineEmits(['concluir-revisao'])

const revisoes = ref([])
const selectedVehicleId = ref(null)
const showNewModal = ref(false)
const saving = ref(false)

const newForm = ref({
  veiculo_id: null,
  titulo: '',
  odometro_previsto: 100000,
  data_prevista: '',
  observacoes: '',
  itens: []
})

const fetchRevisoes = async () => {
  let url = '/api/revisoes?status=PLANEJADA'
  if (selectedVehicleId.value) {
    url += `&veiculo_id=${selectedVehicleId.value}`
  }
  try {
    const res = await fetch(url)
    if (res.ok) {
      revisoes.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  fetchRevisoes()
})

const getVehicleName = (veicId) => {
  const v = props.allVehicles.find(x => x.id === veicId)
  return v ? v.nome : `Veículo #${veicId}`
}

const getPecasPortaMalas = (itens) => {
  if (!itens) return []
  // Peças com fornecedor tipo Mercado Livre ou autopeças para levar no porta-malas
  return itens.filter(i => i.tipo === 'PECA' && (i.fornecedor !== 'Oficina' || i.comprado_porta_malas))
}

const getServicosOficina = (itens) => {
  if (!itens) return []
  return itens.filter(i => i.tipo === 'SERVICO' || (i.tipo === 'PECA' && i.fornecedor === 'Oficina' && !i.comprado_porta_malas))
}

const toggleItemPortaMalas = async (item) => {
  const nextVal = !item.comprado_porta_malas
  item.comprado_porta_malas = nextVal
  try {
    await fetch(`/api/revisoes/itens/${item.id}/porta-malas`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comprado: nextVal })
    })
    fetchRevisoes()
  } catch (e) {
    console.error(e)
  }
}

const openNewRevisionModal = () => {
  newForm.value = {
    veiculo_id: props.allVehicles[0]?.id || 1,
    titulo: 'Nova Revisão Preventiva',
    odometro_previsto: (props.allVehicles[0]?.odometro_referencia || 0) + 10000,
    data_prevista: new Date().toISOString().substring(0, 10),
    observacoes: '',
    itens: []
  }
  showNewModal.value = true
}

const createRevision = async () => {
  saving.value = true
  try {
    const res = await fetch('/api/revisoes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newForm.value)
    })
    if (res.ok) {
      showNewModal.value = false
      fetchRevisoes()
    }
  } catch (e) {
    console.error(e)
  } finally {
    saving.value = false
  }
}

const formatKm = (val) => {
  if (val === undefined || val === null) return '0'
  return Number(val).toLocaleString('pt-BR')
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('pt-BR')
}

const formatMoeda = (val) => {
  if (val === undefined || val === null) return '0,00'
  return Number(val).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

defineExpose({ fetchRevisoes })
</script>
