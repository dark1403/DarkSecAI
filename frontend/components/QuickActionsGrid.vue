<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
    <UButton
      v-for="action in actions"
      :key="action.to"
      :to="action.to"
      :icon="action.icon"
      :color="action.color || 'gray'"
      variant="soft"
      block
      size="lg"
      class="justify-start group hover:scale-105 transition-all shadow-lg"
      :class="`hover:shadow-${action.color}-500/25`"
    >
      <template #leading>
        <div :class="[getIconBg(action.color), 'p-2 rounded-lg group-hover:scale-110 transition-transform']">
          <UIcon :name="action.icon" class="h-5 w-5" />
        </div>
      </template>
      
      <div class="flex flex-col items-start text-left flex-1">
        <span class="font-semibold">{{ action.label }}</span>
        <span v-if="action.description" class="text-xs opacity-75 mt-0.5">
          {{ action.description }}
        </span>
      </div>
      
      <template #trailing>
        <UIcon name="i-heroicons-arrow-right" class="h-4 w-4 opacity-50 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
      </template>
    </UButton>
  </div>
</template>

<script setup>
const actions = [
  {
    label: 'URL Analysis',
    description: 'Scan a website',
    icon: 'i-heroicons-link',
    to: '/url-analysis',
    color: 'cyan'
  },
  {
    label: 'Code Analysis',
    description: 'Analyze source code',
    icon: 'i-heroicons-code-bracket',
    to: '/code-analysis',
    color: 'blue'
  },
  {
    label: 'WebSec Agent',
    description: 'Ask AI assistant',
    icon: 'i-heroicons-chat-bubble-left-right',
    to: '/websec-agent',
    color: 'purple'
  },
  {
    label: 'Payload Tools',
    description: 'Generate payloads',
    icon: 'i-heroicons-beaker',
    to: '/payload-tools',
    color: 'green'
  },
  {
    label: 'JWT Analyzer',
    description: 'Test JWT tokens',
    icon: 'i-heroicons-key',
    to: '/jwt-analyzer',
    color: 'yellow'
  },
  {
    label: 'Discovery Tools',
    description: 'Find endpoints',
    icon: 'i-heroicons-globe-alt',
    to: '/discovery-tools',
    color: 'indigo'
  }
];

const getIconBg = (color) => {
  const colorMap = {
    cyan: 'bg-cyan-500/20',
    blue: 'bg-blue-500/20',
    purple: 'bg-purple-500/20',
    green: 'bg-green-500/20',
    yellow: 'bg-yellow-500/20',
    indigo: 'bg-indigo-500/20'
  };
  return colorMap[color] || 'bg-gray-500/20';
};
</script>