<template>
  <header class="bg-slate-900 border-b border-slate-800 sticky top-0 z-30 shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo / Title -->
        <div class="flex items-center gap-3 cursor-pointer" @click="$emit('change-tab', 'frota')">
          <div class="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <div>
            <div class="font-bold text-lg text-white leading-tight flex items-center gap-2">
              AutoCare <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">DevHub :8015</span>
            </div>
            <p class="text-xs text-slate-400">Suzuki SX4 & Honda Biz 125</p>
          </div>
        </div>

        <!-- Desktop Navigation Tabs -->
        <nav class="hidden md:flex items-center space-x-1">
          <button 
            @click="$emit('change-tab', 'frota')"
            :class="activeTab === 'frota' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'"
            class="px-3.5 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
          >
            <span>🚗</span> Frota & Veículos
          </button>
          <button 
            @click="$emit('change-tab', 'revisoes')"
            :class="activeTab === 'revisoes' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'"
            class="px-3.5 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
          >
            <span>📋</span> Revisões Planejadas
            <span v-if="plannedCount > 0" class="px-1.5 py-0.2 rounded-full text-xs bg-amber-500/20 text-amber-300 border border-amber-500/30">
              {{ plannedCount }}
            </span>
          </button>
          <button 
            @click="$emit('change-tab', 'historico')"
            :class="activeTab === 'historico' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'"
            class="px-3.5 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
          >
            <span>⏱️</span> Linha do Tempo
          </button>
          <button 
            @click="$emit('change-tab', 'dashboard')"
            :class="activeTab === 'dashboard' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-800'"
            class="px-3.5 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
          >
            <span>📊</span> Custos & Relatórios
          </button>
        </nav>

        <!-- Quick Action Buttons -->
        <div class="flex items-center gap-2">
          <button 
            @click="$emit('open-corretiva')"
            class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            + Manutenção Avulsa
          </button>
        </div>
      </div>

      <!-- Mobile Navigation Tabs (Scrollable) -->
      <div class="md:hidden flex items-center space-x-1 py-2 overflow-x-auto border-t border-slate-800 text-xs">
        <button 
          @click="$emit('change-tab', 'frota')"
          :class="activeTab === 'frota' ? 'bg-blue-600 text-white' : 'text-slate-400 bg-slate-800/60'"
          class="px-3 py-1.5 rounded-md font-medium whitespace-nowrap"
        >
          🚗 Frota
        </button>
        <button 
          @click="$emit('change-tab', 'revisoes')"
          :class="activeTab === 'revisoes' ? 'bg-blue-600 text-white' : 'text-slate-400 bg-slate-800/60'"
          class="px-3 py-1.5 rounded-md font-medium whitespace-nowrap flex items-center gap-1"
        >
          📋 Revisões ({{ plannedCount }})
        </button>
        <button 
          @click="$emit('change-tab', 'historico')"
          :class="activeTab === 'historico' ? 'bg-blue-600 text-white' : 'text-slate-400 bg-slate-800/60'"
          class="px-3 py-1.5 rounded-md font-medium whitespace-nowrap"
        >
          ⏱️ Histórico
        </button>
        <button 
          @click="$emit('change-tab', 'dashboard')"
          :class="activeTab === 'dashboard' ? 'bg-blue-600 text-white' : 'text-slate-400 bg-slate-800/60'"
          class="px-3 py-1.5 rounded-md font-medium whitespace-nowrap"
        >
          📊 Custos
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  activeTab: { type: String, default: 'frota' },
  plannedCount: { type: Number, default: 0 }
})
defineEmits(['change-tab', 'open-corretiva'])
</script>
