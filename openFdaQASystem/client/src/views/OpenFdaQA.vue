<template>
  <div class="openfdaqa">
    <b-container>
      <b-row>
        <b-col>
          <h1>OpenFDA Question-Answering System</h1><hr><br>
        </b-col>
      </b-row>
      <b-row class="my-5" id="inputArea">
        <b-col>
          <b-form @submit="onSubmit">
            <b-input-group>
              <b-form-input type="text" v-model="queryText"></b-form-input>
              <b-input-group-append>
                <b-button type="submit" variant="outline-info">Ask!</b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form>
        </b-col>
      </b-row>
      <b-row id="outputArea"
        v-bind:key="index"
        v-for="(result, index) in results">
        <b-col>
          <ResultCard
            class="mb-3"
            :originalQuery="result.Query"
            :textResult="result.Text">
          </ResultCard>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios';
import ResultCard from '@/components/ResultCard.vue';

export default {
  name: 'OpenFdaQA',
  components: {
    ResultCard,
  },
  data() {
    return {
      queryText: '',
      results: [],
      maxResults: 5,
    };
  },
  methods: {
    addResultCard(resultData) {
      if (this.results.length === this.maxResults) {
        // display only maxResults at a time
        this.results.pop();
      }
      this.results.unshift(resultData);
    },
    handleRequest() {
      const path = 'http://127.0.0.1:5000/interpret';
      axios.get(path, {
        params: {
          q: this.queryText,
        },
      }).then((resp) => {
        this.addResultCard(resp.data);
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmit(event) {
      event.preventDefault();
      this.handleRequest();
    },
  },
};
</script>
