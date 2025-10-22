<template>
  <div v-html="renderedContent"></div>
</template>

<script setup>
import { marked } from 'marked';
import createDOMPurify from 'isomorphic-dompurify';

const props = defineProps({
  content: {
    type: String,
    required: true
  }
});

const renderedContent = computed(() => {
  if (!props.content) return '';
  
  // Configure marked options
  marked.setOptions({
    breaks: true,
    gfm: true,
    headerIds: false
  });
  
  // Render markdown to HTML
  const html = marked(props.content);
  
  // Sanitize HTML to prevent XSS
  const DOMPurify = createDOMPurify();
  return DOMPurify.sanitize(html);
});
</script>

<style scoped>
:deep(pre) {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 0.75rem;
  border-radius: 0.375rem;
  overflow-x: auto;
}

:deep(code) {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.875rem;
}

:deep(p) {
  margin-bottom: 1rem;
}

:deep(ul), :deep(ol) {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

:deep(ul) {
  list-style-type: disc;
}

:deep(ol) {
  list-style-type: decimal;
}

:deep(a) {
  color: #06b6d4;
  text-decoration: underline;
}

:deep(a:hover) {
  color: #0891b2;
}

:deep(h1), :deep(h2), :deep(h3), :deep(h4), :deep(h5), :deep(h6) {
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

:deep(h1) {
  font-size: 1.5rem;
}

:deep(h2) {
  font-size: 1.25rem;
}

:deep(h3) {
  font-size: 1.125rem;
}

:deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

:deep(th), :deep(td) {
  border: 1px solid #374151;
  padding: 0.5rem;
}

:deep(th) {
  background-color: rgba(55, 65, 81, 0.5);
}

:deep(blockquote) {
  border-left: 4px solid #4b5563;
  padding-left: 1rem;
  margin-left: 0;
  margin-right: 0;
  font-style: italic;
}
</style>
