import { useAuthStore } from '~/stores/auth';

export const useNavigation = () => {
  const authStore = useAuthStore();

  const baseLinks = [
    {
      label: 'Dashboard',
      icon: 'i-heroicons-home',
      to: '/',
    },
    {
      label: 'Analysis Tools',
      children: [
        {
          label: 'URL Analysis',
          icon: 'i-heroicons-link',
          to: '/url-analysis',
          description: 'Analyze URLs for security vulnerabilities (DAST)'
        },
        {
          label: 'Code Analysis',
          icon: 'i-heroicons-code-bracket',
          to: '/code-analysis',
          description: 'Scan code for security issues (SAST)'
        },
        {
          label: 'Headers Analyzer',
          icon: 'i-heroicons-shield-check',
          to: '/headers-analyzer',
          description: 'Analyze HTTP security headers'
        },
        {
          label: 'JWT Analyzer',
          icon: 'i-heroicons-key',
          to: '/jwt-analyzer',
          description: 'Analyze and test JWT tokens'
        },
        {
          label: 'File Upload Auditor',
          icon: 'i-heroicons-document-arrow-up',
          to: '/file-upload-auditor',
          description: 'Test file upload security'
        }
      ]
    },
    {
      label: 'Security Tools',
      children: [
        {
          label: 'Payload Tools',
          icon: 'i-heroicons-beaker',
          to: '/payload-tools',
          description: 'Generate and test security payloads'
        },
        {
          label: 'XSS Exploit Assistant',
          icon: 'i-heroicons-shield-exclamation',
          to: '/xss-exploit-assistant',
          description: 'XSS vulnerability exploitation'
        },
        {
          label: 'DOM XSS Pathfinder',
          icon: 'i-heroicons-bug-ant',
          to: '/dom-xss-pathfinder',
          description: 'Find DOM-based XSS vulnerabilities'
        },
        {
          label: 'PrivEsc Pathfinder',
          icon: 'i-heroicons-arrow-trending-up',
          to: '/privesc-pathfinder',
          description: 'Find privilege escalation paths'
        }
      ]
    },
    {
      label: 'Discovery',
      children: [
        {
          label: 'JS Recon',
          icon: 'i-heroicons-magnifying-glass-circle',
          to: '/js-recon',
          description: 'JavaScript reconnaissance and analysis'
        },
        {
          label: 'Discovery Tools',
          icon: 'i-heroicons-globe-alt',
          to: '/discovery-tools',
          description: 'Discover endpoints and resources'
        }
      ]
    },
    {
      label: 'WebSec Agent',
      icon: 'i-heroicons-chat-bubble-left-right',
      to: '/websec-agent',
    },
    {
      label: 'Developer Showcase',
      icon: 'i-heroicons-users',
      to: '/developer-showcase',
    },
    // {
    //   label: 'History',
    //   icon: 'i-heroicons-clock',
    //   to: '/history',
    // }
  ];

  const navigationLinks = computed(() => {
    const links = [...baseLinks];

    // Conditionally expose Admin link for admin users
    if (authStore.userRole === 'admin') {
      links.push({
        label: 'Admin',
        icon: 'i-heroicons-cog-8-tooth',
        to: '/admin'
      });
    }

    return links;
  });

  return { navigationLinks };
};
