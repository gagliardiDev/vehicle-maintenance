<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
      <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/60 shrink-0">
        <div>
          <span class="text-[10px] font-bold uppercase tracking-wider text-rose-400">Reparo de Emergência</span>
          <h3 class="font-bold text-white text-base">+ Nova Manutenção Corretiva Avulsa</h3>
        </div>
        <button @click="$emit('close')" class="text-slate-400 hover:text-white p-1">✕</button>
      </div>

      <form @submit.prevent="handleSave" class="p-6 overflow-y-auto space-y-4 flex-1">
        <div>
          <label class="block text-xs font-semibold text-slate-400 mb-1">Veículo</label>
          <select 
            v-model="form.veiculo_id"
            required
            class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3 py-2 rounded-lg outline-none focus:border-rose-500"
          >
            <option v-for="v in allVehicles" :key="v.id" :value="v.id">{{ v.nome }}</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-400 mb-1">Título da Manutenção</label>
          <input 
            v-model="form.titulo" 
            type="text" 
            required
            placeholder="Ex: Troca de Pneu Furado / Bateria Arriada"
            class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3.5 py-2 rounded-lg outline-none focus:border-rose-500"
          />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Odômetro (KM)</label>
            <input 
              v-model.number="form.odometro" 
              type="number" 
              required
              class="w-full bg-slate-950 border border-slate-700 text-white font-mono text-sm px-3 py-2 rounded-lg outline-none focus:border-rose-500"
            />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Data</label>
            <input 
              v-model="form.data_execucao" 
              type="date" 
              required
              class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3 py-2 rounded-lg outline-none focus:border-rose-500"
            />
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-400 mb-1">Oficina / Estabelecimento</label>
          <input 
            v-model="form.oficina_local" 
            type="text" 
            placeholder="Ex: Borracharia / Auto Elétrico"
            class="w-full bg-slate-950 border border-slate-700 text-white text-sm px-3 py-2 rounded-lg outline-none focus:border-rose-500"
          />
        </div>

        <!-- Despesas -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-300">Despesas Envolvidas</span>
            <button 
              type="button" 
              @click="addDespesa"
              class="text-xs text-rose-400 hover:text-rose-300 font-semibold"
            >
              + Adicionar Despesa
            </button>
          </div>

          <div class="space-y-2">
            <div 
              v-for="(d, idx) in form.despesas" 
              :key="idx"
              class="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center gap-2"
            >
              <select 
                v-model="d.tipo"
                class="bg-slate-900 border border-slate-700 text-[10px] font-bold text-white rounded px-2 py-1 outline-none"
              >
                <option value="PECA">PEÇA</option>
                <option value="SERVICO">SERVIÇO</option>
              </select>
              <input 
                v-model="d.descricao" 
                type="text" 
                required
                placeholder="Descrição"
                class="flex-1 bg-transparent border-b border-slate-800 text-xs text-white px-1 py-0.5 outline-none focus:border-rose-500"
              />
              <div class="w-16">
                <input 
                  v-model.number="d.quantidade" 
                  type="number" 
                  step="0.1" 
                  min="0.1"
                  placeholder="Qtd"
                  class="w-full bg-slate-900 border border-slate-700 text-xs text-center font-mono text-white rounded px-1 py-1"
                />
              </div>
              <div class="w-20">
                <input 
                  v-model.number="d.valor_unitario" 
                  type="number" 
                  step="0.01" 
                  min="0"
                  placeholder="R$"
                  class="w-full bg-slate-900 border border-slate-700 text-xs text-right font-mono text-white rounded px-1 py-1"
                />
              </div>
              <button 
                type="button" 
                @click="removeDespesa(idx)" 
                class="text-slate-600 hover:text-rose-400 p-1"
              >
                ✕
              </button>
            </div>
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-400 mb-1">Observações</label>
          <textarea 
            v-model="form.observacoes" 
            rows="2"
            placeholder="Causa da falha ou detalhes adicionais..."
            class="w-full bg-slate-950 border border-slate-700 text-white text-xs px-3 py-2 rounded-lg outline-none focus:border-rose-500"
          ></textarea>
        </div>

        <div v-if="error" class="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
          {{ error }}
        </div>
      </form>

      <div class="px-6 py-4 bg-slate-950 border-t border-slate-800 flex items-center justify-between shrink-0">
        <button 
          type="button" 
          @click="$emit('close')"
          class="px-4 py-2 rounded-lg text-xs font-semibold text-slate-400 hover:text-white"
        >
          Cancelar
        </button>
        <button 
          type="button"
          @click="handleSave"
          :disabled="saving"
          class="px-5 py-2.5 rounded-xl text-xs font-bold bg-rose-600 hover:bg-rose-500 text-white transition-all shadow-lg shadow-rose-600/30 disabled:opacity-50"
        >
          {{ saving ? 'Salvando...' : 'Gravar Manutenção' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  allVehicles: { type: Array, default: () => [] }
})
const emit = defineEmits(['close', 'created'])

const form = ref({
  veiculo_id: null,
  titulo: '',
  odometro: 0,
  data_execucao: new Date().toISOString().substring(0, 10),
  oficina_local: '',
  observacoes: '',
  despesas: []
})

const saving = ref(false)
const error = ref('')

watch(() => props.isOpen, (val) => {
  if (val) {
    error.value = ''
    const defaultVeic = props.allVehicles[0]
    form.value = {
      veiculo_id: defaultVeic?.id || 1,
      titulo: '',
      odometro: defaultVeic?.odometro_referencia || 0,
      data_execucao: new Date().toISOString().substring(0, 10),
      oficina_local: '',
      observacoes: '',
      despesas: [
        { tipo: 'PECA', descricao: '', part_number: '', fornecedor: '', quantidade: 1.0, valor_unitario: 0.0 }
      ]
    }
  }
})

const addDespesa = () => {
  form.value.despesas.push({
    tipo: 'PECA',
    descricao: '',
    part_number: '',
    fornecedor: '',
    quantidade: 1.0,
    valor_unitario: 0.0
  })
}

const removeDespesa = (idx) => {
  form.value.despesas.splice(idx, 1)
}

const handleSave = async () => {
  if (!form.value.titulo) {
    error.value = 'Informe o título da manutenção.'
    return
  }
  saving.value = true
  error.value = ''
  try {
    const res = await fetch('/api/manutencoes/corretiva', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.detail || 'Erro ao registrar manutenção corretiva')
    }
    const created = await res.json()
    emit('created', created)
    emit('close')
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}
</script>
