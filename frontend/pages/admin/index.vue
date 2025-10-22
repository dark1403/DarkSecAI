<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-900/20 via-cyan-900/20 to-pink-900/20 p-8 border border-purple-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10 flex items-center justify-between">
        <div>
          <h1 class="text-4xl font-bold bg-gradient-to-r from-purple-400 via-cyan-400 to-pink-400 bg-clip-text text-transparent">
            Admin Panel
          </h1>
          <p class="text-gray-300 mt-2 text-lg">Manage users, settings, and system insights</p>
        </div>
        <div class="flex gap-2">
          <UButton icon="i-heroicons-arrow-uturn-left" variant="soft" color="gray" to="/">Back to Dashboard</UButton>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-users" class="h-5 w-5 text-purple-400" />
            <h2 class="text-sm font-semibold text-white">Users</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-purple-300">{{ stats.usersTotal }}</div>
        <p class="text-gray-400 mt-1">Total registered users</p>
      </UCard>

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-user-plus" class="h-5 w-5 text-fuchsia-400" />
            <h2 class="text-sm font-semibold text-white">Admins</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-fuchsia-300">{{ stats.adminsTotal }}</div>
        <p class="text-gray-400 mt-1">Staff/superusers</p>
      </UCard>

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-shield-check" class="h-5 w-5 text-emerald-400" />
            <h2 class="text-sm font-semibold text-white">Role</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-emerald-300 capitalize">{{ authStore.userRole }}</div>
        <p class="text-gray-400 mt-1">Current user role</p>
      </UCard>

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-clipboard-document-list" class="h-5 w-5 text-amber-400" />
            <h2 class="text-sm font-semibold text-white">Audit Logs</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-amber-300">{{ stats.auditEvents }}</div>
        <p class="text-gray-400 mt-1">Recent admin events</p>
      </UCard>
    </div>

    <!-- Feature Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-clipboard" class="h-5 w-5 text-cyan-400" />
            <h2 class="text-sm font-semibold text-white">Vulnerability Reports</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-cyan-300">{{ stats.reportsTotal }}</div>
      </UCard>

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-bug-ant" class="h-5 w-5 text-red-400" />
            <h2 class="text-sm font-semibold text-white">Vulnerabilities</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-red-300">{{ stats.vulnerabilitiesTotal }}</div>
      </UCard>

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-shield-check" class="h-5 w-5 text-green-400" />
            <h2 class="text-sm font-semibold text-white">Headers Reports</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-green-300">{{ stats.headersReportsTotal }}</div>
      </UCard>

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-command-line" class="h-5 w-5 text-yellow-400" />
            <h2 class="text-sm font-semibold text-white">DOM XSS Results</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-yellow-300">{{ stats.domxssResultsTotal }}</div>
      </UCard>

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-beaker" class="h-5 w-5 text-purple-400" />
            <h2 class="text-sm font-semibold text-white">Payload Forge Results</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-purple-300">{{ stats.payloadResultsTotal }}</div>
      </UCard>

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-exclamation-triangle" class="h-5 w-5 text-pink-400" />
            <h2 class="text-sm font-semibold text-white">XSS Payload Results</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-pink-300">{{ stats.xssPayloadResultsTotal }}</div>
      </UCard>

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-document-arrow-up" class="h-5 w-5 text-blue-400" />
            <h2 class="text-sm font-semibold text-white">File Upload Results</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-blue-300">{{ stats.fileUploadResultsTotal }}</div>
      </UCard>

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-chat-bubble-left-right" class="h-5 w-5 text-indigo-400" />
            <h2 class="text-sm font-semibold text-white">Conversations</h2>
          </div>
        </template>
        <div class="text-4xl font-bold text-indigo-300">{{ stats.conversationsTotal }}</div>
      </UCard>
    </div>

    <!-- Breakdown and Settings -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-fire" class="h-5 w-5 text-red-400" />
            <h2 class="text-lg font-bold bg-gradient-to-r from-red-400 to-yellow-400 bg-clip-text text-transparent">Severity Breakdown</h2>
          </div>
        </template>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <div class="p-3 rounded-lg bg-red-900/30 border border-red-500/30 text-center">
            <div class="text-xl font-bold text-red-300">{{ severity('Critical') }}</div>
            <div class="text-xs text-gray-300">Critical</div>
          </div>
          <div class="p-3 rounded-lg bg-orange-900/30 border border-orange-500/30 text-center">
            <div class="text-xl font-bold text-orange-300">{{ severity('High') }}</div>
            <div class="text-xs text-gray-300">High</div>
          </div>
          <div class="p-3 rounded-lg bg-yellow-900/30 border border-yellow-500/30 text-center">
            <div class="text-xl font-bold text-yellow-300">{{ severity('Medium') }}</div>
            <div class="text-xs text-gray-300">Medium</div>
          </div>
          <div class="p-3 rounded-lg bg-green-900/30 border border-green-500/30 text-center">
            <div class="text-xl font-bold text-green-300">{{ severity('Low') }}</div>
            <div class="text-xs text-gray-300">Low</div>
          </div>
          <div class="p-3 rounded-lg bg-cyan-900/30 border border-cyan-500/30 text-center">
            <div class="text-xl font-bold text-cyan-300">{{ severity('Info') }}</div>
            <div class="text-xs text-gray-300">Info</div>
          </div>
          <div class="p-3 rounded-lg bg-gray-900/30 border border-gray-500/30 text-center">
            <div class="text-xl font-bold text-gray-300">{{ severity('Unknown') }}</div>
            <div class="text-xs text-gray-300">Unknown</div>
          </div>
        </div>
      </UCard>

      <!-- <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-key" class="h-5 w-5 text-cyan-400" />
            <h2 class="text-lg font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">API Keys</h2>
          </div>
        </template>
        <ul class="space-y-2 text-gray-300">
          <li class="flex items-center justify-between" v-for="(configured, key) in stats.apiKeysMap" :key="key">
            <span class="font-medium">{{ key }}</span>
            <span :class="configured ? 'text-emerald-400' : 'text-red-400'">
              <UIcon :name="configured ? 'i-heroicons-check-circle' : 'i-heroicons-x-circle'" class="h-5 w-5" />
            </span>
          </li>
        </ul>
        <div class="text-sm text-gray-400 mt-3">Configured: {{ stats.apiKeysConfigured }}</div>
      </UCard> -->

      <UCard class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-heroicons-queue-list" class="h-5 w-5 text-amber-400" />
            <h2 class="text-lg font-bold bg-gradient-to-r from-amber-400 to-yellow-400 bg-clip-text text-transparent">Audit & Activity</h2>
          </div>
        </template>
        <div class="space-y-3">
          <p class="text-gray-300">Last event: {{ lastAuditEvent }}</p>
          <p class="text-gray-300">Total activity events: {{ stats.auditEvents }}</p>
          <UButton icon="i-heroicons-arrow-path" variant="soft" color="amber" @click="refreshAudit">Refresh</UButton>
        </div>
      </UCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';
