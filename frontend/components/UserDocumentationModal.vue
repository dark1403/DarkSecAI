<template>
  <div class="bg-gray-800 rounded-lg shadow-xl p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold text-white">User Documentation</h2>
      <UButton
        icon="i-heroicons-x-mark"
        variant="ghost"
        color="gray"
        @click="$emit('close')"
      />
    </div>

    <div class="prose prose-invert max-w-none">
      <h3>DarkSec-AI User Guide</h3>
      
      <p>
        DarkSec-AI is a comprehensive web vulnerability analysis suite that leverages the power of Generative AI 
        to assist developers, penetration testers, and security analysts. It provides a rich set of tools for both 
        static (SAST) and dynamic (DAST) analysis, vulnerability research, and payload generation, all within a 
        single, intuitive interface.
      </p>
      
      <h4>Core Analysis Tools</h4>
      
      <ul>
        <li>
          <strong>WebSec Agent:</strong> An expert AI chat assistant for any web security question. Ask it about 
          security concepts, mitigation techniques, secure coding practices, or how to use security tools.
        </li>
        <li>
          <strong>URL Analysis (DAST):</strong> A non-invasive Dynamic Application Security Test. It uses the AI's 
          search capabilities to analyze a URL's structure, identify the technology stack, and search for public 
          vulnerabilities without sending any malicious traffic to the target.
        </li>
        <li>
          <strong>Code Analysis (SAST):</strong> A "white-box" testing tool. Paste a code snippet, and the AI will 
          act as an expert security code reviewer, looking for insecure functions, logic flaws, and common 
          vulnerability patterns.
        </li>
        <li>
          <strong>Security Headers Analyzer:</strong> Fetches and analyzes the live HTTP security headers of a target 
          URL, providing an overall security score and actionable recommendations.
        </li>
      </ul>
      
      <h4>Specialized Vulnerability Scanners</h4>
      
      <ul>
        <li>
          <strong>DOM XSS Pathfinder:</strong> A specialized tool that performs AI-powered static data flow analysis 
          on JavaScript code to identify DOM XSS vulnerabilities.
        </li>
        <li>
          <strong>JWT Decompiler & Auditor:</strong> Decode and analyze JSON Web Tokens with both defensive and 
          offensive perspectives.
        </li>
        <li>
          <strong>PrivEsc Pathfinder:</strong> An AI-powered research assistant for post-exploitation that searches 
          for known Privilege Escalation exploits.
        </li>
        <li>
          <strong>File Upload Auditor:</strong> A two-step tool to detect file upload forms on a website and generate 
          various types of malicious files to test the security.
        </li>
      </ul>
      
      <h4>Reconnaissance & Discovery Tools</h4>
      
      <ul>
        <li>
          <strong>JS Reconnaissance:</strong> A specialized static analysis tool that parses JavaScript files to find 
          hardcoded API endpoints, URLs, and potential secrets.
        </li>
        <li>
          <strong>URL List Finder:</strong> Discovers all known URLs for a target domain by querying the Wayback Machine.
        </li>
        <li>
          <strong>Subdomain Finder:</strong> Finds subdomains by searching public Certificate Transparency logs.
        </li>
      </ul>
      
      <h4>Payload & Exploitation Tools</h4>
      
      <ul>
        <li>
          <strong>Payload Forge:</strong> Generate advanced variations of a base payload using obfuscation and encoding 
          techniques designed to bypass Web Application Firewalls.
        </li>
        <li>
          <strong>SSTI Forge:</strong> Generate Server-Side Template Injection payloads tailored for specific template 
          engines and goals.
        </li>
        <li>
          <strong>OOB Interaction Helper:</strong> A utility to generate Out-of-Band payloads for blind vulnerabilities.
        </li>
      </ul>
      
      <h3>Getting Started</h3>
      
      <ol>
        <li>Click the <strong>Settings</strong> icon in the header to configure your API key.</li>
        <li>Select a tool from the navigation menu to begin your security analysis.</li>
        <li>For most tools, you'll need to provide a URL, code snippet, or other input to analyze.</li>
        <li>Review the results and use the provided recommendations to improve security.</li>
      </ol>
      
      <p class="text-red-400">
        <strong>Disclaimer:</strong> This application is provided for educational and research purposes only. 
        Only test applications for which you have explicit, written permission from the owner.
      </p>
    </div>
  </div>
</template>

<script setup>
defineEmits(['close']);
</script>
