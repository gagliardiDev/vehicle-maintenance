<template>
  <div class="space-y-6">
    <!-- Header Summary Banner -->
    <div class="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
      <div class="absolute -right-10 -bottom-10 w-48 h-48 bg-blue-500/5 rounded-full blur-3xl pointer-events-none"></div>
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-blue-400">Frota Ativa</span>
          <h1 class="text-2xl font-black text-white mt-0.5">Garagem & Monitoramento</h1>
          <p class="text-xs text-slate-400 mt-1 max-w-xl">
            Acompanhamento em tempo real de ciclos mecânicos por odômetro e tempo, checklist de peças no porta-malas e auditoria de custos.
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="px-4 py-2.5 rounded-xl bg-slate-950/60 border border-slate-800 text-center">
            <span class="text-[10px] uppercase font-bold text-slate-400 block">Veículos</span>
            <span class="text-lg font-black text-white">{{ vehicles.length }}</span>
          </div>
          <div class="px-4 py-2.5 rounded-xl bg-rose-500/10 border border-rose-500/20 text-center">
            <span class="text-[10px] uppercase font-bold text-rose-400 block">Vencidos</span>
            <span class="text-lg font-black text-rose-300">{{ totalVencidos }}</span>
          </div>
          <div class="px-4 py-2.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
            <span class="text-[10px] uppercase font-bold text-amber-400 block">Próximos</span>
            <span class="text-lg font-black text-amber-300">{{ totalProximos }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Vehicles Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div 
        v-for="v in vehicles" 
        :key="v.id"
        class="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-2xl p-6 transition-all shadow-lg flex flex-col justify-between relative group"
      >
        <!-- Top Bar with Badge & Actions -->
        <div>
          <div class="flex items-start justify-between gap-3 mb-4">
            <div class="flex items-center gap-3">
              <div 
                :class="v.tipo === 'CARRO' ? 'bg-blue-600/10 border-blue-500/30 text-blue-400' : 'bg-emerald-600/10 border-emerald-500/30 text-emerald-400'"
                class="w-12 h-12 rounded-xl border flex items-center justify-center text-2xl shadow-inner"
              >
                {{ v.tipo === 'CARRO' ? '🚙' : '🛵' }}
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h2 class="text-lg font-black text-white group-hover:text-blue-400 transition-colors">{{ v.nome }}</h2>
                  <span 
                    :class="v.tipo === 'CARRO' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'"
                    class="text-[10px] font-bold px-2 py-0.5 rounded-full border"
                  >
                    {{ v.tipo }}
                  </span>
                </div>
                <div class="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
                  <span>Ano {{ v.ano }}</span>
                  <span v-if="v.placa" class="px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 font-mono">{{ v.placa }}</span>
                </div>
              </div>
            </div>

            <!-- Fast Odometer Button -->
            <button 
              @click="$emit('open-odometer', v)"
              class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-600/10 hover:bg-blue-600/20 text-blue-400 border border-blue-500/30 transition-all flex items-center gap-1.5 shadow-sm active:scale-95"
              title="Atualizar quilometragem rápida"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              <span>Ajustar KM</span>
            </button>
          </div>

          <!-- Odometer Display -->
          <div class="bg-slate-950 rounded-xl p-4 border border-slate-800/80 mb-5">
            <div class="flex items-center justify-between text-xs text-slate-400 mb-1">
              <span class="flex items-center gap-1.5">
                <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Odômetro de Referência
              </span>
              <span class="text-[10px] text-slate-500">Última atualização: {{ formatDate(v.updated_at) }}</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span class="text-3xl font-mono font-black text-white tracking-tight">
                {{ formatKm(v.odometro_referencia) }}
              </span>
              <span class="text-sm font-semibold text-slate-400">km</span>
            </div>
          </div>

          <!-- Maintenance Health Indicators -->
          <div class="grid grid-cols-2 gap-3 mb-5">
            <div 
              :class="v.itens_vencidos > 0 ? 'bg-rose-500/10 border-rose-500/20 text-rose-300' : 'bg-slate-800/40 border-slate-800 text-slate-400'"
              class="p-3 rounded-xl border flex items-center justify-between"
            >
              <div class="flex items-center gap-2 text-xs font-semibold">
                <span class="w-2.5 h-2.5 rounded-full" :class="v.itens_vencidos > 0 ? 'bg-rose-500 animate-pulse' : 'bg-slate-600'"></span>
                <span>Vencidos</span>
              </div>
              <span class="text-base font-black">{{ v.itens_vencidos }}</span>
            </div>

            <div 
              :class="v.itens_proximos > 0 ? 'bg-amber-500/10 border-amber-500/20 text-amber-300' : 'bg-slate-800/40 border-slate-800 text-slate-400'"
              class="p-3 rounded-xl border flex items-center justify-between"
            >
              <div class="flex items-center gap-2 text-xs font-semibold">
                <span class="w-2.5 h-2.5 rounded-full" :class="v.itens_proximos > 0 ? 'bg-amber-500' : 'bg-slate-600'"></span>
                <span>Próximos</span>
              </div>
              <span class="text-base font-black">{{ v.itens_proximos }}</span>
            </div>
          </div>
        </div>

        <!-- Footer Actions -->
        <div class="border-t border-slate-800/80 pt-4 flex items-center gap-2">
          <button 
            @click="$emit('select-vehicle-plan', v)"
            class="flex-1 py-2.5 px-3 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors flex items-center justify-center gap-1.5"
          >
            <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            Plano Preventivo
          </button>
          <button 
            @click="$emit('view-revisions', v)"
            class="flex-1 py-2.5 px-3 rounded-xl text-xs font-bold bg-blue-600/10 hover:bg-blue-600/20 text-blue-400 border border-blue-500/30 transition-colors flex items-center justify-center gap-1.5"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            Revisões Planejadas
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  vehicles: { type: Array, default: () => [] }
})
defineEmits(['open-odometer', 'select-vehicle-plan', 'view-revisions'])

const totalVencidos = computed(() => {
  return props.vehicles.reduce((acc, v) => acc + (v.itens_vencidos || 0), 0)
})

const totalProximos = computed(() => {
  return props.vehicles.reduce((acc, v) => acc + (v.itens_proximos || 0), 0)
})

const formatKm = (val) => {
  if (val === undefined || val === null) return '0'
  return Number(val).toLocaleString('pt-BR')
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('pt-BR')
}
</script>
