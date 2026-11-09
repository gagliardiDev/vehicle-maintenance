<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-800/60 shrink-0">
        <div>
          <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-400">Oficina & Conclusão</span>
          <h3 class="font-bold text-white text-base">Concluir Revisão e Salvar Histórico</h3>
        </div>
        <button @click="$emit('close')" class="text-slate-400 hover:text-white p-1">✕</button>
      </div>

      <!-- Scrollable Form Body -->
      <form @submit.prevent="handleConclude" class="p-6 overflow-y-auto space-y-5 flex-1">
        <!-- Execution Meta Fields -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 bg-slate-950 p-4 rounded-xl border border-slate-800">
          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Odômetro Final (KM)</label>
            <input 
              v-model.number="form.odometro_real" 
              type="number" 
              required
              class="w-full bg-slate-900 border border-slate-700 text-white font-mono font-bold text-sm px-3 py-2 rounded-lg outline-none focus:border-emerald-500"
            />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Data da Conclusão</label>
            <input 
              v-model="form.data_execucao" 
              type="date" 
              required
              class="w-full bg-slate-900 border border-slate-700 text-white text-sm px-3 py-2 rounded-lg outline-none focus:border-emerald-500"
            />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-400 mb-1">Oficina / Estabelecimento</label>
            <input 
              v-model="form.oficina_local" 
              type="text" 
              placeholder="Ex: Oficina Mecânica Central"
              class="w-full bg-slate-900 border border-slate-700 text-white text-sm px-3 py-2 rounded-lg outline-none focus:border-emerald-500"
            />
          </div>
        </div>

        <!-- Itemized Expenses Table -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <div>
              <h4 class="text-xs font-bold uppercase tracking-wider text-slate-300">Despesas Itemizadas da Revisão</h4>
              <p class="text-[11px] text-slate-500">Valide os valores reais pagos e adicione imprevistos identificados no elevador.</p>
            </div>
            <button 
              type="button" 
              @click="addExtraItem"
              class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-600/10 hover:bg-blue-600/20 text-blue-400 border border-blue-500/30 transition-colors flex items-center gap-1"
            >
              + Adicionar Item Imprevisto
            </button>
          </div>

          <div class="space-y-2">
            <div 
              v-for="(item, idx) in form.despesas" 
              :key="idx"
              class="bg-slate-950 p-3 rounded-xl border border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
            >
              <div class="flex-1 space-y-1">
                <div class="flex items-center gap-2">
                  <select 
                    v-model="item.tipo"
                    class="text-[10px] font-bold rounded px-1.5 py-0.5 bg-slate-900 border border-slate-700 text-slate-300 outline-none"
                  >
                    <option value="PECA">PEÇA</option>
                    <option value="SERVICO">SERVIÇO</option>
                  </select>
                  <input 
                    v-model="item.descricao" 
                    type="text" 
                    required
                    placeholder="Descrição do item ou serviço"
                    class="flex-1 bg-transparent border-b border-slate-800 text-xs font-semibold text-white px-1 py-0.5 outline-none focus:border-blue-500"
                  />
                </div>
                <div class="flex items-center gap-2 text-[11px] text-slate-400">
                  <input 
                    v-model="item.part_number" 
                    type="text" 
                    placeholder="Part number / Ref"
                    class="w-32 bg-transparent border-b border-slate-800 text-[11px] font-mono text-slate-300 px-1 py-0.5 outline-none focus:border-blue-500"
                  />
                  <input 
                    v-model="item.fornecedor" 
                    type="text" 
                    placeholder="Fornecedor / Loja"
                    class="w-32 bg-transparent border-b border-slate-800 text-[11px] text-slate-300 px-1 py-0.5 outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <!-- Quantidade & Valor -->
              <div class="flex items-center gap-2 shrink-0">
                <div class="w-16">
                  <label class="block text-[9px] text-slate-500">Qtd</label>
                  <input 
                    v-model.number="item.quantidade" 
                    type="number" 
                    step="0.1" 
                    min="0.1"
                    class="w-full bg-slate-900 border border-slate-700 text-xs text-white text-center font-mono rounded px-1 py-1"
                  />
                </div>
                <div class="w-24">
                  <label class="block text-[9px] text-slate-500">Valor Unit. (R$)</label>
                  <input 
                    v-model.number="item.valor_unitario" 
                    type="number" 
                    step="0.01" 
                    min="0"
                    class="w-full bg-slate-900 border border-slate-700 text-xs text-white text-right font-mono rounded px-1 py-1"
                  />
                </div>
                <div class="w-20 text-right">
                  <span class="block text-[9px] text-slate-500">Total</span>
                  <span class="text-xs font-mono font-bold text-slate-200">
                    R$ {{ formatMoeda(item.quantidade * item.valor_unitario) }}
                  </span>
                </div>
                <button 
                  type="button" 
                  @click="removeItem(idx)"
                  class="text-slate-600 hover:text-rose-400 p-1 transition-colors"
                >
                  ✕
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Totals Summary Card -->
        <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
          <div class="flex items-center gap-4 text-xs">
            <div>
              <span class="text-slate-500 block">Total Peças:</span>
              <span class="font-mono font-bold text-blue-400">R$ {{ formatMoeda(totalPecas) }}</span>
            </div>
            <div>
              <span class="text-slate-500 block">Total Serviços:</span>
              <span class="font-mono font-bold text-purple-400">R$ {{ formatMoeda(totalServicos) }}</span>
            </div>
          </div>
          <div class="text-right">
            <span class="text-xs text-slate-400 uppercase font-bold block">Total Geral da Revisão</span>
            <span class="text-xl font-mono font-black text-emerald-400">R$ {{ formatMoeda(totalGeral) }}</span>
          </div>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-400 mb-1">Observações da Oficina</label>
          <textarea 
            v-model="form.observacoes" 
            rows="2"
            placeholder="Detalhes mecânicos, condições encontradas nas peças ou orientações para a próxima revisão..."
            class="w-full bg-slate-950 border border-slate-700 text-white text-xs px-3 py-2 rounded-lg outline-none focus:border-emerald-500"
          ></textarea>
        </div>

        <div v-if="error" class="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
          {{ error }}
        </div>
      </form>

      <!-- Footer Buttons -->
      <div class="px-6 py-4 bg-slate-950 border-t border-slate-800 flex items-center justify-between shrink-0">
        <button 
          type="button" 
          @click="$emit('close')"
          class="px-4 py-2 rounded-lg text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800"
        >
          Cancelar
        </button>
        <button 
          type="button"
          @click="handleConclude"
          :disabled="saving"
          class="px-5 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-all shadow-lg shadow-emerald-600/30 flex items-center gap-1.5 disabled:opacity-50"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span>{{ saving ? 'Concluindo...' : 'Salvar no Histórico & Atualizar Ciclos' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  revisao: Object,
  vehicle: Object
})
const emit = defineEmits(['close', 'concluded'])

