<script setup>
import { computed } from 'vue'

const props = defineProps({
  result: { type: Object, default: null },
})

// Old results saved before box rounding exist lack the new fields; treat as N=1.
const rounded = computed(() => props.result?.order_count_rounded ?? props.result?.order_count)
const hasBoxing = computed(() => props.result?.pieces_per_box != null)
</script>
<template>
  <div v-if="result" class="order-summary">
    <div class="hero">{{ rounded }} 片</div>
    <ul>
      <li>净用量 {{ result.raw_count }} 片，损耗 {{ result.waste_pct }}%</li>
      <li>地面 {{ result.area_m2 }} m²，单砖 {{ result.piece_m2 }} m²</li>
      <li v-if="hasBoxing">
        整箱进位：进位前 {{ result.order_count }} 片，每箱 {{ result.pieces_per_box }} 片
        × {{ result.box_count }} 箱 = {{ result.order_count_rounded }} 片
      </li>
    </ul>
  </div>
</template>
