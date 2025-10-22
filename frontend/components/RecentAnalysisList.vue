<template>
  <div class="space-y-3">
    <div v-if="analyses.length === 0" class="text-center py-12">
      <div class="inline-block p-4 bg-gradient-to-br from-gray-700/50 to-gray-800/50 rounded-full mb-4">
        <UIcon name="i-heroicons-inbox" class="h-12 w-12 text-gray-500" />
      </div>
      <p class="text-gray-400 font-medium">No recent analyses</p>
      <p class="text-sm text-gray-500 mt-1">Start by running a scan</p>
    </div>
    
    <div 
      v-for="(analysis, index) in analyses" 
      :key="index"
      class="flex items-start justify-between p-4 hover:bg-gray-700/30 rounded-xl cursor-pointer transition-all group border border-transparent hover:border-primary/30 hover:scale-[1.02] backdrop-blur-sm"
      @click="$emit('select', analysis)"
    >
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-3 mb-2">
          <div :class="[getIconBg(analysis.type), 'p-2 rounded-lg group-hover:scale-110 transition-transform']">
            <UIcon :name="getTypeIcon(analysis.type)" class="h-4 w-4" :class="getIconColor(analysis.type)" />
          </div>
          <p class="font-semibold text-sm truncate text-white group-hover:text-primary transition-colors">{{ analysis.target }}</p>
        </div>
        <div class="flex items-center gap-3 ml-11">
          <UBadge 
            :color="getSeverityColor(analysis.severity)" 
            size="xs"
            class="shadow-sm"
          >
            {{ analysis.severity }}
          </UBadge>
          <span class="text-xs text-gray-400">
            <span class="font-semibold text-white">{{ analysis.vulnerabilitiesCount }}</span> findings
          </span>
          <span class="text-xs text-gray-500">{{ formatTime(analysis.timestamp) }}</span>
        </div>
      </div>
      <UIcon 
        name="i-heroicons-chevron-right" 
        class="h-5 w-5 text-gray-500 group-hover:text-primary group-hover:translate-x-1 transition-all flex-shrink-0" 
      />
    </div>
  </div>
</template>

<script setup>
defineProps({
  analyses: {
    type: Array,
    required: true,
    default: () => []
  }
});

defineEmits(['select']);

const getTypeIcon = (type) => {
  const iconMap = {
    'url': 'i-heroicons-link',
    'code': 'i-heroicons-code-bracket',
    'jwt': 'i-heroicons-key',
    'upload': 'i-heroicons-document-arrow-up',
    'payload': 'i-heroicons-beaker'
  };
  return iconMap[type] || 'i-heroicons-document';
};

const getIconColor = (type) => {
  const colorMap = {
    'url': 'text-cyan-400',
    'code': 'text-blue-400',
    'jwt': 'text-purple-400',
    'upload': 'text-green-400',
    'payload': 'text-yellow-400'
  };
  return colorMap[type] || 'text-gray-400';
};

const getIconBg = (type) => {
  const colorMap = {
    'url': 'bg-cyan-500/20',
    'code': 'bg-blue-500/20',
    'jwt': 'bg-purple-500/20',
    'upload': 'bg-green-500/20',
    'payload': 'bg-yellow-500/20'
  };
  return colorMap[type] || 'bg-gray-500/20';
};

const getSeverityColor = (severity) => {
  const colorMap = {
    'Critical': 'red',
    'High': 'orange',
    'Medium': 'yellow',
    'Low': 'green',
    'Info': 'blue'
  };
  return colorMap[severity] || 'gray';
};

const formatTime = (timestamp) => {
  const now = new Date();
  const time = new Date(timestamp);
  const diffMs = now - time;
  const diffMins = Math.floor(diffMs / 60000);
  
  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `${diffHours}h ago`;
  
  const diffDays = Math.floor(diffHours / 24);
  if (diffDays < 7) return `${diffDays}d ago`;
  
  return time.toLocaleDateString();
};
</script>