const form = ref({
  odometro_real: 0,
  data_execucao: new Date().toISOString().substring(0, 10),
  oficina_local: 'Oficina Mecânica',
  observacoes: '',
  despesas: []
})

const saving = ref(false)
const error = ref('')

watch(() => props.isOpen, (val) => {
  if (val && props.revisao) {
    error.value = ''
    form.value.odometro_real = props.revisao.odometro_previsto || props.vehicle?.odometro_referencia || 0
    form.value.data_execucao = new Date().toISOString().substring(0, 10)
    form.value.oficina_local = 'Oficina Especializada'
    form.value.observacoes = props.revisao.observacoes || ''
    
    // Converte os itens planejados em despesas reais editáveis
    form.value.despesas = (props.revisao.itens || []).map(i => ({
      tipo: i.tipo,
      item_monitorado_id: i.item_monitorado_id,
      descricao: i.descricao,
      part_number: i.part_number || '',
      fornecedor: i.fornecedor || (i.tipo === 'PECA' ? 'Autopeças' : 'Oficina'),
      quantidade: i.quantidade || 1.0,
      valor_unitario: i.valor_estimado || 0.0
    }))
  }
})

const addExtraItem = () => {
  form.value.despesas.push({
    tipo: 'PECA',
    item_monitorado_id: null,
    descricao: '',
    part_number: '',
    fornecedor: 'Oficina',
    quantidade: 1.0,
    valor_unitario: 0.0
  })
}

const removeItem = (idx) => {
  form.value.despesas.splice(idx, 1)
}

const totalPecas = computed(() => {
  return form.value.despesas
    .filter(d => d.tipo === 'PECA')
    .reduce((acc, d) => acc + (d.quantidade * d.valor_unitario), 0)
})

const totalServicos = computed(() => {
  return form.value.despesas
    .filter(d => d.tipo === 'SERVICO')
    .reduce((acc, d) => acc + (d.quantidade * d.valor_unitario), 0)
})

const totalGeral = computed(() => {
  return totalPecas.value + totalServicos.value
})

const handleConclude = async () => {
  if (!form.value.odometro_real) {
    error.value = 'Informe o odômetro final.'
    return
  }
  saving.value = true
  error.value = ''
  try {
    const res = await fetch(`/api/revisoes/${props.revisao.id}/concluir`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })

    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.detail || 'Erro ao concluir revisão')
    }

    const manutencao = await res.json()
    emit('concluded', manutencao)
    emit('close')
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}

const formatMoeda = (val) => {
  if (val === undefined || val === null) return '0,00'
  return Number(val).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>
