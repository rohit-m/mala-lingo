<script setup>
const props = defineProps({
  label: String,
  onClick: Function,
  variant: {
    type: String,
    default: 'filled',
    validator: (value) => ['filled', 'outlined'].includes(value)
  }
})

const handleClick = () => {
  props.onClick()
}
</script>
<template>
  <button 
    @click="props.onClick" 
    :class="[
      'btn',
      variant === 'outlined' ? 'btn-outlined' : 'btn-filled'
    ]"
  >
    {{ props.label }}
  </button>
</template>
<style scoped>
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  min-width: 150px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-filled {
  background-color: #4CAF50;
  color: white;
  border: 2px solid #4CAF50;
}

.btn-filled:hover {
  background-color: #45a049;
  border-color: #45a049;
}

.btn-outlined {
  background-color: transparent;
  color: #4CAF50;
  border: 2px solid #4CAF50;
}

.btn-outlined:hover {
  background-color: #4CAF50;
  color: white;
}
</style>