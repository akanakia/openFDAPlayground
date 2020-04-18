<template>
  <div class="ResultCard">
    <b-card :title="originalQuery">
      <b-form-textarea
        v-model="textResult"
        row="3"
        size="sm">
      </b-form-textarea>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "ResultCard",
  props: {
    originalQuery: String,
    textResult: String
  },
}
</script>