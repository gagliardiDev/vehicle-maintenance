<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <span class="text-xs font-bold uppercase tracking-wider text-purple-400">Linha do Tempo</span>
        <h1 class="text-2xl font-black text-white mt-0.5">Histórico de Manutenções & Comprovantes</h1>
        <p class="text-xs text-slate-400 mt-1 max-w-xl">
          Registro imutável de todas as intervenções executadas, custos discriminados e comprovantes fiscais anexados.
        </p>
      </div>

      <div class="flex items-center gap-2">
        <select 
          v-model="selectedVehicleId" 
          @change="fetchManutencoes"
          class="bg-slate-950 border border-slate-700 text-xs font-semibold text-slate-200 rounded-xl px-3 py-2 outline-none focus:border-blue-500"
        >
          <option :value="null">Todos os Veículos</option>
          <option v-for="v in allVehicles" :key="v.id" :value="v.id">{{ v.nome }}</option>
        </select>
        <button 
          @click="$emit('open-corretiva')"
          class="px-3.5 py-2 rounded-xl text-xs font-bold bg-rose-600 hover:bg-rose-500 text-white transition-colors flex items-center gap-1.5 shadow-md shadow-rose-600/20"
        >
          + Manutenção Avulsa
        </button>
      </div>
    </div>

    <!-- Timeline Content -->
    <div v-if="loading" class="text-center py-16 text-slate-500 text-sm">
      Carregando histórico de manutenções...
    </div>

    <div v-else-if="manutencoes.length === 0" class="text-center py-16 bg-slate-900/40 border border-slate-800/60 rounded-2xl text-slate-400 text-sm">
      Nenhuma manutenção registrada até o momento.
    </div>

    <div v-else class="space-y-6">
      <div 
        v-for="m in manutencoes" 
        :key="m.id"
        class="bg-slate-900 border border-slate-800 hover:border-slate-700/80 rounded-2xl p-6 transition-all shadow-xl relative overflow-hidden"
      >
        <!-- Top Bar -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800/80 mb-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="text-xs font-bold px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono">
                {{ getVehicleName(m.veiculo_id) }}
              </span>
              <span 
                :class="m.tipo_intervencao === 'PREVENTIVA' ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20' : 'bg-rose-500/10 text-rose-300 border-rose-500/20'"
                class="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full border"
              >
                {{ m.tipo_intervencao }}
              </span>
              <span class="text-xs text-slate-400 font-mono">
                {{ formatDate(m.data_execucao) }}
              </span>
            </div>
            <h2 class="text-lg font-black text-white">{{ m.titulo }}</h2>
            <div class="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
              <span class="font-mono text-slate-300 font-semibold">{{ formatKm(m.odometro) }} km</span>
              <span v-if="m.oficina_local" class="text-slate-500">• {{ m.oficina_local }}</span>
            </div>
          </div>

          <!-- Total Badge -->
          <div class="flex items-center gap-4 bg-slate-950 px-4 py-2.5 rounded-xl border border-slate-800 shrink-0">
            <div class="text-right">
              <span class="text-[10px] uppercase font-bold text-slate-500 block">Total Geral</span>
              <span class="text-lg font-mono font-black text-white">R$ {{ formatMoeda(m.total_geral) }}</span>
            </div>
          </div>
        </div>

        <!-- Notes if any -->
        <p v-if="m.observacoes" class="text-xs text-slate-400 bg-slate-950/60 p-3 rounded-xl border border-slate-800/60 mb-4">
          {{ m.observacoes }}
        </p>

        <!-- Itemized Expenses Table -->
        <div class="mb-5">
          <div class="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
            <span>Despesas Itemizadas</span>
            <div class="flex items-center gap-3 font-mono text-[11px]">
              <span class="text-blue-400">Peças: R$ {{ formatMoeda(m.total_pecas) }}</span>
              <span class="text-slate-600">•</span>
              <span class="text-purple-400">Serviços: R$ {{ formatMoeda(m.total_servicos) }}</span>
            </div>
          </div>

          <div class="space-y-1.5">
            <div 
              v-for="d in m.despesas" 
              :key="d.id"
              class="flex items-center justify-between py-2 px-3 rounded-lg bg-slate-950/70 border border-slate-800/50 text-xs"
            >
              <div class="flex items-center gap-2 flex-1">
                <span 
                  :class="d.tipo === 'PECA' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 'bg-purple-500/10 text-purple-400 border-purple-500/20'"
                  class="text-[9px] font-extrabold uppercase px-1.5 py-0.2 rounded border"
                >
                  {{ d.tipo }}
                </span>
                <span class="text-slate-200 font-medium">{{ d.descricao }}</span>
                <span v-if="d.part_number" class="text-slate-500 font-mono text-[11px]">[{{ d.part_number }}]</span>
                <span v-if="d.fornecedor" class="text-slate-600 text-[11px]">({{ d.fornecedor }})</span>
              </div>

              <div class="flex items-center gap-3 shrink-0 font-mono">
                <span class="text-slate-500 text-[11px]">{{ d.quantidade }}x R$ {{ formatMoeda(d.valor_unitario) }}</span>
                <span class="font-bold text-slate-200 w-20 text-right">R$ {{ formatMoeda(d.valor_total) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Attachments / Comprovantes Section -->
        <div class="border-t border-slate-800/80 pt-4">
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
              </svg>
              Comprovantes & Notas Fiscais ({{ (m.comprovantes || []).length }})
            </span>

            <!-- Upload Button -->
            <label class="cursor-pointer px-3 py-1 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              <span>+ Anexar Foto / Nota</span>
              <input 
                type="file" 
                accept="image/*,application/pdf"
                class="hidden" 
                @change="handleFileUpload($event, m.id)"
              />
            </label>
          </div>

          <!-- Attachments Thumbnails -->
          <div v-if="(m.comprovantes || []).length > 0" class="flex flex-wrap gap-3">
            <div 
              v-for="comp in m.comprovantes" 
              :key="comp.id"
              class="relative group rounded-xl overflow-hidden border border-slate-800 bg-slate-950 p-2 flex items-center gap-2"
            >
              <a 
                :href="`/api/anexos/${comp.id}/download`" 
                target="_blank"
                class="flex items-center gap-2 text-xs text-blue-400 hover:underline max-w-[180px] truncate"
              >
                <span>📎</span>
                <span class="truncate">{{ comp.original_name }}</span>
              </a>
              <button 
                @click="deleteAttachment(comp.id)"
                class="text-slate-600 hover:text-rose-400 text-xs p-1"
                title="Excluir anexo"
              >
                ✕
              </button>
            </div>
          </div>
          <div v-else class="text-[11px] text-slate-500 italic">
            Nenhum comprovante fiscal anexado ainda.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  allVehicles: { type: Array, default: () => [] }
})
defineEmits(['open-corretiva'])

