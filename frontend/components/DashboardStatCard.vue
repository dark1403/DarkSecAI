<template>
  <UCard 
    :ui="{ 
      body: { padding: 'p-6' },
      background: 'bg-gradient-to-br from-gray-800/80 to-gray-900/80',
      ring: 'ring-1 ring-gray-700/50',
      shadow: 'shadow-xl hover:shadow-2xl',
    }" 
    class="backdrop-blur-sm transition-all duration-300 hover:scale-105 group border border-gray-700/50"
  >
    <div class="flex items-center justify-between">
      <div class="flex-1">
        <p class="text-sm font-medium text-gray-400 uppercase tracking-wide">{{ title }}</p>
        <p class="mt-3 text-4xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent group-hover:from-primary group-hover:to-purple-400 transition-all duration-300">
          {{ value }}
        </p>
        <div v-if="trend" class="mt-3 flex items-center text-sm">
          <UIcon 
            :name="trend.isPositive ? 'i-heroicons-arrow-trending-up' : 'i-heroicons-arrow-trending-down'" 
            :class="trend.isPositive ? 'text-green-400' : 'text-red-400'"
            class="h-5 w-5 mr-1.5 transition-transform group-hover:scale-110"
          />
          <span :class="trend.isPositive ? 'text-green-400' : 'text-red-400'" class="font-semibold">
            {{ trend.value }}
          </span>
          <span class="text-gray-400 ml-1.5">{{ trend.label }}</span>
        </div>
      </div>
      <div v-if="icon" class="flex-shrink-0">
        <div 
          :class="[iconBgClass, 'rounded-2xl p-4 transition-all duration-300 group-hover:scale-110 group-hover:rotate-6']"
          class="relative overflow-hidden"
        >
          <div class="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent"></div>
          <UIcon :name="icon" class="h-8 w-8 relative z-10" :class="iconColorClass" />
        </div>
      </div>
    </div>
  </UCard>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  icon: {
    type: String,
    default: null
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'success', 'warning', 'danger', 'info'].includes(value)
  },
  trend: {
    type: Object,
    default: null,
  }
});

const iconColorClass = computed(() => {
  const colorMap = {
    primary: 'text-cyan-400',
    success: 'text-green-400',
    warning: 'text-yellow-400',
    danger: 'text-red-400',
    info: 'text-blue-400'
  };
  return colorMap[props.color] || colorMap.primary;
});

const iconBgClass = computed(() => {
  const colorMap = {
    primary: 'bg-gradient-to-br from-cyan-500/20 to-purple-500/20',
    success: 'bg-gradient-to-br from-green-500/20 to-emerald-500/20',
    warning: 'bg-gradient-to-br from-yellow-500/20 to-orange-500/20',
    danger: 'bg-gradient-to-br from-red-500/20 to-pink-500/20',
    info: 'bg-gradient-to-br from-blue-500/20 to-indigo-500/20'
  };
  return colorMap[props.color] || colorMap.primary;
});
</script>