import adminService, { type AdminStats } from '~/services/api/adminService';

definePageMeta({
  middleware: ['auth', 'admin']
});

const authStore = useAuthStore();

const stats = reactive({
  usersTotal: 0,
  adminsTotal: 0,
  reportsTotal: 0,
  vulnerabilitiesTotal: 0,
  headersReportsTotal: 0,
  domxssResultsTotal: 0,
  payloadResultsTotal: 0,
  xssPayloadResultsTotal: 0,
  fileUploadResultsTotal: 0,
  conversationsTotal: 0,
  apiKeysConfigured: 0,
  apiKeysMap: {} as Record<string, boolean>,
  severityBreakdown: {} as Record<string, number>,
  auditEvents: 0,
});

const lastAuditEvent = ref('No recent events');

onMounted(async () => {
  // Initialize auth and load stats
  authStore.initialize();
  await loadStats();
});

async function loadStats() {
  try {
    const data: AdminStats = await adminService.getStats();
    stats.usersTotal = data.users_total;
    stats.adminsTotal = data.admins_total;
    stats.reportsTotal = data.reports_total;
    stats.vulnerabilitiesTotal = data.vulnerabilities_total;
    stats.headersReportsTotal = data.headers_reports_total;
    stats.domxssResultsTotal = data.domxss_results_total;
    stats.payloadResultsTotal = data.payload_results_total;
    stats.xssPayloadResultsTotal = data.xss_payload_results_total;
    stats.fileUploadResultsTotal = data.file_upload_results_total;
    stats.conversationsTotal = data.conversations_total;
    stats.apiKeysConfigured = data.api_keys_configured;
    stats.apiKeysMap = data.api_keys || {};
    stats.severityBreakdown = data.severity_breakdown || {};
    stats.auditEvents = data.audit_events;
    lastAuditEvent.value = data.last_event
      ? new Date(data.last_event).toLocaleString()
      : 'No recent events';
  } catch (e) {
    useToast().add({ title: 'Failed to load admin stats', color: 'red' });
  }
}

const refreshAudit = async () => {
  await loadStats();
};

function severity(name: string): number {
  return stats.severityBreakdown[name] || 0;
}
</script>
