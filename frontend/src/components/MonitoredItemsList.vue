<template>
  <div class="space-y-6">
    <!-- Header with Vehicle Selector -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <button @click="$emit('back')" class="text-slate-400 hover:text-white transition-colors text-xs flex items-center gap-1 font-semibold">
            ← Voltar para Frota
          </button>
          <span class="text-slate-600">•</span>
          <span class="text-xs font-bold uppercase tracking-wider text-blue-400">Plano Preventivo</span>
        </div>
        <h1 class="text-2xl font-black text-white flex items-center gap-2">
          <span>{{ vehicle?.nome }}</span>
          <span class="text-xs font-normal text-slate-400 font-mono bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
            {{ formatKm(vehicle?.odometro_referencia) }} km
          </span>
        </h1>
      </div>

      <div class="flex items-center gap-2">
        <select 
          :value="vehicle?.id" 
          @change="$emit('change-vehicle', Number($event.target.value))"
          class="bg-slate-950 border border-slate-700 text-xs font-semibold text-slate-200 rounded-xl px-3 py-2 outline-none focus:border-blue-500"
        >
          <option v-for="v in allVehicles" :key="v.id" :value="v.id">{{ v.nome }}</option>
        </select>
        <button 
          @click="openAddModal"
          class="px-3.5 py-2 rounded-xl text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white transition-colors flex items-center gap-1.5 shadow-md shadow-blue-600/20"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Novo Item Preventivo
        </button>
      </div>
    </div>

    <!-- Filters & Stats Bar -->
    <div class="flex flex-wrap items-center justify-between gap-3 bg-slate-900/60 border border-slate-800/80 p-3 rounded-xl">
      <div class="flex items-center gap-1.5 text-xs">
        <button 
          v-for="st in ['TODOS', 'VENCIDO', 'PROXIMO', 'EM_DIA']" 
          :key="st"
          @click="filterStatus = st"
          :class="filterStatus === st ? 'bg-blue-600 text-white font-bold' : 'text-slate-400 hover:bg-slate-800 font-medium'"
          class="px-3 py-1.5 rounded-lg transition-colors capitalize"
        >
          {{ st === 'TODOS' ? 'Todos' : (st === 'EM_DIA' ? 'Em Dia' : (st === 'PROXIMO' ? 'Próximos' : 'Vencidos')) }}
          ({{ getCountByStatus(st) }})
        </button>
      </div>

      <div class="text-xs text-slate-400">
        Mostrando <span class="text-white font-bold">{{ filteredItems.length }}</span> de {{ items.length }} itens
      </div>
    </div>

    <!-- Monitored Items Cards -->
    <div v-if="loading" class="text-center py-12 text-slate-500 text-sm">
      Carregando itens preventivos...
    </div>

    <div v-else-if="filteredItems.length === 0" class="text-center py-12 bg-slate-900/40 border border-slate-800/60 rounded-2xl text-slate-400 text-sm">
      Nenhum item preventivo encontrado com o filtro selecionado.
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div 
        v-for="item in filteredItems" 
        :key="item.id"
        class="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-5 transition-all shadow-md flex flex-col justify-between"
      >
        <div>
          <!-- Title & Status Badge -->
          <div class="flex items-start justify-between gap-2 mb-3">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 block">
                {{ formatCategoria(item.categoria) }}
              </span>
              <h3 class="font-bold text-white text-base leading-snug">{{ item.nome }}</h3>
            </div>
            <span 
              :class="getStatusBadgeClass(item.status_vencimento)"
              class="text-[10px] font-extrabold uppercase px-2.5 py-1 rounded-full border shrink-0 flex items-center gap-1"
            >
              <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDotClass(item.status_vencimento)"></span>
              {{ formatStatus(item.status_vencimento) }}
            </span>
          </div>

          <!-- Description / Notes -->
          <p v-if="item.observacoes" class="text-xs text-slate-400 mb-4 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/50">
            {{ item.observacoes }}
          </p>

          <!-- Progress Meters -->
          <div class="space-y-3 mb-4">
            <!-- KM Progress -->
            <div v-if="item.intervalo_km">
              <div class="flex items-center justify-between text-xs mb-1">
                <span class="text-slate-400 font-medium">Ciclo de Quilometragem</span>
                <span class="font-mono" :class="item.km_restante <= 0 ? 'text-rose-400 font-bold' : (item.km_restante <= 1000 ? 'text-amber-400 font-bold' : 'text-slate-300')">
                  {{ item.km_restante <= 0 ? `Vencido há ${formatKm(Math.abs(item.km_restante))} km` : `Resta ${formatKm(item.km_restante)} km` }}
                </span>
              </div>
              <div class="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                <div 
                  class="h-full rounded-full transition-all duration-500"
                  :class="getProgressBarClass(item.percentual_km)"
                  :style="{ width: `${Math.min(100, item.percentual_km || 0)}%` }"
                ></div>
              </div>
              <div class="flex items-center justify-between text-[10px] text-slate-500 mt-0.5">
                <span>Último: {{ formatKm(item.ultimo_odometro) }} km</span>
                <span>Intervalo: {{ formatKm(item.intervalo_km) }} km</span>
                <span>Alvo: {{ formatKm(item.proximo_odometro_alvo) }} km</span>
              </div>
            </div>

            <!-- Time Progress -->
            <div v-if="item.intervalo_meses">
              <div class="flex items-center justify-between text-xs mb-1">
                <span class="text-slate-400 font-medium">Ciclo por Tempo</span>
                <span class="font-mono" :class="item.dias_restantes <= 0 ? 'text-rose-400 font-bold' : (item.dias_restantes <= 30 ? 'text-amber-400 font-bold' : 'text-slate-300')">
                  {{ item.dias_restantes <= 0 ? `Vencido há ${Math.abs(item.dias_restantes)} dias` : `Restam ${item.dias_restantes} dias` }}
                </span>
              </div>
              <div class="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                <div 
                  class="h-full rounded-full transition-all duration-500"
                  :class="getProgressBarClass(item.percentual_tempo)"
                  :style="{ width: `${Math.min(100, item.percentual_tempo || 0)}%` }"
                ></div>
              </div>
              <div class="flex items-center justify-between text-[10px] text-slate-500 mt-0.5">
                <span>Última troca: {{ formatDate(item.ultima_data) }}</span>
                <span>Prazo: {{ item.intervalo_meses }} meses</span>
                <span>Alvo: {{ formatDate(item.proxima_data_alvo) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Card Actions -->
        <div class="border-t border-slate-800/80 pt-3 flex items-center justify-end gap-2 text-xs">
          <button 
            @click="editItem(item)"
            class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
          >
            Editar
          </button>
          <button 
            @click="deleteItem(item.id)"
            class="px-2.5 py-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 transition-colors"
          >
            Excluir
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Adicionar / Editar Item -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div class="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl">
        <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/50">
          <h3 class="font-bold text-white text-base">
            {{ editingItem ? 'Editar Item Preventivo' : 'Novo Item Preventivo' }}
          </h3>
          <button @click="showModal = false" class="text-slate-400 hover:text-white p-1">✕</button>
        </div>

        <form @submit.prevent="saveItem" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Nome do Item / Serviço</label>
            <input 
              v-model="form.nome" 
              type="text" 
              required
              placeholder="Ex: Óleo de Motor 5W-30 Sintético"
              class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-blue-500"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-slate-400 mb-1">Categoria</label>
              <select 
                v-model="form.categoria"
                class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3 py-2 rounded-lg outline-none focus:border-blue-500"
              >
                <option value="MOTOR">Motor</option>
                <option value="AR_E_FILTROS">Ar e Filtros</option>
                <option value="TRANSMISSAO">Transmissão / Câmbio / 4x4</option>
                <option value="FREIOS">Freios</option>
                <option value="SUSPENSAO">Suspensão</option>
                <option value="ELETRICA">Elétrica / Bateria</option>
                <option value="CORRENTE_RELACAO">Corrente / Relação (Moto)</option>
                <option value="RODAGEM">Rodagem / Pneus</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-400 mb-1">Intervalo em KM</label>
              <input 
                v-model.number="form.intervalo_km" 
                type="number" 
                step="500"
                placeholder="Ex: 10000"
                class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-slate-400 mb-1">Intervalo em Meses</label>
              <input 
                v-model.number="form.intervalo_meses" 
                type="number" 
                step="1"
                placeholder="Ex: 6 ou 12"
                class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-400 mb-1">Último Odômetro Realizado (KM)</label>
              <input 
                v-model.number="form.ultimo_odometro" 
                type="number" 
                required
                class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Data da Última Execução</label>
            <input 
              v-model="form.ultima_data" 
              type="date" 
              required
              class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Observações / Part Number / Especificações</label>
            <textarea 
              v-model="form.observacoes" 
              rows="2"
              placeholder="Ex: Wega JFA 0885, óleo 5W-30 sintético..."
              class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-blue-500"
            ></textarea>
          </div>

          <div class="pt-4 border-t border-slate-800 flex items-center justify-end gap-2">
            <button 
              type="button" 
              @click="showModal = false"
              class="px-4 py-2 rounded-lg text-xs font-semibold text-slate-300 hover:bg-slate-800"
            >
              Cancelar
            </button>
            <button 
              type="submit" 
              :disabled="saving"
              class="px-5 py-2 rounded-lg text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white transition-colors disabled:opacity-50"
            >
              {{ saving ? 'Salvando...' : 'Salvar Item' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
  vehicle: Object,
  allVehicles: { type: Array, default: () => [] }
})
const emit = defineEmits(['back', 'change-vehicle', 'item-updated'])

const items = ref([])
const loading = ref(false)
const filterStatus = ref('TODOS')
const showModal = ref(false)
const editingItem = ref(null)
const saving = ref(false)

const form = ref({
  nome: '',
  categoria: 'MOTOR',
  intervalo_km: null,
  intervalo_meses: null,
  ultimo_odometro: 0,
  ultima_data: new Date().toISOString().substring(0, 10),
  observacoes: ''
})

const fetchItems = async () => {
  if (!props.vehicle?.id) return
  loading.value = true
  try {
    const res = await fetch(`/api/veiculos/${props.vehicle.id}/itens`)
    if (res.ok) {
      items.value = await res.json()
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

watch(() => props.vehicle?.id, () => {
  fetchItems()
}, { immediate: true })

const filteredItems = computed(() => {
  if (filterStatus.value === 'TODOS') return items.value
  return items.value.filter(i => i.status_vencimento === filterStatus.value)
})

const getCountByStatus = (st) => {
  if (st === 'TODOS') return items.value.length
  return items.value.filter(i => i.status_vencimento === st).length
}

const openAddModal = () => {
  editingItem.value = null
  form.value = {
    nome: '',
    categoria: 'MOTOR',
    intervalo_km: 10000,
    intervalo_meses: 6,
    ultimo_odometro: props.vehicle?.odometro_referencia || 0,
    ultima_data: new Date().toISOString().substring(0, 10),
    observacoes: ''
  }
  showModal.value = true
}

const editItem = (it) => {
  editingItem.value = it
  form.value = {
    nome: it.nome,
    categoria: it.categoria,
    intervalo_km: it.intervalo_km,
    intervalo_meses: it.intervalo_meses,
    ultimo_odometro: it.ultimo_odometro,
    ultima_data: it.ultima_data ? it.ultima_data.substring(0, 10) : new Date().toISOString().substring(0, 10),
    observacoes: it.observacoes || ''
  }
  showModal.value = true
}

const saveItem = async () => {
  saving.value = true
  try {
    let res
    if (editingItem.value) {
      res = await fetch(`/api/itens/${editingItem.value.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form.value)
      })
    } else {
      res = await fetch(`/api/veiculos/${props.vehicle.id}/itens`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form.value, veiculo_id: props.vehicle.id })
      })
    }

    if (res.ok) {
      showModal.value = false
      fetchItems()
      emit('item-updated')
    }
  } catch (e) {
    console.error(e)
  } finally {
    saving.value = false
  }
}

const deleteItem = async (itemId) => {
  if (!confirm('Deseja realmente remover este item preventivo?')) return
  try {
    const res = await fetch(`/api/itens/${itemId}`, { method: 'DELETE' })
    if (res.ok) {
      fetchItems()
      emit('item-updated')
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

const formatCategoria = (cat) => {
  const map = {
    'MOTOR': 'Motor e Ignição',
    'AR_E_FILTROS': 'Filtros e Admissão',
    'TRANSMISSAO': 'Transmissão & Diferencial',
    'FREIOS': 'Sistema de Freios',
    'SUSPENSAO': 'Suspensão e Direção',
    'ELETRICA': 'Sistema Elétrico',
    'CORRENTE_RELACAO': 'Transmissão Secundária',
    'RODAGEM': 'Pneus e Geometria'
  }
  return map[cat] || cat
}

const formatStatus = (st) => {
  if (st === 'VENCIDO') return 'Vencido'
  if (st === 'PROXIMO') return 'Próximo'
  return 'Em Dia'
}

const getStatusBadgeClass = (st) => {
  if (st === 'VENCIDO') return 'bg-rose-500/10 text-rose-400 border-rose-500/30'
  if (st === 'PROXIMO') return 'bg-amber-500/10 text-amber-400 border-amber-500/30'
  return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
}

const getStatusDotClass = (st) => {
  if (st === 'VENCIDO') return 'bg-rose-500 animate-pulse'
  if (st === 'PROXIMO') return 'bg-amber-500'
  return 'bg-emerald-500'
}

const getProgressBarClass = (pct) => {
  if (pct >= 100) return 'bg-rose-500'
  if (pct >= 85) return 'bg-amber-500'
  return 'bg-blue-500'
}
</script>
