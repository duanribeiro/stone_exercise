<template>
  <div>
    <b-alert variant="dark" show>{{ message }}</b-alert>
    <br>
  </div>
</template>
<script>
export default {
  props: ['message'],
};
</script>
