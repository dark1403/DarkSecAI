<template>
  <div class="bg-gray-800 rounded-lg shadow-xl p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold text-white">Developer Documentation</h2>
      <UButton
        icon="i-heroicons-x-mark"
        variant="ghost"
        color="gray"
        @click="$emit('close')"
      />
    </div>

    <div class="prose prose-invert max-w-none">
      <h3>DarkSec-AI Developer Guide</h3>
      
      <p>
        This documentation provides an overview of the DarkSec-AI architecture and implementation details
        for developers who want to understand or contribute to the project.
      </p>
      
      <h4>Architecture Overview</h4>
      
      <p>DarkSec-AI is built using a modern stack:</p>
      
      <ul>
        <li><strong>Frontend:</strong> Nuxt.js 4 with Nuxt UI 4 components</li>
        <li><strong>Backend:</strong> Django 5.x with Django REST Framework</li>
        <li><strong>AI Provider:</strong> Backend AI Service (via Django REST API)</li>
      </ul>
      
      <h4>Backend Structure</h4>
      
      <p>The Django backend is organized as follows:</p>
      
      <ul>
        <li><strong>Models:</strong> Data structures for storing analysis results, reports, and chat history</li>
        <li><strong>Views:</strong> API endpoints for handling requests from the frontend</li>
        <li><strong>Services:</strong> Business logic for interacting with the Django REST API</li>
        <li><strong>Prompts:</strong> Carefully crafted prompts for different analysis types</li>
      </ul>
      
      <h4>Frontend Structure</h4>
      
      <p>The Nuxt.js frontend follows a component-based architecture:</p>
      
      <ul>
        <li><strong>Pages:</strong> Main views corresponding to different tools</li>
        <li><strong>Components:</strong> Reusable UI elements and tool-specific components</li>
        <li><strong>Stores:</strong> State management using Pinia</li>
        <li><strong>Layouts:</strong> Page layouts for consistent UI structure</li>
        <li><strong>Utils:</strong> Helper functions and utilities</li>
      </ul>
      
      <h4>AI Integration</h4>
      
      <p>
        DarkSec-AI uses AI models via the Django backend for all security analysis capabilities. The integration follows a pattern:
      </p>
      
      <ol>
        <li><strong>Prompt Engineering:</strong> Carefully crafted prompts for different analysis types</li>
        <li><strong>Recursive Analysis:</strong> Multiple runs with different prompt variations for reliability</li>
        <li><strong>Consolidation:</strong> Merging results from multiple analyses for better accuracy</li>
        <li><strong>Validation:</strong> Additional checks to filter out potential false positives</li>
      </ol>
      
      <h4>Contributing</h4>
      
      <p>To contribute to DarkSec-AI:</p>
      
      <ol>
        <li>Fork the repository</li>
        <li>Create a feature branch</li>
        <li>Make your changes</li>
        <li>Write tests if applicable</li>
        <li>Submit a pull request</li>
      </ol>
      
      <h4>API Documentation</h4>
      
      <p>
        The backend exposes a RESTful API for all functionality. Key endpoints include:
      </p>
      
      <ul>
        <li><code>/api/analyze/url/</code> - URL analysis (DAST)</li>
        <li><code>/api/analyze/code/</code> - Code analysis (SAST)</li>
        <li><code>/api/analyze/headers/</code> - Security headers analysis</li>
        <li><code>/api/forge/payloads/</code> - Generate payload variations</li>
        <li><code>/api/chat/messages/</code> - WebSec Agent chat functionality</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineEmits(['close']);
</script>
