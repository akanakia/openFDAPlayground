<template>
  <div class="openfdaqa">
    <b-container>
      <b-row>
        <b-col>
          <h1>OpenFDA Question-Answering System</h1><hr><br>
        </b-col>
      </b-row>
      <b-row id="inputArea">
        <b-col>
          <b-form @submit="onSubmit">
            <b-input-group>
              <b-form-input type="text" v-model="queryText" @keyup.enter="onSubmit"></b-form-input>
              <b-input-group-append>
                <b-button type="submit" variant="outline-info">Ask!</b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form>
        </b-col>
      </b-row>
      <b-row id="outputArea">
        <b-col
        v-bind:key="result"
        v-for="result in results">
          <ResultCard :originaQuery="result.Query" :textResult="result.Text"></ResultCard>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import ResultCard from '@/components/ResultCard.vue';

export default {
  name: 'OpenFdaQA',
  components: {
    ResultCard
  },
  data() {
    return {
      queryText: '',
      results: [],
      maxResults: 5,
    }
  },
  methods: {
    addResultCard(resultData) {
      if (this.results.length == maxResults)
      {
        // display only maxResults at a time
        this.results.pop;
      }
      this.results.unshift(resultData);
    },
    onSubmit() {

    },
  },
};
</script>
