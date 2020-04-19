<template>
  <div class="ResultCard">
    <b-card :title="originalQuery">
      <b-form-textarea
        v-model="textResult"
        rows="5"
        size="sm"
        no-resize>
      </b-form-textarea>
    </b-card>
  </div>
</template>

<script>
export default {
  name: 'ResultCard',
  props: {
    originalQuery: String,
    textResult: String,
  },
};
</script>