const manutencoes = ref([])
const selectedVehicleId = ref(null)
const loading = ref(false)

const fetchManutencoes = async () => {
  loading.value = true
  let url = '/api/manutencoes'
  if (selectedVehicleId.value) {
    url += `?veiculo_id=${selectedVehicleId.value}`
  }
  try {
    const res = await fetch(url)
    if (res.ok) {
      manutencoes.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchManutencoes()
})

const getVehicleName = (veicId) => {
  const v = props.allVehicles.find(x => x.id === veicId)
  return v ? v.nome : `Veículo #${veicId}`
}

const handleFileUpload = async (event, manutencaoId) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch(`/api/manutencoes/${manutencaoId}/anexos`, {
      method: 'POST',
      body: formData
    })
    if (res.ok) {
      fetchManutencoes()
    } else {
      const err = await res.json()
      alert(err.detail || 'Erro ao fazer upload do arquivo')
    }
  } catch (e) {
    console.error(e)
  } finally {
    event.target.value = ''
  }
}

const deleteAttachment = async (compId) => {
  if (!confirm('Deseja excluir este comprovante?')) return
  try {
    const res = await fetch(`/api/anexos/${compId}`, { method: 'DELETE' })
    if (res.ok) {
      fetchManutencoes()
    }
  } catch (e) {
    console.error(e)
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

defineExpose({ fetchManutencoes })
</script>
