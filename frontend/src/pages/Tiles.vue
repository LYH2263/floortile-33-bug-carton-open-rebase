<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'

const items = ref([])
const err = ref('')

onMounted(async () => {
  items.value = (await getJSON('/api/tiles')).items
})

async function saveBox(t) {
  err.value = ''
  const n = Number(t.pieces_per_box)
  if (!Number.isInteger(n) || n <= 0) {
    err.value = `砖型「${t.name}」每箱片数必须为正整数`
    return
  }
  try {
    const updated = await putJSON(`/api/tiles/${t.id}`, { pieces_per_box: n })
    Object.assign(t, updated)
  } catch (e) {
    err.value = e.message
  }
}
</script>
<template>
  <div class="page">
    <h1>砖型库</h1>
    <p v-if="err" class="alert">{{ err }}</p>
    <div class="tile-cards">
      <div v-for="t in items" :key="t.id" class="tile-card" :class="{ dirty: t.data_quality === 'dirty' }">
        <strong>{{ t.name }}</strong>
        <span>{{ t.tile_l }} × {{ t.tile_w }} m</span>
        <em v-if="t.data_quality === 'dirty'">无效规格</em>
        <label class="box-field">
          每箱片数
          <input type="number" min="1" step="1" v-model.number="t.pieces_per_box" />
        </label>
        <button @click="saveBox(t)">保存</button>
      </div>
    </div>
  </div>
</template>
