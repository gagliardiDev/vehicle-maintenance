<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-blue-600 selection:text-white">
    <!-- Navbar -->
    <Navbar 
      :activeTab="activeTab" 
      :plannedCount="plannedCount"
      @change-tab="handleTabChange"
      @open-corretiva="openCorretivaModal"
    />

    <!-- Main Content Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- 1. Frota & Veículos (Home) -->
      <FleetOverview 
        v-if="activeTab === 'frota'"
        :vehicles="vehicles"
        @open-odometer="openOdometerModal"
        @select-vehicle-plan="selectVehiclePlan"
        @view-revisions="viewVehicleRevisions"
      />

      <!-- 2. Plano Preventivo do Veículo Selecionado -->
      <MonitoredItemsList 
        v-else-if="activeTab === 'plano'"
        :vehicle="selectedVehicle"
        :allVehicles="vehicles"
        @back="activeTab = 'frota'"
        @change-vehicle="handleChangeVehicle"
        @item-updated="fetchVehicles"
      />

      <!-- 3. Revisões Planejadas (Checklist de Oficina & Porta-Malas) -->
      <PlannedRevisionView 
        v-else-if="activeTab === 'revisoes'"
        ref="plannedViewRef"
        :allVehicles="vehicles"
        @concluir-revisao="openConcluirModal"
      />

      <!-- 4. Linha do Tempo / Histórico de Manutenções -->
      <MaintenanceTimeline 
        v-else-if="activeTab === 'historico'"
        ref="timelineRef"
        :allVehicles="vehicles"
        @open-corretiva="openCorretivaModal"
      />

      <!-- 5. Custos & Relatórios Financeiros -->
      <FinancialDashboard 
        v-else-if="activeTab === 'dashboard'"
        ref="dashboardRef"
      />
    </main>

    <!-- Modais Globais -->
    <!-- Modal de Atualização Rápida de Odômetro -->
    <OdometerModal 
      :isOpen="showOdometerModal"
      :vehicle="vehicleForOdometer"
      @close="showOdometerModal = false"
      @updated="handleOdometerUpdated"
    />

    <!-- Modal de Conclusão de Revisão -->
    <CompleteRevisionModal 
      :isOpen="showConcluirModal"
      :revisao="revisaoToConclude"
      :vehicle="getVehicleById(revisaoToConclude?.veiculo_id)"
      @close="showConcluirModal = false"
      @concluded="handleRevisionConcluded"
    />

    <!-- Modal de Manutenção Corretiva Avulsa -->
    <CorrectiveMaintenanceModal 
      :isOpen="showCorretivaModal"
      :allVehicles="vehicles"
      @close="showCorretivaModal = false"
      @created="handleCorretivaCreated"
    />

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950 py-4 text-center text-xs text-slate-500">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
        <span>AutoCare • Controle de Manutenção Veicular • Porta :8015</span>
        <span class="text-slate-600">Integrado ao DevHub (C:\projetos)</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import FleetOverview from './components/FleetOverview.vue'
import MonitoredItemsList from './components/MonitoredItemsList.vue'
import PlannedRevisionView from './components/PlannedRevisionView.vue'
import MaintenanceTimeline from './components/MaintenanceTimeline.vue'
import FinancialDashboard from './components/FinancialDashboard.vue'
import OdometerModal from './components/OdometerModal.vue'
import CompleteRevisionModal from './components/CompleteRevisionModal.vue'
import CorrectiveMaintenanceModal from './components/CorrectiveMaintenanceModal.vue'

const activeTab = ref('frota')
const vehicles = ref([])
const selectedVehicle = ref(null)
const plannedCount = ref(0)

// Modal states
const showOdometerModal = ref(false)
const vehicleForOdometer = ref(null)

const showConcluirModal = ref(false)
const revisaoToConclude = ref(null)

const showCorretivaModal = ref(false)

// Component refs
const plannedViewRef = ref(null)
const timelineRef = ref(null)
const dashboardRef = ref(null)

const fetchVehicles = async () => {
  try {
    const res = await fetch('/api/veiculos')
    if (res.ok) {
      vehicles.value = await res.json()
      if (!selectedVehicle.value && vehicles.value.length > 0) {
        selectedVehicle.value = vehicles.value[0]
      }
    }
  } catch (e) {
    console.error(e)
  }
}

const fetchPlannedCount = async () => {
  try {
    const res = await fetch('/api/revisoes?status=PLANEJADA')
    if (res.ok) {
      const revs = await res.json()
      plannedCount.value = revs.length
    }
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  fetchVehicles()
  fetchPlannedCount()
})

const handleTabChange = (tab) => {
  activeTab.value = tab
}

const selectVehiclePlan = (v) => {
  selectedVehicle.value = v
  activeTab.value = 'plano'
}

const viewVehicleRevisions = (v) => {
  activeTab.value = 'revisoes'
}

const handleChangeVehicle = (veicId) => {
  const v = vehicles.value.find(x => x.id === veicId)
  if (v) selectedVehicle.value = v
}

const getVehicleById = (id) => {
  return vehicles.value.find(x => x.id === id)
}

// Odometer
const openOdometerModal = (v) => {
  vehicleForOdometer.value = v
  showOdometerModal.value = true
}

const handleOdometerUpdated = () => {
  fetchVehicles()
  fetchPlannedCount()
}

// Complete Revision
const openConcluirModal = (rev) => {
  revisaoToConclude.value = rev
  showConcluirModal.value = true
}

const handleRevisionConcluded = () => {
  fetchVehicles()
  fetchPlannedCount()
  activeTab.value = 'historico'
  if (timelineRef.value?.fetchManutencoes) {
    timelineRef.value.fetchManutencoes()
  }
}

// Corrective
const openCorretivaModal = () => {
  showCorretivaModal.value = true
}

const handleCorretivaCreated = () => {
  fetchVehicles()
  activeTab.value = 'historico'
  if (timelineRef.value?.fetchManutencoes) {
    timelineRef.value.fetchManutencoes()
  }
}
</script>
