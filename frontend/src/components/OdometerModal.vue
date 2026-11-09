<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-md overflow-hidden shadow-2xl">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/50">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div>
            <h3 class="font-bold text-white text-base">Atualização Rápida de Odômetro</h3>
            <p class="text-xs text-slate-400">{{ vehicle?.nome }}</p>
          </div>
        </div>
        <button @click="$emit('close')" class="text-slate-400 hover:text-white transition-colors p-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Form Body -->
      <form @submit.prevent="handleSave" class="p-6 space-y-4">
        <div>
          <label class="block text-xs font-semibold text-slate-400 mb-1">Odômetro Atual de Referência</label>
          <div class="text-lg font-mono font-bold text-slate-300 bg-slate-950 px-3 py-2 rounded-lg border border-slate-800">
            {{ formatKm(vehicle?.odometro_referencia) }} km
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-blue-400 mb-1">Novo Odômetro (KM)</label>
          <input 
            v-model.number="newKm" 
            type="number" 
            step="1"
            :min="vehicle?.odometro_referencia"
            required
            class="w-full bg-slate-950 border border-blue-500/50 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-white font-mono text-xl font-bold px-4 py-2.5 rounded-lg outline-none transition-all"
            placeholder="Ex: 101500"
            autofocus
          />
          <p class="text-xs text-slate-500 mt-1">
            Digite a quilometragem atual do painel do veículo. O odômetro não pode ser reduzido.
          </p>
        </div>

        <div v-if="error" class="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ error }}</span>
        </div>

        <!-- History Preview -->
        <div v-if="history.length > 0" class="border-t border-slate-800 pt-3">
          <span class="text-xs font-semibold text-slate-400 block mb-2">Últimas Atualizações</span>
          <div class="space-y-1.5 max-h-32 overflow-y-auto text-xs pr-1">
            <div v-for="h in history.slice(0, 5)" :key="h.id" class="flex items-center justify-between py-1 px-2 rounded bg-slate-800/40 text-slate-300 font-mono">
              <span>{{ formatKm(h.odometro) }} km</span>
              <span class="text-slate-500 text-[10px]">{{ formatDate(h.data_registro) }} ({{ h.origem }})</span>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="pt-4 flex items-center justify-end gap-2 border-t border-slate-800">
          <button 
            type="button" 
            @click="$emit('close')" 
            class="px-4 py-2 rounded-lg text-xs font-semibold text-slate-300 hover:bg-slate-800 transition-colors"
          >
            Cancelar
          </button>
          <button 
            type="submit" 
            :disabled="saving"
            class="px-5 py-2 rounded-lg text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white transition-colors disabled:opacity-50 flex items-center gap-1.5 shadow-lg shadow-blue-600/30"
          >
            <span v-if="saving">Salvando...</span>
            <span v-else>Atualizar Odômetro</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  vehicle: Object
})
const emit = defineEmits(['close', 'updated'])

const newKm = ref(0)
const error = ref('')
const saving = ref(false)
const history = ref([])

watch(() => props.isOpen, async (val) => {
  if (val && props.vehicle) {
    newKm.value = props.vehicle.odometro_referencia || 0
    error.value = ''
    fetchHistory()
  }
})

const fetchHistory = async () => {
  if (!props.vehicle?.id) return
  try {
    const res = await fetch(`/api/veiculos/${props.vehicle.id}/odometro/historico`)
    if (res.ok) {
      history.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  }
}

const handleSave = async () => {
  if (newKm.value < props.vehicle.odometro_referencia) {
    error.value = `O novo valor não pode ser menor que o atual (${props.vehicle.odometro_referencia} km).`
    return
  }

  saving.value = true
  error.value = ''
  try {
    const res = await fetch(`/api/veiculos/${props.vehicle.id}/odometro`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ odometro: newKm.value })
    })

    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.detail || 'Erro ao atualizar odômetro')
    }

    const updatedVehicle = await res.json()
    emit('updated', updatedVehicle)
    emit('close')
  } catch (err) {
    error.value = err.message
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
</script>
