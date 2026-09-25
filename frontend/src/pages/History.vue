<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const items = ref([])
const openId = ref(null)
const detail = ref(null)

onMounted(async () => { items.value = (await getJSON('/api/runs')).items })

async function toggle(id) {
  if (openId.value === id) { openId.value = null; detail.value = null; return }
  openId.value = id
  detail.value = await getJSON(`/api/runs/${id}`)
}

function snap(run) {
  const r = run.result || {}
  const n = r.pieces_per_box ?? 1
  return {
    piecesPerBox: n,
    before: r.order_count,
    boxes: r.box_count ?? r.order_count,
    rounded: r.order_count_rounded ?? r.order_count,
  }
}
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>片数</th><th></th></tr></thead>
      <tbody>
        <template v-for="r in items" :key="r.id">
          <tr class="clickable">
            <td>{{ r.created_at?.slice(0, 19) }}</td>
            <td>{{ r.room_name }}</td>
            <td>{{ r.tile_name }}</td>
            <td>{{ snap(r).rounded }}</td>
            <td><button class="link-btn" @click="toggle(r.id)">{{ openId === r.id ? '收起' : '详情' }}</button></td>
          </tr>
          <tr v-if="openId === r.id && detail" class="run-detail">
            <td colspan="5">
              <dl>
                <dt>进位前</dt><dd>{{ snap(detail).before }} 片</dd>
                <dt>每箱片数</dt><dd>{{ snap(detail).piecesPerBox }}</dd>
                <dt>箱数</dt><dd>{{ snap(detail).boxes }}</dd>
                <dt>进位后</dt><dd>{{ snap(detail).rounded }} 片</dd>
                <dt>损耗</dt><dd>{{ detail.waste_pct }}%</dd>
              </dl>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
